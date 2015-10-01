#!flask/bin/python
import os
import sys
import unittest
import tempfile
from resources.link_data import LinkDataResource, LinkDataListResource

#tests
class TestLinkDataResource(unittest.TestCase):
	
	def test_get(self):
		link_data = LinkDataResource()
		response = LinkDataResource.get(link_data, 4329499)
		self.assertEqual(200, response[1])

class TestLinkDataListResource(unittest.TestCase):

	def test_get(self):
		link_data_list = LinkDataListResource()
		response = LinkDataListResource.get(link_data_list)
		self.assertEqual(200, response[1])

if __name__ == '__main__':
    unittest.main()