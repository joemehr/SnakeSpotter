
import unittest
import Server

#Tests the methods that access the snake database
class TestSnakeMethods(unittest.TestCase):
	
	#Verifies that a snake description can be retrieved
	def testGet(self):
		snake = Server.Snake()
		description = snake.get("diamondback")
		assert description == 'The rattlesnake is known for its unique tail, which it shakes to produce a loud sound when threatened.'

if __name__ == '__main__':
	unittest.main()