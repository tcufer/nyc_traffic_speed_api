import requests, csv, pymongo, sys, json, logging
from flask import jsonify, abort, Response
from bson import json_util
from common import send_email
from flask.ext.restful import Resource
from nyc_traffic_speed_api import api, db_conn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nyc_traffic_speed')
hdlr = logging.FileHandler('nyc_traffic_speed.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
# logger.setLevel(logging.WARNING)

def output_html(data, code, headers=None):
    resp = Response(data, mimetype='text/html', headers=headers)
    resp.status_code = code
    return resp


@api.route('/')	
class ResourceList(Resource):

	def get(self):
		resources_html = "<html><body><h1>Resource list: </h1><ul><li><a href='/linkData/'>Traffic links</a></li><li><a href='/speedData/'>Traffic speed</a></li></ul></body></html>"
		return output_html(resources_html, 200)
