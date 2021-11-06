#IMPORTING LIBRARIES AND DEFINING SOME DATA FOR ROBOT CONTROL

from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""
R = Robot()
""" instance of the class Robot"""
gold_th=1
""" float: Threshold for the control of robot's distance from the closest golden token """
silver_th=1
""" float: Threshold for the control of robot's distance from the closest silver token token, I define it to avoid robot from hitting the token without catching hit """

#DEFINING FUNCTION

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -60<token.rot_y<60:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
 
def find_golden_token_front():
    """
    Function to find the closest golden token in front of the robot
    Returns:
	dist (float): distance of the closest golden token in front of the robot (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -30<token.rot_y<30:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token_left():
    """
    Function to find the closest golden token on the left of the robot
    Returns:
	dist (float): distance of the closest golden token on robot's left (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -70<token.rot_y<-110:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

def find_golden_token_right():
    """
    Function to find the closest golden token on the right of the robot
    Returns:
	dist (float): distance of the closest golden token on robot's right (-1 if no golden token is detected)
    """
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
	    
#DEFINING THE MAIN FUNCTION
"""
I decided to define a main function that will be called later, it is not mandatory but i decided to go in this way
"""
def main():

# we need a while loop to make the robot move without stopping

	while 1:
	
		dist_S, rot_S=find_silver_token()
		dist_G, rot_G=find_golden_token_front()
		dist_left=find_golden_token_left()
		dist_right=find_golden_token_right()
		
		if(dist_G>gold_th and dist_S>d_th) or (dist_G>gold_th and dist_S==-1):
			print("I go straight")
			drive(10,0.5)
		elif(dist_G>gold_th and dist_S<d_th and dist_S!=-1):
			print("found it")
			if -a_th<= rot_S <= a_th:
				Grab()
			elif rot_S < -a_th:
				print("Left a bit")
				turn(-2,0.5)
			elif rot_S > a_th
				print("Right a bit")
				turn(2,0.5)
main()
