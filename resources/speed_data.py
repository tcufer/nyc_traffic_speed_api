import datetime
from datetime import datetime as dt

from flask.ext.restful import Resource

import pytz
import re
from common.helper import Eastern
from common.models import Sensor
from flask import jsonify, abort
from . import api

# timezone
EST = Eastern()

class TrafficSpeedResource(Resource):


    def get(self, id):

        req_fields = ['dataAsOf','sensorId', 'speed', 'travelTime', 'linkId']
        # sensor = Sensor.objects(sensorId = str(id)).order_by('-dataAsOf').limit(1).only(*req_fields)
        sensor = Sensor._get_collection().find({"sensorId" : str(id) },
                                               {"_id": 0, "dataAsOf":1, "sensorId": 1, "speed": 1, "travelTime": 1, "linkId": 1})\
                                        .sort("dataAsOf", -1)\
                                        .limit(1)
        sensor_list = []
        for s in sensor:
                s['dataAsOf'] = (s['dataAsOf'].replace(tzinfo=pytz.UTC)).astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z')
                sensor_list.append(s)


        if len(sensor_list) == 0:
            abort(404)

        return jsonify({'speedSensor': sensor_list})


class TrafficSpeedByDateResource(Resource):

    def get(self, id, date):

        if not re.search("^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$",  date):
            abort(404)
        else:
            localtz = pytz.timezone('America/New_York')
            date = localtz.localize(dt.strptime(date, "%Y-%m-%d"))
            end_date = date + datetime.timedelta(days=1)


            # sensors = Sensor.objects(sensorId = str(id), dataAsOf = )
            doc = Sensor._get_collection().aggregate(
                    [
                        {
                            "$match": { "sensorId" : str(id),
                                        "dataAsOf": { "$gte": date,
                                                      "$lt": end_date}  }
                        },
                        {
                            "$group":
                                {
                                    "_id": {"sensorId": "$sensorId",
                                            "linkId": "$linkId"},
                                    "measures": { "$push": {"timestamp": "$dataAsOf",
                                                            "speed": "$speed",
                                                            "travelTime": "$travelTime"}}

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



            speed_sensor = []
            for sensor in doc['result']:

                measures = sensor['measures']
                sensor['measures'] = []
                for m in measures:
                    sensor['measures'].append({ 'timestamp': (m['timestamp'].replace(tzinfo=pytz.UTC)).astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z'),
                                                'speed': m['speed'],
                                                'travelTime': m['travelTime']
                                             })
                speed_sensor.append(sensor)
            if len(speed_sensor) == 0:
                abort(404)
            return jsonify({'speedSensor': speed_sensor})


class TrafficSpeedListResource(Resource):

    def get(self):


        documents = Sensor._get_collection().aggregate( [{"$sort": { "dataAsOf": -1 }},
            {"$group": { "_id": "$sensorId",
            "dataAsOf": {"$first": "$dataAsOf"},
            "speed": {"$first": "$speed" },
            "travelTime":{"$first":"$travelTime"},
            "linkId": {"$first": "$linkId"}
            }
            }
            ], allowDiskUse = True)
        speed_sensors_list = []
        for point in documents['result']:
            point['dataAsOf'] = (point['dataAsOf'].replace(tzinfo=pytz.UTC)).astimezone(EST).strftime('%Y-%m-%d %H:%M:%S %Z')
            speed_sensors_list.append(point)


        if len(speed_sensors_list) == 0:
            abort(404)

        return jsonify({'speedSensor': speed_sensors_list})

    #
    # def post(self):
    #
    # 	localtz = pytz.timezone('America/New_York')
    # 	# Read data from the website
    # 	try:
    # 		response = requests.get("http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt")
    # 	except Exception as e:
    # 		abort(500)
    #
    # 	# Split to lines
    # 	trafficData = (response.text).split('\n')
    # 	# skip first line (headers) and last line (empty); read lines
    # 	# "Id"	"Speed"	"TravelTime"	"Status"	"DataAsOf"	"linkId"	"linkPoints"	"EncodedPolyLine"	"EncodedPolyLineLvls"	"Owner"	"Transcom_id"	"Borough"	"linkName"
    # 	for line in csv.reader(trafficData[1:-1], delimiter="\t"):
    # 		sensor = Sensor(sensorId = line[0],
    # 						speed = line[1],
    # 						travelTime = line[2],
    # 						status = line[3],
    # 						dataAsOf = localtz.localize(dt.strptime(line[4], "%m/%d/%Y %H:%M:%S")),
    # 						linkId = line[5])
    # 		sensor.save()
    #
    # 	return {}, 201



api.add_resource(TrafficSpeedListResource, '/trafficSpeed')
api.add_resource(TrafficSpeedResource, '/trafficSpeed/<int:id>')
api.add_resource(TrafficSpeedByDateResource, '/trafficSpeed/<int:id>/<string:date>')
