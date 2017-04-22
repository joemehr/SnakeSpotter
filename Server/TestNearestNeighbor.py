import unittest
import NearestNeighbor
import pickle
import Image
import cv2
import numpy as np

#Tests for all of the functions related to the K-Nearest Neighbors algorithm
class TestNearestNeighbor(unittest.TestCase):

	#Tests that feature vectors are properly generated
	def test_image_to_feature_vector(self):
		image = cv2.imread("diamondback.jpg")
		verificationFeatureVector = pickle.loads(open("testFeatureVector.pickle", "rb").read())
		testFeatureVector = NearestNeighbor.image_to_feature_vector(image)

		assert np.array_equal(verificationFeatureVector, testFeatureVector)
	
	#Tests that color histogram generation works
	def test_extract_color_histogram(self):
		image = cv2.imread("diamondback.jpg")
		verificationHistogram = pickle.loads(open("testHistogram.pickle", "rb").read())
		testHistogram = NearestNeighbor.extract_color_histogram(image)

		assert np.array_equal(verificationHistogram, testHistogram)
		
	#Tests that a diamondback can be correctly classified
	def test_classify_diamondback(self):
		model = pickle.loads(open("model.pickle", "rb").read())
		image = cv2.imread("diamondback.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		#print species[0]
		assert species[0] == 'diamondback'
		
	#Tests that a garter snake can be correctly classified
	def test_classify_garter(self):
		model = pickle.loads(open("model.pickle", "rb").read())
		image = cv2.imread("garter.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		#print species[0]
		assert species[0] == 'garter'
	
	#Tests that a coral snake can be correctly classified
	def test_classify_coral(self):
		model = pickle.loads(open("model.pickle", "rb").read())
		image = cv2.imread("coral.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		print species[0]
		assert species[0] == 'coral'
	
	#Verify that we are at minimum of 50% accuracy
	def test_train(self):
		accuracy = NearestNeighbor.train()
		assert accuracy > 50

if __name__ == '__main__':
	unittest.main()