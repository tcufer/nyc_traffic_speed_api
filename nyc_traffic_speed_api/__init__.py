from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
# from flask.ext.pymongo import PyMongo
from errors import ValidationError, not_found
import types

app = Flask(__name__)
api = Api(app, catch_all_404s=True)
# auth = HTTPBasicAuth()
# mongo = PyMongo(app)



# connect to another MongoDB server altogether
# app.config['MONGO_HOST'] = '127.0.0.1'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'dev_nyc_traffic_speed'
# mongo = PyMongo(app, config_prefix='MONGO')


# @auth.get_password
# def get_password(username):
#     if username == 'tomaz':
#         return 'python'
#     return None


# @auth.error_handler
# def unauthorized():
#     # return 403 instead of 401 to prevent browsers from displaying the default
#     # auth dialog
    # return make_response(jsonify({'message': 'Unauthorized access'}), 403)

from auth import auth
@app.before_request
@auth.login_required
def before_request():
    pass



# @app.errorhandler(404)
# def not_found_error(e):
#     return not_found('Not found')


# @app.errorhandler(400)
# def bad_request_error(e):
#     return bad_request('invalid request')

# def mongodb_conn():
#         try:
#             client = pymongo.MongoClient("mongodb://admin:iSWR8Y751s@ds051625.mongolab.com:51625/nyc_traffic_speed", tz_aware=True)
#             # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/dev_nyc_traffic_speed", tz_aware=True)
#             conn = client.get_default_database()
#             return conn
#             # return pymongo.MongoClient("mongodb://admin:iSWR8Y751s@ds051625.mongolab.com:51625/nyc_traffic_speed", tz_aware=True)
#             # return pymongo.MongoClient("mongodb://127.0.0.1:27017", tz_aware=True).dev_nyc_traffic_speed
#         except pymongo.errors.ConnectionFailure, e:
# 			print "Could not connect to server: %s" % e

def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

# db_conn = mongodb_conn()
api.route = types.MethodType(api_route, api)

if __name__ == '__main__':
    app.run()