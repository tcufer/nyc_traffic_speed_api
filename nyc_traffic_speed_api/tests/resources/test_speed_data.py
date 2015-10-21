import unittest
import json
from nyc_traffic_speed_api import app
from resources.speed_data import SpeedSensorResource, SpeedSensorsListResource


def resp_data_to_dict(response, encoding='utf-8'):
	return json.loads(response.data.decode(encoding))

#tests
class TestSpeedSensorResource(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		self.app = app
		self.client = self.app.test_client()

	# def tearDown(self):
		# pass

	def test_get_returns_200(self):
		response = self.client.get('/speedData/1', follow_redirects=True)
		self.assertEqual(response.status_code, 200) 

	def test_get_returns_404(self):
		response = self.client.get('/speedData/999', follow_redirects=True)
		self.assertEqual(response.status_code, 404)
	
	def test_get_returns_valid_data(self):
		response = self.client.get('/speedData/1', follow_redirects=True)
		response_data = resp_data_to_dict(response)
		sensor = response_data['speedSensor']
		assert isinstance(response_data.pop('speedSensor'), list)
		self.assertEqual(sensor[0]['sensorId'],'1')


class TestSpeedSensorsListResource(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		self.app = app
		self.client = self.app.test_client()

	def test_get_returns_200(self):
		response = self.client.get('/speedData', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_get_returns_valid_data(self):
		response = self.client.get('/speedData', follow_redirects=True)
		response_data = resp_data_to_dict(response)
		sensor = response_data['speedSensors']
		assert isinstance(response_data.pop('speedSensors'), list)

if __name__ == '__main__':
    unittest.main()