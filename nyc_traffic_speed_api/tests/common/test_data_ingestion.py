import unittest
import json
from resources import app
from models import Link, Sensor
from common.data_ingestion import insert_traffic_data

#tests
class TestDataIngestion(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        Sensor.drop_collection()
        Link.drop_collection()

    # def tearDown(self):
    #     # Sensor.drop_collection()
    #     # Link.drop_collection()
    #     pass

    def test_insert_traffic_data(self):
         self.assertTrue(insert_traffic_data())

    # def test_link_collection(self):
        # test return of a query;  assertTrue (links.count()>=0) and assertTrue (links.count()>=0)

if __name__ == '__main__':
    unittest.main()