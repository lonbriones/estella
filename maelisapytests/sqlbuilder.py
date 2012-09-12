""" SqlBuilder Unit test case
Author: Dionylon Briones
Date Created: November 22, 2008
"""
import unittest
from maelisapy.sqlbuilder import SqlBuilder
from maelisapy.maelisadb import maelisadb

class SqlBuilderTest(unittest.TestCase):
	def setUp(self):
		self.sqlbuilder = SqlBuilder('control')
		self.db = maelisadb()

	def test_selectAll(self):
		sql = self.sqlbuilder.q()
		self.assertEquals(sql, 'select * from control')
		self.db.execute(sql)
		

	def test_selectFields(self):
		sql = self.sqlbuilder.q(fields='fid')
		self.assertEquals(sql,'select fid from control')
		self.db.execute(sql)

	def test_selectWithFilter(self):
		sql = self.sqlbuilder.q(filters="accessno='acc001'")
		self.assertEquals(sql, "select * from control where accessno='acc001'")
		self.db.execute(sql)

	def test_selectOrderBy(self):
		sql = self.sqlbuilder.q(orderby='accessno', direction='asc')
		self.assertEquals(sql, "select * from control order by accessno asc")
		self.db.execute(sql)

	def test_limit(self):
		sql = self.sqlbuilder.q(limit=50, offset=100)
		self.assertEquals(sql, "select first 100 skip 50 * from control")
		self.db.execute(sql)

	def test_selectWithSeveralArguments(self):
		sql = self.sqlbuilder.q(
			fields = 'accessno, fid',
			filters = "accessno='acc001'",
			orderby = 'accessno',
			direction = 'desc',
			limit = 50,
			offset = 100
		)

		self.assertEquals(sql, "select first 100 skip 50 accessno, fid from control where accessno='acc001' order by accessno desc")
		self.db.execute(sql)

def suite():
    test_suite = unittest.makeSuite(SqlBuilderTest, 'test')
    return test_suite

if __name__ == '__main__':
    unittest.main()

	
