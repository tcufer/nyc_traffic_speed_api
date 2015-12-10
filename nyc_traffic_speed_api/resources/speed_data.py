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

@api.route('/trafficSpeed/<int:id>')	
class TrafficSpeedResource(Resource):

	def get(self, id):

		# get a handle to the nyc_traffic_speed database
		# db=connection.nyc_traffic_speed
		sensors = db_conn.sensors
		links = db_conn.links
		try:
			doc = sensors.find({"sensorId": str(id)}, { 	"_id": False,
															'sensorId': True,
														   	"dataAsOf": True,
														   	"speed": True,
														   	"travelTime": True,
														   	"linkId": True
														   	# "borough": True
														   	}).sort("dataAsOf", -1).limit(1)
		
		except pymongo.errors, e:
			return "Unexpected error: ", e	
			# return status code
		# speed_sensor = [sensor for sensor in doc]
		speed_sensor = []
		for sensor in doc:
			try:
				l = links.find({"linkId": sensor["linkId"]}, {"linkName"})	
				sensor["linkName"] = l[0]["linkName"]
				speed_sensor.append(sensor)
			except pymongo.errors, e:
				return "Unexpected error: ", e

		if len(speed_sensor) == 0:
			abort(404)
		return jsonify({'speedSensor': speed_sensor})


@api.route('/trafficSpeed')	
class TrafficSpeedListResource(Resource):

	def get(self):

		# get a handle to the nyc_traffic_speed database
		# db=connection.nyc_traffic_speed
		sensors = db_conn.sensors
		links = db_conn.links

		try:
			documents = sensors.aggregate([
			    								{"$sort": { "dataAsOf": -1 }},
			    								{"$group": { "_id": "$sensorId", 
												        "dataAsOf": {"$first": "$dataAsOf"},
												        "speed": {"$first": "$speed" },
												        "travelTime":{"$first":"$travelTime"},
												        "linkId": {"$first": "$linkId"},
												        # "borough": {"$first": "$borough"}
												    }}
												])
		except pymongo.errors, e:
			print "Unexpected error: ", e	

		# try:
		# 	linkNames = links.find({},{"linkId", "linkName"})
		# except pymongo.errors, e:
		# 	print "Unexpected error: ", e	

		# link_names = dict()
		# for name in linkNames:
		# 	link_names[name["linkId"]] = name["linkName"]
		# 	# print "1" 

		speed_sensors_list = [point for point in documents['result']]
		
		# for point in documents['result']:
		# 	speed_sensors_list

		if len(speed_sensors_list) == 0:
			abort(404)
		
		return jsonify({'speedSensors': speed_sensors_list})

