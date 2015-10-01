import requests, csv, pymongo, sys, json, logging
from datetime import datetime as dt
from bson import json_util
#from common import send_email
# from flask.ext.restful import Resource

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nyc_traffic_speed')
hdlr = logging.FileHandler('nyc_traffic_speed.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
# logger.setLevel(logging.WARNING)

	
class DataIngestion():

	def exception_handler(ex_message):
		logger.error(ex_message)

	def insert_traffic_data(self, response):

		# get a handle to the nyc_traficc_speed database
		db=connection.nyc_traffic_speed
		sensordata = db.sensordata

		trafficData = (response).split('\n')
		# skip first (headers) and last (empty) line		
		for line in csv.reader(trafficData[1:-1], delimiter="\t"): 
		# "Id"	"Speed"	"TravelTime"	"Status"	"DataAsOf"	"linkId"	"linkPoints"	"EncodedPolyLine"	"EncodedPolyLineLvls"	"Owner"	"Transcom_id"	"Borough"	"linkName"
			try:
				sensordata.insert({	'sensorId': line[0], 
									'speed':line[1], 
									'travelTime':line[2], 
									'status':	line[3], 
									'dataAsOf':dt.strptime(line[4], "%m/%d/%Y %H:%M:%S"), 
									'linkId': line[5], 
									'linkPoints':line[6], 
									'encodedPolyLine':line[7], 
									'encodedPolyLineLvls':line[8],  
									'owner':line[9], 
									'borough': line[11], 
									'linkName': line[12]})
			except Exception as e:
				# logger.error("Error when inserting the document: %s %s", type(e), e)
				msg = "Error when inserting the document: %s %s", type(e), e
				exception_handler(msg)
				return 1
		# return 0



	def get_traffic_data(self):

		try:
			response = requests.get("http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt")
		except Exception as e:
			msg = 'An error occured: {} Status: {}'.format(e, 500)
			exception_handler(msg)
			return {'status': 500}

		if 400 <= response.status_code <= 413:
			 # logger.error('An error occured, status: %s', response.status_code)
			 msg = 'An error occured, status: {}'.format(response.status_code)
			 exception_handler(msg)
			 return {'status': response.status_code }

		logger.info('Data received, status: %s', response.status_code)
		# return {'status': response.status_code, 'trafficData': response.text}
		tmp = self.insert_traffic_data(response.text)
		return tmp