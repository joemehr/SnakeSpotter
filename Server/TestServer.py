import flaskr
import unittest
import Server

#Tests the methods that access the snake database
class TestSnakeMethods(unittest.TestCase):
	
	#Verifies that a snake description can be retrieved
	def testGet(self):
		description = Server.Snake.get("diamondback")
		assert description == ""

if __name__ == '__main__':
	unittest.main()