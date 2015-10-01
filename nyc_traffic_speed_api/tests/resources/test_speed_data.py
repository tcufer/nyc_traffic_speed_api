#!flask/bin/python
import os
import sys
import unittest
import tempfile
from resources.speed_data import SpeedDataResource, SpeedDataListResource

#tests
class TestSpeedDataResource(unittest.TestCase):
	
	def test_get(self):
		speed_data = SpeedDataResource()
		response = SpeedDataResource.get(speed_data, 1)
		self.assertEqual(200, response[1])

class TestSpeedDataListResource(unittest.TestCase):

	def test_get(self):
		speed_data_list = SpeedDataListResource()
		response = SpeedDataListResource.get(speed_data_list)
		self.assertEqual(200, response[1])

if __name__ == '__main__':
    unittest.main()