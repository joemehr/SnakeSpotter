#Joseph Mehr
#Back end for the Snake Spotter database

from flask import Flask, request, json
from flask_restful import Resource, Api
from sqlalchemy import *
from json import dumps

database = create_engine('sqlite:///SnakeSpotter.db')

server = Flask(__name__)
restful_api = Api(server)
metadata = MetaData(database)

#Tables
SnakeTable = Table('Snake', metadata, autoload=True)
SightingTable = Table('Sighting', metadata, autoload=True)
UserTable = Table('User', metadata, autoload=True)

class Snake(Resource):
    def get(self, species):
		row = SnakeTable.select(SnakeTable.c.species == species).execute().fetchone();
		return {'description':row[3]};
		
class Sighting(Resource):
	def post(self):
		if request.content_type != 'application/json':
			return {'content_type':request.content_type}
		sighting = json.loads(request.data)
		image = sighting['image']
		species = 'Python'  #ML stuff goes here
		SightingTable.insert().values({'image':sighting['image'], 'time':sighting['time'],'location':sighting['location'], 'species':sighting['species'], 'observer':sighting['observer']}).execute()
		return {'species':species}
		
class User(Resource):
	def post(self):
		if request.content_type != 'application/json':
			return {'content_type':request.content_type}
		body = json.loads(request.data)
		print body['name']
		print UserTable.insert().values({'name':body['name']}).execute()
		return {}

restful_api.add_resource(Snake, '/snake/<string:species>')
restful_api.add_resource(Sighting, '/sighting/')
restful_api.add_resource(User, '/user/')

if __name__ == '__main__':
     server.run()