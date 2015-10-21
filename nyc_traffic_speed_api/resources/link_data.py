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


@api.route('/linkData/<int:id>')	
class LinkDataResource(Resource):

	def get(self, id):

		sensordata = db_conn.sensordata

		try:
			doc = sensordata.find({"linkId": str(id)}, { "_id":False, 
														"dataAsOf": True, 
														"linkName": True, 
														"borough": True, 
														"owner": True, 
														"linkPoints": True, 
														"encodedPolyLine": True, 
														"encodedPolyLineLvls": True}).sort("dataAsOf", -1).limit(1)
		
		except pymongo.errors, e:
			print "Unexpected error: ", e


		link_data = [link for link in doc]
		if len(link_data) == 0:
			abort(404)
		return jsonify({'linkData': link_data})


@api.route('/linkData')
class LinkDataListResource(Resource):

	def get(self):	

		sensordata = db_conn.sensordata

		try:
			documents = sensordata.aggregate([
			    								{"$sort": { "dataAsOf": -1 }},
			    								{"$group": { "_id": "$linkId", 
												        "dataAsOf": {"$first": "$dataAsOf"},
												        "linkName": {"$first": "$linkName" },
												        "borough":{"$first":"$borough"},
												        "owner": {"$first": "$owner"},
												        "linkPoints": {"$first": "$linkPoints"},
												        "encodedPolyLine": {"$first": "$encodedPolyLine"},
												        "encodedPolyLineLvls": {"$first": "$encodedPolyLineLvls"}
												    }}
												])
		except pymongo.errors, e:
			print "Unexpected error: ", e	


		links_list = [link for link in documents['result']]
		if len(links_list) == 0:
			abort(404)
		
		return jsonify({'linksList': links_list})
