import requests, csv, pymongo, sys, json, logging, re, pytz
import datetime
from flask import jsonify, abort
from bson import json_util
from common import send_email
from flask.ext.restful import Resource
from nyc_traffic_speed_api import api, db_conn, not_found_error
from . import Eastern

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

		sensors = db_conn.sensors
		links = db_conn.links
		
		try:
			doc = sensors.find({"sensorId": str(id)}, { 	"_id": False,
															'sensorId': True,
														   	"dataAsOf": True,
														   	"speed": True,
														   	"travelTime": True,
														   	"linkId": True
														   	}).sort("dataAsOf", -1).limit(1)
		
		except pymongo.errors, e:
			return "Unexpected error: ", e	

		EST = Eastern()
		speed_sensor = []
		for sensor in doc:
			try:
				l = links.find({"linkId": sensor["linkId"]}, {"linkName"})	
				sensor["linkName"] = l[0]["linkName"]
				sensor['dataAsOf'] = sensor['dataAsOf'].astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z')
				speed_sensor.append(sensor)
			except pymongo.errors, e:
				return "Unexpected error: ", e

		if len(speed_sensor) == 0:
			abort(404)
		return jsonify({'speedSensor': speed_sensor})


@api.route('/trafficSpeed/<int:id>/<string:date>')
class TrafficSpeedByDateResource(Resource):

	def get(self, id, date):

		if date is None:
			return jsonify({'test': "date parameter missing"})
		if not re.search("^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$",  date):
			abort(404)

		else:

			sensors = db_conn.sensors
			links = db_conn.links
			localtz = pytz.timezone('America/New_York')
			date = localtz.localize(datetime.datetime.strptime(date, "%Y-%m-%d"))
			end_date = date + datetime.timedelta(days=1)

			try:

				doc = sensors.aggregate(
						[
							{ 
								"$match": { "sensorId" : str(id), "dataAsOf": {"$gte": date, "$lt": end_date}  }
							},
							{
								"$group":
									{
										"_id": {"sensorId": "$sensorId", "linkId": "$linkId"},
										"measures": { "$push": {"timestamp": "$dataAsOf", "speed": "$speed", "travelTime": "$travelTime"}}

									}
							},
							{
								"$project":
									{
										"_id": 0,
										"sensorId": "$_id.sensorId",
										"linkId" : "$_id.linkId",
										"measures": 1
									}
							}
						]
					)


			except pymongo.errors, e:
				return "Unexpected error: ", e	

			EST = Eastern()
			speed_sensor = []
			for sensor in doc['result']:
				try:
					l = links.find({"linkId": sensor["linkId"]}, {"linkName"})	
					sensor["linkName"] = l[0]["linkName"]
					measures = sensor['measures']
					sensor['measures'] = []
					for m in measures:
						sensor['measures'].append({ 'timestamp': m['timestamp'].astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z'),
													'speed': m['speed'],
													'travelTime': m['travelTime'] 
												 })
					speed_sensor.append(sensor)
				except pymongo.errors, e:
					return "Unexpected error: ", e
			if len(speed_sensor) == 0:
				print "jazbec"
				abort(404)
			return jsonify({'speedSensor': speed_sensor})

@api.route('/trafficSpeed')	
class TrafficSpeedListResource(Resource):

	def get(self):

		sensors = db_conn.sensors
		links = db_conn.links

		try:
			documents = sensors.aggregate( [{"$sort": { "dataAsOf": -1 }},
											{"$group": { "_id": "$sensorId", 
											        "dataAsOf": {"$first": "$dataAsOf"},
											        "speed": {"$first": "$speed" },
											        "travelTime":{"$first":"$travelTime"},
											        "linkId": {"$first": "$linkId"}
											        # "borough": {"$first": "$borough"}
										    		}
								    		}
											], allowDiskUse = True)
		except pymongo.errors, e:
			print "Unexpected error: ", e	

		EST = Eastern()
		speed_sensors_list = []
		for point in documents['result']:
			point['dataAsOf'] = point['dataAsOf'].astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z')
			speed_sensors_list.append(point)	

		if len(speed_sensors_list) == 0:
			abort(404)
		
		return jsonify({'speedSensors': speed_sensors_list})


