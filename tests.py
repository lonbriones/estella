import unittest
from maelisapytests import catalog
from maelisapytests import logme


def suite():
	test_suite = unittest.TestSuite()
	test_suite.addTest(catalog.suite())
	#test_suite.addTest(logme.suite())
	return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())


