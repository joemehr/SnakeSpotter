#Joseph Mehr
#Back end for the Snake Spotter database

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

def image_to_feature_vector(image, size=(32,32)):
	return cv2.resize(image, size).flatten()

def extract_color_histogram(image, bins=(8, 8, 8)):
	# extract a 3D color histogram from the HSV color space using
	# the supplied number of `bins` per channel
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
		[0, 180, 0, 256, 0, 256])
 
	# handle normalizing the histogram if we are using OpenCV 2.4.X
	if imutils.is_cv2():
		hist = cv2.normalize(hist)
 
	# otherwise, perform "in place" normalization in OpenCV 3 (I
	# personally hate the way this is done
	else:
		cv2.normalize(hist, hist)
 
	# return the flattened histogram as the feature vector
	return hist.flatten()
	
def train():
	imageDir = "C:\Users\Joseph\Desktop\BID"
	
	garterImages = list(paths.list_images(imageDir+"/garter"))
	rattleImages = list(paths.list_images(imageDir+"/diamondback"))
	coralImages = list(paths.list_images(imageDir+"/coral"))
	# initialize the raw pixel intensities matrix, the features matrix,
	# and labels list
	rawImages = []
	features = []
	labels = []
	for (i, imagePath) in enumerate(garterImages):
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
		
		image = cv2.imread(imagePath)
		label = "gartersnake"
 
	# extract raw pixel intensity "features", followed by a color
	# histogram to characterize the color distribution of the pixels
	# in the image
		pixels = image_to_feature_vector(image)
		hist = extract_color_histogram(image)
 
	# update the raw images, features, and labels matricies,
	# respectively
		rawImages.append(pixels)
		features.append(hist)
		labels.append(label)
 
	# show an update every 1,000 images
		if i > 0 and i % 100 == 0:
			print("[INFO] processed {}/{}".format(i, len(garterImages)))
	for (i, imagePath) in enumerate(rattleImages):
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
		#print imagePath
		image = cv2.imread(imagePath)
		label = "rattlesnake"

	# extract raw pixel intensity "features", followed by a color
	# histogram to characterize the color distribution of the pixels
	# in the image
		pixels = image_to_feature_vector(image)
		hist = extract_color_histogram(image)
 
	# update the raw images, features, and labels matricies,
	# respectively
		rawImages.append(pixels)
		features.append(hist)
		labels.append(label)
 
	# show an update every 1,000 images
		if i > 0 and i % 100 == 0:
			print("[INFO] processed {}/{}".format(i, len(rattleImages)))
	
	for (i, imagePath) in enumerate(coralImages):
	# load the image and extract the class label (assuming that our
	# path as the format: /path/to/dataset/{class}.{image_num}.jpg
		print imagePath
		image = cv2.imread(imagePath)
		label = "coralsnake"
 
	# extract raw pixel intensity "features", followed by a color
	# histogram to characterize the color distribution of the pixels
	# in the image
		pixels = image_to_feature_vector(image)
		hist = extract_color_histogram(image)
 
	# update the raw images, features, and labels matricies,
	# respectively
		rawImages.append(pixels)
		features.append(hist)
		labels.append(label)
 
	# show an update every 1,000 images
		if i > 0 and i % 100 == 0:
			print("[INFO] processed {}/{}".format(i, len(coralImages)))
	(trainRI, testRI, trainRL, testRL) = train_test_split(rawImages, labels, test_size=0.25, random_state=42)
	(trainFeat, testFeat, trainLabels, testLabels) = train_test_split(features, labels, test_size=0.25, random_state=42)
	print("[INFO] evaluating raw pixel accuracy...")
	model = KNeighborsClassifier(n_neighbors=20,
	n_jobs=1)
	model.fit(trainRI, trainRL)
	acc = model.score(testRI, testRL)
	print("[INFO] histogram accuracy: {:.2f}%".format(acc * 100))
	print("[INFO] evaluating histogram accuracy...")
	model = KNeighborsClassifier(n_neighbors=20,
	n_jobs=1)
	model.fit(trainFeat, trainLabels)
	acc = model.score(testFeat, testLabels)

	print("[INFO] raw pixel accuracy: {:.2f}%".format(acc * 100))

if __name__ == '__main__':
	train()
	server.run()