from datetime import datetime

import pytz

from .tables import DictTable, AutoIncrementDictTable


def dump_table(db, user, passwd, table, output, host='localhost', port=3306):
    table = DictTable.load_from_mysql_table(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        db=db,
        table=table
    )

    table.save_csv(output, True)


def convert_time(naive_time_string, tz_from, tz_to, fmt='%Y-%m-%d %H:%M:%S'):
    t = pytz.timezone(tz_from).localize(datetime.strptime(naive_time_string, fmt))

    return t.astimezone(pytz.timezone(tz_to)).strftime(fmt)


def parse_datetime(input_data, parse_format):
    output = ''

    try:
        d = datetime.strptime(input_data, parse_format)
        output = d.strftime('%y-%m-%d %H:%M:%S')
    except ValueError:
        pass

    return output


def rollback_sql(f, db_table_name, pk, table, table_key=None):
    """
    :param f:
    :type  f: file-like objects

    :param db_table_name:
    :type  db_table_name: str

    :param pk: str
    :type  pk: int|str

    :param table:
    :type  table: AutoIncrementDictTable

    :param table_key:
    :return:
    """
    if not table_key:
        table_key = pk
    f.write(
        'DELETE FROM `%s` WHERE `%s` BETWEEN %s AND %s;\n' % (
            db_table_name, pk, table.row(0)[table_key], table.row(-1)[table_key]
        )
    )
