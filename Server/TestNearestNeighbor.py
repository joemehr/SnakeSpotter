import flaskr
import unittest
import TestNearestNeighbor
import pickle
import Image

#Tests for all of the functions related to the K-Nearest Neighbors algorithm
class TestNearestNeighbor(unittest.TestCase):

	#Tests that feature vectors are properly generated
	def test_image_to_feature_vector():
		image = Image.open("garter.jpg");
		verificationFeatureVector = pickle.loads(open("testfv.pickle", "rb").read())
		testFeatureVector = NearestNeighbor.image_to_feature_vector(image)
		assert verificationFeatureVector == testFeatureVector
	
	#Tests that color histogram generation works
	def test_extract_color_histogram():
		image = Image.open("diamondback.jpg")
		verificationHistogram = pickle.loads(open("testfv.pickle", "rb").read())
		testHistogram = NearestNeighbor.extract_color_histogram(image)
		assert verificationFeatureVector == testFeatureVector
	
	#Tests that a diamondback can be correctly classified
	def test_classify_diamondback():
		model = pickle.loads(open("model.pickle", "rb").read())
		image = Image.open("diamondback.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		assert species = 'diamondback'
		
	#Tests that a garter snake can be correctly classified
	def test_classify_garter():
		model = pickle.loads(open("model.pickle", "rb").read())
		image = Image.open("garter.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		assert species = 'garter'
	
	#Tests that a coral snake can be correctly classified
	def test_classify_coral():
		model = pickle.loads(open("model.pickle", "rb").read())
		image = Image.open("coral.jpg")
		species = model.predict(NearestNeighbor.extract_color_histogram(image))
		assert species = 'coral'

if __name__ == '__main__':
	unittest.main()