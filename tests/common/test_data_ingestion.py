import unittest

from common.data_ingestion import insert_traffic_data
from common.models import Link, Sensor
from resources import app


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

    def test_bad_url_insert_traffic_data(self):
        tmp_url = self.app.config['NYC_LINK_SPEED_URL']
        self.app.config['NYC_LINK_SPEED_URL'] = ""
        self.assertEqual(insert_traffic_data(), 500)
        self.app.config['NYC_LINK_SPEED_URL'] = tmp_url
    #
    # def test_link_collection(self):
        # test return of a query;  assertTrue (links.count()>=0) and assertTrue (links.count()>=0)

    def test_insert_traffic_data(self):
         self.assertTrue(insert_traffic_data())

if __name__ == '__main__':
    unittest.main()