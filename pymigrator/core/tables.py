import codecs
import csv
import os
import sys
from copy import deepcopy

import pymysql

from .indices import ConversionIndex, FieldIndex


class Table(object):
    def __init__(self, header, table_name='', default_values=None):
        self.header = header
        self.table_name = table_name
        self.content = []
        self.field_index = FieldIndex(self)

        if not default_values:
            default_values = {}
        for h in set(default_values.keys()).difference(set(self.header)):
            del default_values[h]
        for h in self.header:
            if h not in default_values:
                default_values[h] = ''

        self.default_values = default_values

    def __iter__(self):
        return self.content.__iter__()

    def headers(self):
        return self.header

    def row(self, row):
        return self.content[row]

    def num_rows(self):
        return len(self.content)

    def num_cols(self):
        return len(self.header)

    def insert_row(self, row):
        if len(row) != len(self.header):
            raise ValueError('table column mismatch')
        self.content.append(row)

    def print_status(self, stream=sys.stdout):
        stream.write('%s, %d records\n' % (self.table_name, self.num_rows()))

    def slice(self, size):
        result = []

        current = self.__class__(self.header, self.table_name)

        for idx, row in enumerate(self):
            current.insert_row(row)
            if current.num_rows() == size:
                result.append(current)
                current = self.__class__(self.header, self.table_name)

        if current and current.num_rows() > 0:
            result.append(current)

        return result


class DictTable(Table):
    """
    DictTable

    Table composed of dict objects.
    Every row is stored as a dict object.
    """

    def __init__(self, header, table_name='', default_values=None):
        super(DictTable, self).__init__(header, table_name, default_values)
        self.indices = {}

    def insert_row(self, table_row, check_validity=False):
        """
        :param table_row: A row data. Accepts only a dict object, encoded in UTF-8.
        :param check_validity:
        :return: row
        """
        if check_validity:
            filtered_row = {}
            for h in self.header:
                if h in table_row:
                    filtered_row[h] = table_row[h]
                else:
                    filtered_row[h] = self.default_values[h]
        else:
            filtered_row = table_row

        self.content.append(filtered_row)

    def create_index(self, index_field):
        """
        Create inner index
        """
        if isinstance(index_field, str):
            idx = ConversionIndex(index_field)
            for i, row in enumerate(self):
                idx.set_index(row[index_field], i)
            self.indices[index_field] = idx
        elif isinstance(index_field, list):
            idx = ConversionIndex('-'.join(index_field))
            for i, row in enumerate(self):
                idx.set_index([row[f] for f in index_field], i)
            self.indices[index_field] = idx

    def get_row_num_by_indexed_value(self, index_name, field_value):
        idx = self.indices[index_name]
        if idx.is_origin_indexed(field_value):
            return idx.get_target_by_origin(field_value)
        else:
            return None

    def get_row_by_indexed_value(self, index_name, field_value):
        idx = self.indices[index_name]
        if idx.is_origin_indexed(field_value):
            return self.row(idx.get_target_by_origin(field_value))
        else:
            return None

    def new_item(self):
        self.insert_row(deepcopy(self.default_values))
        return self.row(-1)

    @staticmethod
    def load_csv(file_name, include_header=True, header=None, filter_null=True, table_name='', encoding='utf-8'):
        """
        :param file_name: input csv file name. UTF-8 encoding only, quote character <">, header must be present.
        :param include_header: True if file contains header data at the first row.
                               If it is False, you have to provide a valid header list.
        :param header: a header list
        :param filter_null:
        :param table_name:
        :param encoding:

        :return: Table object
        """
        read_bytes = min(4, os.path.getsize(file_name))
        with open(file_name, 'rb') as f:
            raw = f.read(read_bytes)

        bom_list = (
            ('utf-8-sig', (codecs.BOM_UTF8,)),
            ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)),
            ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)),
        )

        for enc, boms in bom_list:
            if any(raw.startswith(bom) for bom in boms):
                encoding = enc
                break

        with open(file_name, 'r', encoding=encoding) as f:
            if include_header:
                line = f.readline().strip()
                header = [i.strip('"').strip() for i in line.split(',')]
            reader = csv.DictReader(f, fieldnames=header, delimiter=',', quotechar='"')
            table = DictTable(header)
            for row in reader:
                if filter_null:
                    for k, v in row.items():
                        if v == 'NULL':
                            row[k] = None
                table.insert_row(row)

        if table_name:
            table.table_name = table_name
        else:
            table.table_name = file_name

        return table

    def save_csv(self, file_name, export_header=False, stream=sys.stdout):
        """
        :param file_name: output csv file name. UTF-8 encoding only.
        :param export_header:
        :param stream:

        :return:
        """
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', quotechar='"')
            if export_header:
                writer.writerow(dict(zip(self.header, self.header)))
            writer.writerows(self.content)

        stream.write('%s exported as %s. %s records.\n' % (self.table_name, file_name, self.num_rows()))

    @classmethod
    def load_from_mysql_table(cls, host='', port='', user='', passwd='', db='', table='', charset='utf8',
                              unix_socket='',
                              _conn=None, headers=None):

        if _conn:
            conn = _conn
        else:
            if host:
                conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
            elif unix_socket:
                conn = pymysql.connect(unix_socket=unix_socket, user=user, passwd=passwd, db=db, charset=charset)
            else:
                raise RuntimeError('Provide a host name or unix socket path')

        # just for detecting columns
        if not headers:
            cur = conn.cursor()
            cur.execute(cls.get_mysql_table_header_query(db, table))
            headers = [r[0] for r in cur.fetchall()]
            del cur

        t = DictTable(headers)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM %s" % (table,))

        for r in cur.fetchall():
            t.insert_row(r)

        return t

    @staticmethod
    def get_mysql_table_header_query(db, table):
        q = 'SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=\'{}\' AND TABLE_NAME=\'{}\' ' + \
            'ORDER BY ORDINAL_POSITION'

        return q.format(pymysql.converters.escape_string(db), pymysql.converters.escape_string(table))

    def get_value_count(self, field_name, value):
        if field_name not in self.header:
            raise RuntimeError("'%s' is not in header!" % (field_name,))

        count = 0
        for item in self:
            if item[field_name] == value:
                count += 1

        return count

    def print_dict_range(self, field_name, stream=sys.stdout):
        if self.num_rows():
            stream.write(
                "'%s', ID %d - %d\n" % (self.table_name, self.row(0)[field_name], self.row(-1)[field_name])
            )

    def get_mysql_insert_query(self, database_name=None):

        if database_name:
            qualified_name = '`%s.%s`' % (database_name, self.table_name)
        else:
            qualified_name = '`%s`' % self.table_name

        fields = self.header
        fields_text = '({})'.format(','.join(fields))

        values_list = []
        for row in self:
            cols = [pymysql.escape_string(str(row[field])) for field in fields]
            values_list.append('({})'.format(','.join(['\'%s\'' % col.replace('\'', '\'\'') for col in cols])))
        values_text = ','.join(values_list)

        del values_list

        return "INSERT INTO {} {} VALUES {};".format(qualified_name, fields_text, values_text)

    def create_field_index(self, name, **kwargs):
        return self.field_index.create_index(name, **kwargs)

    def filter_field_index(self, name, filters, dict_key=None):
        return self.field_index.filter_index(name, filters, dict_key)


class AutoIncrementMixin(object):
    def __init__(self, ai_field=None, ai_begin=1):
        self.ai_field = ai_field
        self.next_id = ai_begin

    def increment_id(self):
        self.next_id += 1


class AutoIncrementDictTable(DictTable, AutoIncrementMixin):
    def __init__(self, header, table_name='', ai_field=None, ai_begin=1, default_values=None):
        """
        :param header: header columns. Include all fields
        :param table_name: table's name
        :param ai_field: specify a field used for auto increment
        :param ai_begin: begin index
        :return:
        """
        if ai_field not in header:
            raise ValueError('id_field not in header')
        super(AutoIncrementDictTable, self).__init__(header, table_name, default_values)
        self.ai_field = ai_field
        self.next_id = ai_begin

    def new_item(self):
        item = super(AutoIncrementDictTable, self).new_item()
        item[self.ai_field] = self.next_id
        self.increment_id()
        return self.row(-1)

    def print_dict_range(self, field_name='', stream=sys.stdout):
        if self.num_rows():
            if not field_name:
                field_name = self.ai_field
            stream.write(
                "'%s', ID %d - %d\n" % (
                    self.table_name,
                    self.row(0)[field_name],
                    self.row(-1)[field_name]
                )
            )

    def slice(self, size):
        result = []

        if self.num_rows() > 0:
            ai_begin = self.row(0)[self.ai_field]
        else:
            ai_begin = 1

        current = self.__class__(self.header, self.table_name, self.ai_field, ai_begin)

        for idx, row in enumerate(self):
            current.insert_row(row)
            if current.num_rows() == size:
                result.append(current)
                current = self.__class__(self.header, self.table_name, self.ai_field, self.row(idx)[self.ai_field])

        if current and current.num_rows() > 0:
            result.append(current)

        return result
