# SnakeSpotter
Phone application that identifies snake species

The Snake Spotter is divided into two parts: the android application and the server.

The application allows users to take pictures of snakes, then send them to the server for identification.  The user can also query the server for additional information about a snake.

After receiving a snake picture, the server classifies it by using a K-Nearest Neighbors algorithm on a model that was trained on a set of 2300 images scraped from Google Images.  It then stores the sighting into a database and returns the snake's species name to the user.  If the user inquires about additional information, a brief description of the snake is returned from the database.
