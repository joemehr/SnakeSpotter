from flask import Flask, request
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
        #Connect to database
        #connection = database.connect()
        #Perform query and return JSON data
        #query = connection.execute("SELECT s.description FROM Snake s WHERE")
        return {'description':SnakeTable.select(SnakeTable.c.species == species).execute().fetchone()[3]}

#class Departmental_Salary(Resource):
#    def get(self, department_name):
#        conn = e.connect()
#        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
#        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
restful_api.add_resource(Snake, '/snake/<string:species>')
if __name__ == '__main__':
     server.run()