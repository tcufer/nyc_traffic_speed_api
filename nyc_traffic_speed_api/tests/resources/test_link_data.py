import unittest
import json
from nyc_traffic_speed_api import app
from resources.link_data import LinkDataResource, LinkDataListResource


def resp_data_to_dict(response, encoding='utf-8'):
	return json.loads(response.data.decode(encoding))


#tests
class TestLinkDataResource(unittest.TestCase):
	
	def setUp(self):
		app.config['TESTING'] = True
		self.app = app
		self.client = self.app.test_client()

	# def tearDown(self):

	def test_get_returns_200(self):
		link_data = LinkDataResource()
		response = self.client.get('/linkData/4329499', follow_redirects=True)
		self.assertEqual(response.status_code, 200) 

	def test_get_returns_404(self):
		link_data = LinkDataResource()
		response = self.client.get('/linkData/0000', follow_redirects=True)
		self.assertEqual(response.status_code, 404)


	def test_get_returns_valid_data(self):
		response = self.client.get('/linkData/4329499', follow_redirects=True)
		response_data = resp_data_to_dict(response)
		link = response_data['linkData']
		assert isinstance(response_data.pop('linkData'), list)
	

class TestLinkDataListResource(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		self.app = app
		self.client = self.app.test_client()

	# def tearDown(self):

	def test_get_returns_200(self):
		link_data = LinkDataResource()
		response = self.client.get('/linkData', follow_redirects=True)
		self.assertEqual(response.status_code, 200) 

	def test_get_returns_valid_data(self):
		response = self.client.get('/linkData', follow_redirects=True)
		response_data = resp_data_to_dict(response)
		link = response_data['linksList']
		assert isinstance(response_data.pop('linksList'), list)


if __name__ == '__main__':
	unittest.main()