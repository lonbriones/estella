""" Location Unit test case
Author: Dionylon Briones
Date Created: November 14, 2008
"""
import unittest
from maelisapy.location import Location

class LocationTest(unittest.TestCase):
	def setUp(self):
		self.loc = Location()

	def tearDown(self):
		pass

	def test_getLocation(self):
		row = self.loc.getLocation('GS')
		self.assertTrue(row)

	def test_saveLocation(self):
		res = self.loc.saveLocation('GS', 'GS')
		self.assertTrue(res)


def suite():
    test_suite = unittest.makeSuite(LocationTest, 'test')
    return test_suite

if __name__ == '__main__':
    unittest.main()

