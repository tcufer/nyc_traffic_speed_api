#!flask/bin/python
from flask import Flask, jsonify
from flask.ext.restful import Api
from werkzeug import Response
from resources.speed_data import SpeedDataResource, SpeedDataListResource
from resources.link_data import LinkDataResource, LinkDataListResource
from common.data_ingestion import DataIngestion
from apscheduler.scheduler import Scheduler

app = Flask(__name__)
api = Api(app)


api.add_resource(SpeedDataResource, '/speedData/<int:id>', endpoint='speedData')
api.add_resource(SpeedDataListResource, '/speedData', endpoint='speedDataList')
api.add_resource(LinkDataResource, '/linkData/<int:id>', endpoint='linkData')
api.add_resource(LinkDataListResource, '/linkData', endpoint='linkDataAll')

		

# @app.before_first_request
# def initialize():
# 	apsched = Scheduler()
# 	apsched.start()

# 	data_ingestion = DataIngestion()
# 	apsched.add_interval_job(lambda: data_ingestion.get_traffic_data(), seconds=300)
	# response = data_ingestion.get_traffic_data()
	# if response['status'] == 200:
	# 	data_ingestion.insert_traffic_data(response)

if __name__ == '__main__':
    app.run(debug=True)