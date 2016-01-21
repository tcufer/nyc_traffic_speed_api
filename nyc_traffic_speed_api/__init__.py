from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
import pymongo
import types

app = Flask(__name__)
api = Api(app)

def mongodb_conn():
		try:
			return pymongo.MongoClient("mongodb://127.0.0.1:27017", tz_aware=True).dev_nyc_traffic_speed
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to server: %s" % e

def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

db_conn = mongodb_conn()
api.route = types.MethodType(api_route, api)

if __name__ == '__main__':
    app.run()