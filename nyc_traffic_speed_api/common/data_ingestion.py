import requests, csv, pytz
from flask import abort
from datetime import datetime as dt
from models import Sensor, Link
from resources import app

def insert_traffic_data():

    localtz = pytz.timezone('America/New_York')
    # Read data from the website
    try:
        response = requests.get("http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt")
    except Exception as e:
        if not app.debug:
            import logger
            logger.logger_message("Retrieving data failed.")
        abort(500)

    # Split to lines
    trafficData = (response.text).split('\n')
    # skip first line (headers) and last line (empty); read lines
    # "Id"	"Speed"	"TravelTime"	"Status"	"DataAsOf"	"linkId"	"linkPoints"	"EncodedPolyLine"	"EncodedPolyLineLvls"	"Owner"	"Transcom_id"	"Borough"	"linkName"
    for line in csv.reader(trafficData[1:-1], delimiter="\t"):
            sensor = Sensor(sensorId = line[0],
                           speed = line[1],
                           travelTime = line[2],
                           status = line[3],
                           dataAsOf = localtz.localize(dt.strptime(line[4], "%m/%d/%Y %H:%M:%S")),
                           linkId = line[5])
            sensor.save()
            Link.objects(linkId = line[5]).upsert_one(
                    linkPoints = line[6],
                    encodedPolyLine = line[7],
                    encodedPolyLineLvls = line[8],
                    owner = line[9],
                    borough =  line[11],
                    linkName = line[12])

    return True

