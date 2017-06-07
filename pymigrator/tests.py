import unittest
from codecs import BOM_UTF8
from os import close, remove
from tempfile import mkstemp

import pymysql

from pymigrator.core import tables


class TestTable(unittest.TestCase):
    def setUp(self):
        self.test_column = ['a', 'b', 'c']
        self.test_rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        self.table = tables.Table(self.test_column)
        for row in self.test_rows:
            self.table.insert_row(row)

    def testHeaders(self):
        self.assertListEqual(
            self.test_column,
            self.table.headers()
        )

    def testRow(self):
        for i in range(len(self.test_rows)):
            self.assertListEqual(
                self.test_rows[i],
                self.table.row(i)
            )

    def testNumRows(self):
        self.assertEqual(
            len(self.test_rows),
            self.table.num_rows()
        )

    def testNumCols(self):
        self.assertEqual(
            len(self.test_column),
            self.table.num_cols()
        )


class TestDictTable(unittest.TestCase):
    def setUp(self):
        self.test_header = ['A', 'B', 'C']

        self.test_rows = [
            {'A': '1', 'B': '4', 'C': '7'},
            {'A': '2', 'B': '5', 'C': '8'},
            {'A': '3', 'B': '6', 'C': '9'},
        ]

        self.test_name = 'test_table'

        self.index_field = 'A'

        self.table = tables.DictTable(
            header=self.test_header,
            table_name=self.test_name
        )

    def testInsertRow(self):
        for row in self.test_rows:
            self.table.insert_row(row, check_validity=True)

        for idx, row in enumerate(self.table):
            self.assertDictEqual(
                self.test_rows[idx],
                row
            )

        exception_raised = False
        try:
            self.table.insert_row({'A': '11', 'B': '12'}, check_validity=True)
        except ValueError:
            exception_raised = True

        self.assertTrue(exception_raised)

    def testCreateIndex(self):
        for row in self.test_rows:
            self.table.insert_row(row, check_validity=True)

        self.table.create_index('A')

        for i, r in enumerate(self.test_rows):
            row = self.table.get_row_by_indexed_value('A', r['A'])
            self.assertDictEqual(r, row)
            self.assertEqual(i, self.table.get_row_num_by_indexed_value('A', r['A']))

    def testSaveLoadCSV(self):
        for row in self.test_rows:
            self.table.insert_row(row)

        handle, file_name = mkstemp()
        close(handle)

        self.table.save_csv(file_name, True)

        tester_table = tables.DictTable.load_csv(file_name, True, table_name='tester_table')

        self.assertEqual(self.table.num_rows(), tester_table.num_rows())
        self.assertEqual(self.table.num_cols(), tester_table.num_cols())

        for r in range(self.table.num_rows()):
            self.assertDictEqual(self.table.row(r), tester_table.row(r))

        remove(file_name)

    def testLoadCSVWithBOM(self):
        for row in self.test_rows:
            self.table.insert_row(row)

        handle, file_name = mkstemp()
        close(handle)

        self.table.save_csv(file_name, True)

        # add BOM
        with open(file_name, 'rb') as f:
            csv = f.read()

        csv = BOM_UTF8 + csv
        with open(file_name, 'wb') as f:
            f.write(csv)

        tester_table = tables.DictTable.load_csv(file_name, True, table_name='tester_table')

        self.assertEqual(self.table.num_rows(), tester_table.num_rows())
        self.assertEqual(self.table.num_cols(), tester_table.num_cols())

        for r in range(self.table.num_rows()):
            self.assertDictEqual(self.table.row(r), tester_table.row(r))

        remove(file_name)

    def testLoadTableSQL(self):
        self.assertEqual(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS " +
            "WHERE TABLE_SCHEMA='test_db' AND TABLE_NAME='test_table' ORDER BY ORDINAL_POSITION",
            self.table.get_mysql_table_header_query('test_db', 'test_table')
        )

    def testAsMySQL(self):
        for row in self.test_rows:
            self.table.insert_row(row)

        self.assertEqual(
            "INSERT INTO `test_db.test_table` (A,B,C) VALUES ('1','4','7'),('2','5','8'),('3','6','9');",
            self.table.get_mysql_insert_query('test_db')
        )

    def testSaveLoadTable(self):

        for row in self.test_rows:
            self.table.insert_row(row)

        host = 'localhost'
        user = 'root'
        passwd = '0000'
        db = 'wordpress_test'

        create_query = "CREATE TEMPORARY TABLE IF NOT EXISTS %s " \
                       "(A VARCHAR(5) NOT NULL, B VARCHAR(5) NOT NULL, C VARCHAR(5) NOT NULL)" % self.table.table_name
        insert_query = self.table.get_mysql_insert_query()

        conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
        cur = conn.cursor()
        cur.execute(create_query)
        cur.execute(insert_query)

        tester_table = tables.DictTable.load_from_mysql_table(
            db=db, table=self.table.table_name, _conn=conn, headers=self.table.headers())

        conn.close()

        self.assertEqual(self.table.num_rows(), tester_table.num_rows())
        self.assertEqual(self.table.num_cols(), tester_table.num_cols())

        for r in range(self.table.num_rows()):
            self.assertDictEqual(self.table.row(r), tester_table.row(r))
