from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo
from errors import ValidationError, not_found
import pymongo
import types

app = Flask(__name__)
api = Api(app)
# mongo = PyMongo(app)



# connect to another MongoDB server altogether
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'dev_nyc_traffic_speed'
mongo = PyMongo(app, config_prefix='MONGO')

@app.errorhandler(404)
def not_found_error(e):
    return not_found('Not found')


# @app.errorhandler(400)
# def bad_request_error(e):
#     return bad_request('invalid request')

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