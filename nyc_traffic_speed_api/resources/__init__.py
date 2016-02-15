import os
from flask import Flask, abort, Response, request
from flask.ext.restful import Resource, Api
from flask_limiter import Limiter

from auth import auth
from models import db
import datetime
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_CONFIG') or
                       'config')
app.debug = False
api = Api(app)
db.init_app(app)
if app.config['USE_RATE_LIMITS']:
    limiter = Limiter(app, global_limits=["10 per minute"],  key_func = lambda : request.remote_addr)
    limiter = Limiter(app)

# class ResourceList(Resource):
#
#     def get(self):
#         resources_html = "<html><body>" \
#                          "<h1>Resource list: </h1>" \
#                          "<ul><li><a href='/trafficLink'>Traffic links</a></li>" \
#                          "<li><a href='/trafficSpeed'>Traffic speed</a></li>""</ul>" \
#                          "</body></html>"
#         return output_html(resources_html, 200)
#
# api.add_resource(ResourceList, '/')

# @api.errorhandler(401)
# def validation_error(e):
#     # return bad_request(e.args[0])
#     return bad_request('Validation error.')
#
#
# @api.errorhandler(400)
# def bad_request_error(e):
#     return bad_request('invalid request')
#
#
# @api.errorhandler(404)
# def not_found_error(e):
#     return not_found('item not found')
#
# @app.errorhandler(429)
# def not_found_error(e):
#     return not_found('item not found')

@app.before_request
@auth.login_required
def before_request():
    pass
#
#
# @api.after_request
# def after_request(response):
#     if hasattr(g, 'headers'):
#         response.headers.extend(g.headers)
#     return response
#
# do this last to avoid circular dependencies
from speed_data import TrafficSpeedResource, TrafficSpeedListResource
from link_data import TrafficLinkResource, TrafficLinkListResource
#
# def output_html(data, code, headers=None):
#     resp = Response(data, mimetype='text/html', headers=headers)
#     resp.status_code = code
#     return resp
