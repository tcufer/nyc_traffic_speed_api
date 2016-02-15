import unittest
from werkzeug.exceptions import BadRequest
from .test_client import TestClient
from models import db, User
from resources import app
from datetime import datetime as dt

# from api.errors import ValidationError

class TestAPI(unittest.TestCase):
    default_username = 'saul'
    default_password = 'goodman'

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        u = User(username=self.default_username)
        u.set_password(self.default_password)
        u.save()
        self.client = TestClient(self.app, self.default_username, self.default_password)

    def tearDown(self):
        User.drop_collection()
        self.ctx.pop()


    def test_password_auth(self):
        self.app.config['USE_TOKEN_AUTH'] = False
        good_client = TestClient(self.app, self.default_username,
                                 self.default_password)
        rv, json = good_client.get('/trafficSpeed')
        self.assertTrue(rv.status_code == 200)

    def test_bad_auth(self):
        bad_client = TestClient(self.app, 'abc', 'def')
        rv, json = bad_client.get('/trafficSpeed')
        self.assertTrue(rv.status_code == 401)

    def test_link(self):
        # get all links
        rv, json = self.client.get('/trafficLink/')
        self.assertTrue(rv.status_code == 200)
        assert isinstance(json.pop('trafficLinkList'), list)


        #get a link by linkId
        rv, json = self.client.get('/trafficLink/4616337')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('borough' and
                        'encodedPolyLine' and
                        'encodedPolyLineLvls' and
                        'linkId' and
                        'linkName' and
                        'linkPoints' and
                        'owner' in json['Link'][0])

        #invalid id
        rv, json = self.client.get('/trafficLink/123456789')
        self.assertTrue(rv.status_code == 404)

    def test_speed(self):
        # get data of all speed sensors
        rv, json = self.client.get('/trafficSpeed')
        self.assertTrue(rv.status_code == 200)
        assert isinstance(json.pop('speedSensor'), list)


        #get a link by linkId
        rv, json = self.client.get('/trafficSpeed/137')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('dataAsOf' and
                        'sensorId' and
                        'linkId' and
                        'speed' and
                        'travelTime' in json['speedSensor'][0])

        #invalid id
        rv, json = self.client.get('/trafficSpeed/00')
        self.assertTrue(rv.status_code == 404)


        #get sensor data by id for for date
        today = dt.strftime(dt.now(), "%Y-%m-%d")
        rv, json = self.client.get('/trafficSpeed/137/'+today)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('measures' in json['speedSensor'][0])

        #invalid date
        rv, json = self.client.get('/trafficSpeed/137/2016-22-30')
        self.assertTrue(rv.status_code == 404)
        rv, json = self.client.get('/trafficSpeed/137/2016-05-32')
        self.assertTrue(rv.status_code == 404)
        rv, json = self.client.get('/trafficSpeed/137/2020-02-02')
        self.assertTrue(rv.status_code == 404)
        rv, json = self.client.get('/trafficSpeed/137/a30')
        self.assertTrue(rv.status_code == 404)
