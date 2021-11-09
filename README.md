Research Track 1 first assignment
================================

This first assignment is based on a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course.
The task for this assignment is to make the robot move counterclockwisely in the environment made of golden and silver boxes. The robot has to catch the silver tokens and let them behind itself and it has also to avoid the golden tokens, that forms the walls of the environment in which the robot moves.

* # **The robot**
    <img src="https://github.com/andreamanera/RTassignment1/blob/main/sr/robot.png">

* # **The silver token**
    <img src="https://github.com/andreamanera/RTassignment1/blob/main/sr/token_silver.png">

* # **The golden token**
    <img src="https://github.com/andreamanera/RTassignment1/blob/main/sr/token.png">

* # **The environment**
<img src="https://github.com/andreamanera/RTassignment1/blob/main/images/maze.png">

* # **The robot moving towards a silver token**
<img src="https://github.com/andreamanera/RTassignment1/blob/main/images/image1.png">

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).
If the dependencies are not installed you can install them using these commands:

```bash
$ sudo apt-get install python-dev python-pip python-pygame python-yaml
```

``` bash
$ sudo pip install pypybox2d
```

Once the dependencies are installed, get inside the directory on the shell, and then run the game using:

```bash
$ python2 run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

Functions
---------

I have implemented some functions to make the robot behave properly. Some of these are easy to understand while others need an explanation to correctly understand the behavior that I wanted the robot to have
while moving into the environment.

### drive() ###

the `drive()`  function was created to allow the robot to move straight, it can go forward, giving to `speed`parameter a positive value, or it can go backward giving to `speed` parameter a negative value

* Arguments 
  - `speed`, the linear velocity that we want the robot to assume.
  - `seconds`, the amount of seconds we want to drive.
* Returns
  - None.
* Code
```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```

### turn() ###

The `turn()` functions permits the robot to turn on itself.

* Arguments 
  - `speed`, the angular velocity that we want the robot to assume.
  - `seconds`, the amount of seconds we want the robot to turn.
* Returns
  - None.
* Code
```python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```

### find_silver_token() ###

The `find_silver_token()` function is used to find all the silver tokens around the robot. The robot can see the silver token thanks to the method `R.see()`. Since we want only silver tokens, we want to
have as `marker_type` `MARKER_TOKEN_SILVER`, thanks to this function we can consider only the silver tokens that are at a at a maximum distance of `3` from the robot and within the following angle
`-50°<\alpha<50°`, this is better understandable in the image below.

<p align="center">
<img src="https://github.com/andreamanera/RTassignment1/blob/main/images/findStoken.png">
</p>
                                                   
* Arguments 
  - None.
* Returns
  - `dist` distance of the closest silver token (-1 if no silver token is detected)
  - `rot_y` angle between the robot and the silver token (-1 if no silver token is detected)
* Code
```python
def find_silver_token():
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -50<token.rot_y<50:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y
```

### find_golden_token_front() ###

The `find_golden_token_front()` function is used to find the golden tokens in front of the robot so that it can avoid them, the mechanism is the same as seen for the function `find_silver_token()`, what
changes is the value of the parameters, first the `marker_type` is  `MARKER_TOKEN_GOLDEN` and also the angle change: `-35°<\alpha<35°`.

* Arguments 
  - None.
* Returns
  - `dist` distance of the closest golden token (-1 if no golden token is detected)
  - `rot_y` angle between the robot and the golden token (-1 if no golden token is detected)
* Code
```python
def find_golden_token_front():
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -35<token.rot_y<35:
            		dist=token.dist
            		rot_y=token.rot_y
   	 if dist==100:
		return -1, -1
    	else:
   		return dist, rot_y
```

### find_golden_token_left() ###

The `find_golden_token_left()` function, as the `find_golden_token_right()` function that will be commented on later, is necessary to find the distance between the robot and the wall to its left and so
decide if it needs to turn left or right. The mechanism is the same as before, but as we look for tokens to the left of the robot the angle chosen is: `-110°<\alpha<-70°`

* Arguments 
  - None.
* Returns
  - `dist` distance of the closest golden token on robot's left (-1 if no golden token is detected)
* Code
```python
def find_golden_token_left():
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -110<token.rot_y<-70:
            		dist=token.dist
            		rot_y=token.rot_y
   	 if dist==100:
		return -1
    	else:
   		return dist
```
### find_golden_token_right() ###

as mentioned above the function `find_golden_token_right()` is used for the same purpose as the function `find_golden_token_left()`, but since we are looking for token on robot's right the angle chosen is:
`70°<\alpha<110°`.

* Arguments 
  - None.
* Returns
  - `dist` distance of the closest golden token on robot's right (-1 if no golden token is detected)
* Code
```python
def find_golden_token_right():
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 70<token.rot_y<110:
            		dist=token.dist
            		rot_y=token.rot_y
   	 if dist==100:
		return -1
    	else:
   		return dist
```

### Grab() ###

the `Grab()` function contains the routine to move the robot after the token has been grabbed, after this the robot turns, drive for a short distance, leave the token and then it comes back to its original
position.

* Arguments 
  - None.
* Returns
  - None
* Code
```python
def Grab():
 	if R.grab():
            print("Gotcha!")
	    turn(30, 2)
	    drive(20,2)
	    R.release()
	    drive(-20,2)
	    turn(-30,2)
```

### adjust_position(dist_S, rot_S) ###

the `adjust_position(dist_S, rot_S)` function contains the routine to grab the token, if the robot is in the right position, and to move the robot in the correct position if it is in the wrong position to
grab the token.

* Arguments 
  - `dist_S` distance of the closest silver token
  - `rot_S` angle between the robot and the silver token
* Returns
  - None.
* Code
```python
def adjust_position(dist_S, rot_S):
	if dist_S < d_th:
		print("Found it!")
		Grab()
	elif -a_th<=rot_S<=a_th:
		drive(35, 0.2)
	    	print("Ah, that'll do.")
	elif rot_S < -a_th:
		print("Left a bit...")
		turn(-8, 0.2)
	elif rot_S > a_th:
		print("Right a bit...")
		turn(8, 0.2)
```

### avoid_walls(dist_left, dist_right) ###

the `avoid_walls(dist_left, dist_right)` function is necessary to check if the wall is closer to the right or to the left and then move the robot in the right way; if the robot is closer to the wall on the
left it turns right, if it is closer to the wall on the right it turn left.

* Arguments 
  - `dist_left` distance of the golden token on robot's left
  - `dist_right` distance of the golden token on robot's right
* Returns
  - None.
* Code
```python
def avoid_walls(dist_left, dist_right):

	if (dist_left > dist_right):
		print("Turn left a bit, there is a wall on the right at this distance:" + str(dist_right))
		turn(-20, 0.2)
			
	elif (dist_left < dist_right):
		print("Turn right a bit, there is a wall on the left at this distance:" + str(dist_left))
		turn(20,0.2)
			
	else:
		print("Similar distance from left and right golden token")
		print("Distance of the wall on the left:" + str(dist_left))
		print("Distance of the wall on the right:" + str(dist_right))
```

### main() ###

in the `main()` function are made all the controls necessary for the correct behavior of the robot in the environment.

First off all we need a `while` loop to make the robot move without stopping.

```python
def main():

	while 1:
```

After this we need to call all the functions to check the tokens position, thanks to the `while` these information are updated in every loop.

```python
		dist_S, rot_S=find_silver_token()
		dist_G, rot_G=find_golden_token_front()
		dist_left=find_golden_token_left()
		dist_right=find_golden_token_right()
```
Then is checked if the robot is close to a silver or to a golden token, if it isn't close to any token it moves straight.

```python
		if(dist_G>gold_th and dist_S>silver_th) or (dist_G>gold_th and dist_S==-1):
			print("I go straight")
			drive(100,0.05)
```

Tow if the robot is close to a silver token it tries to catch it. if the robot is close to a token but in the wrong position it adjusts its position in the environement calling the function adjust_position.

```python
		if(dist_S<silver_th and dist_S!=-1):
			adjust_position(dist_S, rot_S)
```

finally if the robot is close to a wall (golden token), he has to turn to avoid hitting it we make the robot turns using the function avoid_walls, previously discussed.

```python
		if(dist_G<gold_th and dist_G!=-1):
			avoid_walls(dist_left, dist_right)
```

**NOTE: all parameters in the code are selected, after several tests, to ensure the best possible behavior of the robot in the maze**

