import requests, csv, pymongo, sys, json, logging, pytz
from datetime import datetime as dt
from bson import json_util
from nyc_traffic_speed_api import app, db_conn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nyc_traffic_speed')
hdlr = logging.FileHandler('nyc_traffic_speed.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

	
class DataIngestion():

	def exception_handler(ex_message):
		logger.error(ex_message)


	def insert_traffic_data(self, response):

		sensors = db_conn.sensors

		localtz = pytz.timezone('America/New_York')
		trafficData = (response).split('\n')
		# skip first (headers) and last (empty) line		
		for line in csv.reader(trafficData[1:-1], delimiter="\t"): 
		# "Id"	"Speed"	"TravelTime"	"Status"	"DataAsOf"	"linkId"	"linkPoints"	"EncodedPolyLine"	"EncodedPolyLineLvls"	"Owner"	"Transcom_id"	"Borough"	"linkName"
			try:
				sensors.insert({	'sensorId': line[0], 
									'speed':line[1], 
									'travelTime':line[2], 
									'status':	line[3], 
									'dataAsOf': localtz.localize(dt.strptime(line[4], "%m/%d/%Y %H:%M:%S")),#dt.strptime(line[4], "%m/%d/%Y %H:%M:%S"), 
									'linkId': line[5] 
									# 'owner':line[9] 
									# 'linkPoints':line[6], 
									# 'encodedPolyLine':line[7], 
									# 'encodedPolyLineLvls':line[8],  
									# 'borough': line[11], 
									# 'linkName': line[12]
								})
			except pymongo.errors.WriteError as e:
				msg = "Error when inserting the document: %s ", e
				exception_handler(msg)



	def get_traffic_data(self):

		try:
			response = requests.get("http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt")
		except Exception as e:
			msg = 'An error occured: {} Status: {}'.format(e, 500)
			exception_handler(msg)
			return {'status': 500}

		if 400 <= response.status_code < 500:
			 # logger.error('An error occured, status: %s', response.status_code)
			msg = 'An error occured, status: {}'.format(response.status_code)
			exception_handler(msg)
			return {'status': response.status_code }

		logger.info('Data received, status: %s', response.status_code)
		self.insert_traffic_data(response.text)
		