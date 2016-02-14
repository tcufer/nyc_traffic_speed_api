from flask import jsonify, abort
from flask.ext.restful import Resource
from flask.ext.mongoengine import MongoEngine
import requests, csv, pymongo, sys, json, logging, re, pytz
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from bson import json_util
# from nyc_traffic_speed_api import api, app
from nyc_traffic_speed_api import app, api

# from flask.ext.pymongo import PyMongo
# from resources import Eastern
# app.config['MONGODB_DB'] = 'dev_nyc_traffic_speed'
app.config['MONGODB_DB'] = 'dev_nyc_traffic_speed'
db = MongoEngine()
db.init_app(app)



class Sensor(db.Document):
	sensorId = db.StringField()
	speed = db.StringField()
	travelTime = db.StringField()
	linkId = db.StringField()
	dataAsOf = db.DateTimeField()
	status = db.StringField()
	
	meta = {'collection': 'sensors'}


	# def get_sensor_by_sensor_id(self, sensorId):
	# 	sensor = Sensor.objects(sensorId = self.sensorId) #get_or_404(sensorId = sensorId)
	# 	return jsonify({'speedSensor': sensor})


class Link(db.Document):
	linkId = db.StringField()
	linkName = db.StringField()
	borough = db.StringField()
	owner = db.StringField()
	linkPoints = db.StringField()
	encodedPolyLine = db.StringField()
	encodedPolyLineLvls = db.StringField()

	meta = {'collection': 'links'}


class User(db.Document):
	# id = db.Column(db.Integer, primary_key=True)
	username = db.StringField()
	password_hash = db.StringField()

	meta = {'collection': 'users'}

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_auth_token(self, expires_in=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
		return s.dumps({'id': self.id}).decode('utf-8')

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.objects.get(data['id'])