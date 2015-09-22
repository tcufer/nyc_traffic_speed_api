import os
import data_ingestion
import unittest
import tempfile

#tests
class TestDataIngestion(unittest.TestCase):
	
	def test_get_traffic_data(self):
		response = data_ingestion.get_traffic_data()
		self.assertEqual(200, response['status'])

if __name__ == '__main__':
    unittest.main()