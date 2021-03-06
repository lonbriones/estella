""""""""""""""""""""""""""""""""" 
Logme Controller Unit test case
Author: Dionylon Briones
Date Created: January 14, 2009
Date Modified: January 14, 2009
"""""""""""""""""""""""""""""""""
import unittest
from maelisapy import logme
from datetime import datetime

class LogMeTest(unittest.TestCase):

	def setUp(self):
		self.logme = logme.LogMeController()
		self.data = {
			'plogno': 123,
			'userid': 'lon123',
			'timein': datetime.today(),
			'timeout': datetime.today(),
			'terminal': ''
		}

		success = self.logme.addLog(self.data)
		self.assertEquals(True, success)

	def tearDown(self):
		success = self.logme.deleteLogByUserId(self.data['userid'])
		self.assertEquals(True, success)

	def test_getLogsByUserId(self):
		rows = self.logme.getLogsByUserId(self.data['userid'], 1, 1)
		self.assertTrue(rows)
	
def suite():
	test_suite = unittest.makeSuite(LogMeTest, 'test')
	return test_suite

if __name__ == '__main__':
	unittest.main()
