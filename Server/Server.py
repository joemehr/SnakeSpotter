#Joseph Mehr
#Server.py exposes a RESTful API that can be used to
#access the sqlite database, SnakeSpotter.db

from flask import Flask, request, json
from flask_restful import Resource, Api
from sqlalchemy import *
from json import dumps

from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os

import NearestNeighbor
import pickle

database = create_engine('sqlite:///SnakeSpotter.db')

server = Flask(__name__)
restful_api = Api(server)
metadata = MetaData(database)
model = pickle.loads(open("model.pickle", "rb").read());

#Tables
SnakeTable = Table('Snake', metadata, autoload=True)
SightingTable = Table('Sighting', metadata, autoload=True)
UserTable = Table('User', metadata, autoload=True)

#Represents the snale table in the database
class Snake(Resource):

	#Access with a HTTP.GET request to URL/snake/<species>
	#Returns a description of that species from the database
    def get(self, species):
		row = SnakeTable.select(SnakeTable.c.species == species).execute().fetchone();
		return row[3];
		
#Represents the Sighting table in the database
class Sighting(Resource):

	#Access with a HTTP.POST request to URL/sighting/
	#Include a JSON body that has fields 'image', 'time', 
	#'location', 'species', and 'observer'
	#Returns the species name
	def post(self):
	#	if request.content_type != 'application/json':
	#		print "Wrong content type!"
	#		return {'content_type':request.content_type}
		print "Received a request"
		#sighting = json.loads(request.data)
		sighting = request.get_json(force=True)
		print sighting
		print sighting['image']
		image = cv2.imdecode(np.fromstring(sighting['image'].decode('base64'), np.uint8), cv2.IMREAD_COLOR)
		f = open('image.bmp','wb')
		f.write(sighting['image'].decode('base64'))
		f.close()
		#cv2.imshow('image', image);
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		
		SightingTable.insert().values({'image':sighting['image'], 'time':sighting['time'],'location':sighting['location'], 'species':sighting['species'], 'observer':sighting['observer']}).execute()
		print species[0]
		#return {'species':species[0]}
		return species[0]
		
#Represents the User table in the database
class User(Resource):
	
	#Adds a user to the database
	#Include a JSON body that contains the field 'name'
	def post(self):
		if request.content_type != 'application/json':
			return {'content_type':request.content_type}
		body = json.loads(request.data)
		print body['name']
		print UserTable.insert().values({'name':body['name']}).execute()
		return {}

#Links each class to a specific URL
restful_api.add_resource(Snake, '/snake/<string:species>')
restful_api.add_resource(Sighting, '/sighting/')
restful_api.add_resource(User, '/user/')



if __name__ == '__main__':
	server.run(host='0.0.0.0') #0.0.0.0 allows external API Access