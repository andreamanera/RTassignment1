#IMPORTING LIBRARIES AND DEFINING SOME DATA FOR ROBOT CONTROL

from __future__ import print_function

import time
from sr.robot import *

# the parameters are chosen in order to optimize the behavior of the robot in the environement
a_th = 2.2
# float: Threshold for the control of the orientation
d_th = 0.4
# float: Threshold for the control of the linear distance
R = Robot()
# instance of the class Robot
gold_th=1.0
# float: Threshold for the control of robot's distance from the closest golden token 
silver_th=1.5
# float: Threshold for the control of robot's distance from the closest silver token
# I need this threshold to make the robot adjust his position before grabbing the token

################################################################################################################################

#DEFINING FUNCTION TO MAKE THE ROBOT MOVE

def drive(speed, seconds):

#    Function for setting a linear velocity
#    Args: speed (int): the speed of the wheels
#	  seconds (int): the time interval

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):

#    Function for setting an angular velocity
#    Args: speed (int): the speed of the wheels
#	  seconds (int): the time interval

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

################################################################################################################################

#DEFINING FUNCTION TO FIND SILVER AND GOLDEN TOKENS

def find_silver_token():

#   Function to find the closest silver token
#   Returns:
#	dist (float): distance of the closest silver token (-1 if no silver token is detected)
#	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)

    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -50<token.rot_y<50:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y
 
def find_golden_token_front():

#    Function to find the closest golden token in front of the robot
#    Returns:
#	dist (float): distance of the closest golden token in front of the robot (-1 if no golden token is detected)
#	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -35<token.rot_y<35:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token_left():

#   Function to find the closest golden token on the left of the robot
#   Returns:
#	dist (float): distance of the closest golden token on robot's left (-1 if no golden token is detected)

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -110<token.rot_y<-70:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

def find_golden_token_right():

#    Function to find the closest golden token on the right of the robot
#    Returns:
#	dist (float): distance of the closest golden token on robot's right (-1 if no golden token is detected)

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 70<token.rot_y<110:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
def Grab():
 	if R.grab():
            print("Gotcha!")
	    turn(30, 2)
	    drive(20,2)
	    R.release()
	    drive(-20,2)
	    turn(-30,2)
################################################################################################################################

#DEFINING THE FUNCTION TO ADJUST THE ROBOT POSITION WHEN A TOKEN IS SEEN

def adjust_position(dist_S, rot_S):

#    Function to adjust the position of the robot when we are close to a silver token
#    Args: dist_S (float): distance of the closest silver token
#	   rot_S (float): angle between the robot and the silver token
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
	    
################################################################################################################################

# DEFINING THE FUNCTION TO AVOID THE ROBOT HIT THE WALLS

def avoid_walls(dist_left, dist_right):

#    Function to avoid the walls when detected
#    Args: dist_left (float): distance of the closest golden token on robot's left
#	   dist_right (float): distance of the closest golden token on robot's right

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
	    
################################################################################################################################	    
	    
# DEFINING THE MAIN FUNCTION

# I decided to define a main function that will be called later, it is not mandatory but i decided to go in this way

def main():

# we need a while loop to make the robot move without stopping

	while 1:

# we need to update the information about tokens position in every loop	
		dist_S, rot_S=find_silver_token()
		dist_G, rot_G=find_golden_token_front()
		dist_left=find_golden_token_left()
		dist_right=find_golden_token_right()

# here we check if the robot is close to a silver or to a golden token, if it isn't close to any token we move straight
		
		if(dist_G>gold_th and dist_S>silver_th) or (dist_G>gold_th and dist_S==-1):
			print("I go straight")
			drive(100,0.05)

# if the robot is close to a silver token it tries to catch it. if the robot is close to a token but in the wrong position
# it adjusts its position in the environement using the function adjust_position
			
		if(dist_S<silver_th and dist_S!=-1):
			adjust_position(dist_S, rot_S)
			
# if the robot is close to a wall (golden token), he has to turn to avoid hitting it
# we make the robot turns using the function avoid_walls
# if it is close to a wall on the right it turns left
# if it is close to a wall on the left it turns right	
			
		if(dist_G<gold_th and dist_G!=-1):
			avoid_walls(dist_left, dist_right)
			
# MAIN CALL			
				
main()
