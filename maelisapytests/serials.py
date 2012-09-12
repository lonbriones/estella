""" Serial Unit test case
Author: Dionylon Briones
Date Created: November 14, 2008
"""

import unittest
from maelisapy.serials import Serials

class SerialsTest(unittest.TestCase):

	def test_serials(self):
		ser = Serials()
		self.assertTrue(ser.getSerials() == 'lon')

def suite():
    test_suite = unittest.makeSuite(SerialsTest, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()


