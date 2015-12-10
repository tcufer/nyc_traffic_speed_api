import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, make_response, jsonify
from flask.ext.restful import Api
from werkzeug import Response
from resources.speed_data import TrafficSpeedResource, TrafficSpeedListResource
from resources.link_data import TrafficLinkResource, TrafficLinkListResource
from common.data_ingestion import DataIngestion
from apscheduler.scheduler import Scheduler
from nyc_traffic_speed_api import app, api

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.before_first_request
def initialize():
	data_ingestion = DataIngestion()
	data_ingestion.get_traffic_data()

	apsched = Scheduler()
	apsched.start()
	# Retrieve traffic data every 5 min
	apsched.add_interval_job(lambda: data_ingestion.get_traffic_data(), seconds=300)
	
if __name__ == '__main__':
    app.run(debug=True)