from flask import jsonify, current_app
from flask.ext.mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db = MongoEngine()

class Sensor(db.Document):
	sensorId = db.StringField()
	speed = db.StringField()
	travelTime = db.StringField()
	linkId = db.StringField()
	dataAsOf = db.DateTimeField()
	status = db.StringField()
	
	meta = {'collection': 'sensors'}


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
	username = db.StringField(max_length=64, required=True)
	password_hash = db.StringField(max_length=255, required=True)

	meta = {'collection': 'users'}

	# def __init__(self, *args, **kwargs):
	# 	# db.Document.__init__(self, *args, **kwargs)
    #
	# 	if 'password' in kwargs:
	# 		self.password = kwargs['password']

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_auth_token(self, expires_in=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
		return s.dumps({'id': 123}).decode('utf-8')

	# @staticmethod
	# def verify_auth_token(token):
	# 	s = Serializer(current_app.config['SECRET_KEY'])
	# 	try:
	# 		data = s.loads(token)
	# 	except:
	# 		return None
	# 	return User.objects.get(data['id'])