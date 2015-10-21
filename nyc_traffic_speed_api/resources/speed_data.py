import requests, csv, pymongo, sys, json, logging
from flask import jsonify, abort
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

@api.route('/speedData/<int:id>')	
class SpeedSensorResource(Resource):

	def get(self, id):

		# get a handle to the nyc_traffic_speed database
		# db=connection.nyc_traffic_speed
		sensordata = db_conn.sensordata

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
		speed_sensor = [sensor for sensor in doc]
		if len(speed_sensor) == 0:
			abort(404)
		return jsonify({'speedSensor': speed_sensor})


@api.route('/speedData')	
class SpeedSensorsListResource(Resource):

	def get(self):

		# get a handle to the nyc_traffic_speed database
		# db=connection.nyc_traffic_speed
		sensordata = db_conn.sensordata

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
			print "Unexpected error: ", e	

		speed_sensors_list = [point for point in documents['result']]
		if len(speed_sensors_list) == 0:
			abort(404)
		
		return jsonify({'speedSensors': speed_sensors_list})

