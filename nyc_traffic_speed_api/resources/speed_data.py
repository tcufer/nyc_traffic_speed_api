import requests, csv, pymongo, sys, json, logging
from flask import jsonify
from datetime import datetime as dt
from bson import json_util
from common import send_email
from flask.ext.restful import Resource
from werkzeug import Response

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nyc_traffic_speed')
hdlr = logging.FileHandler('nyc_traffic_speed.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
# logger.setLevel(logging.WARNING)

	
class SpeedDataResource(Resource):

	def get(self, id):
		
		# get a handle to the nyc_traffic_speed database
		db=connection.nyc_traffic_speed
		sensordata = db.sensordata

		try:
			doc = sensordata.find({"sensorId": str(id)}, { 	"_id": False,
															'sensorId': True,
														   	"dataAsOf": True,
														   	"speed": True,
														   	"travelTime": True,
														   	"linkName": True,
														   	"borough": True}).sort("dataAsOf", -1).limit(1)
		
		except pymongo.errors, e:
			return "Unexpected error: ", e	
			# return status code
		resp = Response(json_util.dumps(doc), status=200, mimetype='application/json')
		return resp



class SpeedDataListResource(Resource):

	def get(self):

		# get a handle to the nyc_traffic_speed database
		db=connection.nyc_traffic_speed
		sensordata = db.sensordata

		try:
			documents = sensordata.aggregate([
			    								{"$sort": { "dataAsOf": -1 }},
			    								{"$group": { "_id": "$sensorId", 
												        "dataAsOf": {"$first": "$dataAsOf"},
												        "speed": {"$first": "$speed" },
												        "travelTime":{"$first":"$travelTime"},
												        "linkName": {"$first": "$linkName"},
												        "borough": {"$first": "$borough"}
												    }}
												])
		except pymongo.errors, e:
			print "Unexpected error: ", type(e), e	

		resp = Response(json_util.dumps(documents['result']), status=200, mimetype='application/json')
		return resp		