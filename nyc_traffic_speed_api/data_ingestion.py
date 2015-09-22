import requests, csv, pymongo, sys, json
from datetime import datetime as dt
from bson import json_util

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

def get_traffic_data():

	try:
		response = requests.get("http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt")
	except Exception as e:
		print "An error occured:", type(e), e
		return {'status': 500}

	return {'status': response.status_code, 'trafficData': response.text}

def insert_traffic_data(response):

	# get a handle to the nyc_traficc_speed database
	db=connection.nyc_traffic_speed
	sensordata = db.sensordata

	trafficData = (response['trafficData']).split('\n')
	# skip first (headers) and last (empty) line		
	for line in csv.reader(trafficData[1:-1], delimiter="\t"): 
	# "Id"	"Speed"	"TravelTime"	"Status"	"DataAsOf"	"linkId"	"linkPoints"	"EncodedPolyLine"	"EncodedPolyLineLvls"	"Owner"	"Transcom_id"	"Borough"	"linkName"
		try:
			sensordata.insert({'sensorId': line[0], 
						'speed':line[1], 
						'travelTime':line[2], 
						'status':line[3], 
						'dataAsOf':dt.strptime(line[4], "%m/%d/%Y %H:%M:%S"), 
						'linkId': line[5], 
						'linkPoints':line[6], 
						'encodedPolyLine':line[7], 
						'encodedPolyLineLvls':line[8],  
						'owner':line[9], 
						'borough': line[11], 
						'linkName': line[12]})
		except Exception as e:
			print "Error when inserting the document:", type(e), e
			return 1

def current_traffic():
	
	# get a handle to the nyc_traficc_speed database
	db=connection.nyc_traffic_speed
	sensordata = db.sensordata

	try:
		documents = sensordata.aggregate([
		    								{"$sort": { "dataAsof": -1 }},
		    								{"$group": { "_id": "$sensorId", 
											        "dataAsOf": {"$first": "$dataAsof"},
											        "speed": {"$first": "$speed" },
											        "travelTime":{"$first":"$travelTime"},
											        "linkName": {"$first": "$linkName"},
											        "borough": {"$first": "$borough"}
											    }}
											])
	except Exception as e:
		print "Unexpected error: ", type(e), e	


	return documents['result']

# def get_link(id):
	# returns all data for link (geospatial data, owner, )


def delete_traffic_data():
	# establish connection to db
	db=connection.nyc_traffic_speed
	sensordata = db.sensordata

	try:
		result = sensordata.drop()
	except Exception as e:
		print "Connection error: ", type(e), e
		return 1

	return 0

