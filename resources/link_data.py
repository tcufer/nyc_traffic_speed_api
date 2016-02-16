from flask.ext.restful import Resource

from common.models import Link
from flask import jsonify, abort
from . import api


class TrafficLinkResource(Resource):

	def get(self, id):

		req_fields = ['linkId','linkName', 'borough', 'owner', 'linkPoints', 'encodedPolyLine', 'encodedPolyLineLvls']
		link = Link.objects(linkId = str(id)).only(*req_fields)
		if len(link) == 0:
			abort(404)	
		return jsonify({'Link': link})



class TrafficLinkListResource(Resource):

	def get(self):	
		
		req_fields = ['linkId', 'linkName', 'borough', 'owner', 'linkPoints', 'encodedPolyLine', 'encodedPolyLineLvls']
		links = Link.objects().only(*req_fields)
		if len(links) == 0:
			abort(404)
		
		return jsonify({'trafficLinkList': links})


	# def post(self):
    #
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
	# 		link = Link(linkId = line[5],
	# 						linkPoints = line[6],
	# 						encodedPolyLine = line[7],
	# 						encodedPolyLineLvls = line[8],
	# 						owner = line[9],
	# 						borough =  line[11],
	# 						linkName = line[12])
	# 		link.save()
	#
	# 	return {}, 201


api.add_resource(TrafficLinkResource, '/trafficLink/<int:id>')
api.add_resource(TrafficLinkListResource, '/trafficLink/')
