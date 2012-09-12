""" 
Catalog Controller Unit test case
Author: Dionylon Briones
Date Created: November 14, 2008
Date Modified: Dec 28, 2008
"""
import unittest
from maelisapy import catalog
from datetime import datetime

class CatalogTest(unittest.TestCase):

	def setUp(self):
		self.catalog = catalog.CatalogController()
		self.data = {
			'fid': 'fid1', 
			'moudle': '1', 
			'mtype': '1', 
			'marc': 'aa',
			'holdings':[
				{
					'accessno': 'acc 1',
					'location': 'loc 1',
					'barcode': 'barcode 4',
				},{
					'accessno': 'acc 2',
				}
			]
		}

		self.addCatalog()

	def tearDown(self):
		success = self.catalog.deleteCatalog('fid1')
		self.assertEquals(True, success)

	def addCatalog(self):
		success = self.catalog.save(self.data)
		self.assertEquals(True, success)
	
	def assertCatalog(self, row):

		#functions that don't return the 'count'
		#has no 'data' key
		if row.has_key('data'):
			row = row['data']

		for key in self.data:
			if key != 'holdings':
				self.assertEquals(self.data[key], row[key])

		i = 0
		for holdings in row['holdings']:
			for key in holdings:
				if self.data['holdings'][i].has_key(key):
					self.assertEquals(self.data['holdings'][i][key], row['holdings'][i][key])
			i = i + 1

	def test_getCatalogById(self):
		#check if it's really saved :D
		row = self.catalog.getCatalogById('fid1')
		self.assertCatalog(row)


	def test_getCatalogByAccessNo(self):
		row = self.catalog.getCatalogByAccessNo(self.data['holdings'][0]['accessno'])
		self.assertCatalog(row)
		row = self.catalog.getCatalogByAccessNo(self.data['holdings'][1]['accessno'])
		self.assertCatalog(row)

	def test_deleteAccessNo(self):
		success = self.catalog.deleteAccessNo(self.data['holdings'][0]['accessno'])
		self.assertEquals(True, success)

		success = self.catalog.deleteAccessNo('asdfas')
		self.assertFalse(success)

	def test_getCatalogByLocation(self):
		rows = self.catalog.getCatalogByLocation(self.data['holdings'][0]['location'], 1,0)
		self.assertCatalog(rows['data'][0])
	
	def test_getCatalogByBarcode(self):
		row = self.catalog.getCatalogByBarcode(self.data['holdings'][0]['barcode'])
		self.assertCatalog(row)
	
	def test_assignBarcode(self):
		success = self.catalog.assignBarcode('acc 1', 'barcode 1')
		self.assertEquals(True, success)
		row = self.catalog.getCatalogByBarcode('barcode 1')
		self.assertTrue(row)
		self.assertEquals('barcode 1', row['holdings'][0]['barcode'])

	def test_Location(self):

		success = self.catalog.addLocation('oldloc', 'Old Location')
		self.assertEquals(True, success)
		
		self.data['holdings'][0]['location'] = 'oldloc'
		self.data['holdings'][1]['location'] = 'oldloc'
		self.addCatalog()

		success = self.catalog.renameLocation('oldloc', 'newloc', 'New Location')
		self.assertEquals(True, success)

		rows = self.catalog.getCatalogByLocation('newloc', 20, 0)
		self.assertTrue(rows)
		for row in rows['data']:
			for holdings in row['holdings']:
				self.assertEquals('newloc', holdings['location'])

		success = self.catalog.deleteLocation('newloc')
		self.assertEquals(True, success)

	def test_getCatalog(self):
		rows = self.catalog.getCatalog('', 5, 5)
		self.assertTrue(rows)
		self.assertEquals(5, len(rows['data']))

	def test_getMarcTags(self):
		rows = self.catalog.getMarcTags()
		self.assertTrue(rows)

	def test_addMarcTag(self):
		#add a tag
		success = self.catalog.addMarcTag('991', 'sadfsadf', 'F', 'F', 'safdsadf')
		self.assertEquals(True, success)

		#delete it
		success = self.catalog.deleteMarcTag('991')
		self.assertEquals(True, success)

def suite():
    test_suite = unittest.makeSuite(CatalogTest, 'test')
    return test_suite

if __name__ == '__main__':
    unittest.main()
