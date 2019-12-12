#!/usr/bin/env python
"""
Created on Sun Nov 24 13:44:04 2019

@author: Marc Friis Torkelund
"""

import rospy
import actionlib
import arm_control
# from typing import NamedTuple
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryFeedback
from control_msgs.msg import FollowJointTrajectoryResult
from control_msgs.msg import FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from trajectory_msgs.msg import JointTrajectory
from au_crustcrawler_base.msg import Object_data_array, Arm_data, Arm_data_array
from au_crustcrawler_base.msg import TrackedObjectArray
from math import pi
from math import cos
from math import sin
from math import atan2
from math import sqrt

def temptShite():
    test1 = [30, 0, 0, 0, 3, 3, 'b']
    test2 = [30, 0, 0, 0, 6, 5, 'r']
    test3 = [30, 0, 0, 0, 5, 5, 'b']
    test4 = [30, 0, 0, 0, 3, 3, 'r']
    
    klodsListe = sampleBlock([test1, test2, test3, test4])

    print(klodsListe)

    pathen = []

    redHeight = 0

    blueHeight = 0

    for i in range(len(klodsListe)):
        if i % 2 == 0:
            pathen = pathen + goToBlock([klodsListe[i][0], klodsListe[i][1], klodsListe[i][2]])
            if klodsListe[i][6] == 'r':
                pathen = pathen + moveBlock([20,-25,redHeight])
                redHeight = redHeight + klodsListe[i][5]
            elif klodsListe[i][6] == 'b':
                pathen = pathen + moveBlock([20,25,blueHeight])
                blueHeight = blueHeight + klodsListe[i][5]
        else:
            pathen = pathen + goToBlock([klodsListe[i][0], klodsListe[i][1], klodsListe[i][2]])
            # pathen = pathen + moveBlock([20,-25,0+klodsListe[i-1][5]])
            if klodsListe[i][6] == 'r':
                pathen = pathen + moveBlock([20,-25,redHeight])
                redHeight = redHeight + klodsListe[i][5]
            elif klodsListe[i][6] == 'b':
                pathen = pathen + moveBlock([20,25,blueHeight])
                blueHeight = blueHeight + klodsListe[i][5]

    pathen = pathen + resetArm();

    return pathen



def sampleBlock(blockStructArray):
    blockOrder = []
#blockStructArray.count
    for j in range(2):
        largestWidth = 0
        previouslyUsedI = blockStructArray.count
        for i in range(len(blockStructArray)):
            if blockStructArray[i][4] > largestWidth:
                largestWidth = blockStructArray[i][4]
    
        
        for i in range(len(blockStructArray)):
            if blockStructArray[i][4] == largestWidth:
                blockOrder.append(blockStructArray[i])
                previouslyUsedI = i
                break
            
        for i in range(len(blockStructArray)):
            if i != previouslyUsedI:
                if blockStructArray[i][6] == blockStructArray[previouslyUsedI][6]:
                    blockOrder.append(blockStructArray[i])
                    if i < previouslyUsedI:
                        blockStructArray.pop(previouslyUsedI)
                        blockStructArray.pop(i)
    
                    elif previouslyUsedI < i:
                        blockStructArray.pop(i)
                        blockStructArray.pop(previouslyUsedI)
                    
    return blockOrder

def goToBlock(xyz):
    
    # if xyz[3] <= pi/2:
    #     nyVinkel = xyz[3]
    # elif xyz[3] > pi/2:
    #     nyVinkel = xyz[3]-pi
    
    # nyVinkel = nyVinkel-atan2(xyz[1], xyz[0])

    nyVinkel = 0

    path = [
            [xyz[0],xyz[1],15,nyVinkel,-pi/2],
            [xyz[0],xyz[1],xyz[2],nyVinkel,-pi/2],
            [xyz[0],xyz[1],xyz[2],nyVinkel,-pi/2],
            [xyz[0],xyz[1],xyz[2],nyVinkel,pi/4],
            [xyz[0],xyz[1],15,0,pi/4]
            ]
    return path

def moveBlock(xyz):
    path = [
            [xyz[0],xyz[1],15, 0,pi/4],
            [xyz[0],xyz[1],xyz[2],0,pi/4],
            [xyz[0],xyz[1],xyz[2],0,-pi/2],
            [xyz[0],xyz[1],15,0,-pi/2]
            ]
    return path

def resetArm():
    path = [[0,0,0,0,0]]
    return path

# class struct(NamedTuple):
#     x: float
#     y: int
#     z: int
#     rot: int
#     height: int
#     length: int
#     color: str

#Incoming parameters up to: X, Y, Z, Rotation, height, length, color
class behaviourNode:
#	print("In class")
	def __init__(self,server_name):
		self.publisher = rospy.Publisher("/arm_data", Arm_data_array, queue_size=1)
		rospy.Subscriber("/objects", TrackedObjectArray, self.on_receive_temp)
		#self.timer = rospy.Timer(rospy.Duration(0.1), self.on_timer)
		#self.send(20,20,10,3.14,1.3)
	        #test1 = struct(30, 0, 0, 0, 3, 3, 'b')
	        #test2 = struct(30, 0, 0, 0, 5, 5, 'b')
        
	        #klodsListe = sampleBlock([test1, test2])
        
	        #pathen = []
        
	        #for i in klodsListe:
	        #    if i % 2 == 0:
	        #        pathen = pathen + goToBlock(klodsListe[i].x, klodsListe[i].y, klodsListe[i].z)
	        #        pathen = pathen + moveBlock([20,-25,0])
	        #    else:
	        #        pathen = pathen + goToBlock(klodsListe[i].x, klodsListe[i].y, klodsListe[i].z)
	        #        pathen = pathen + moveBlock([20,-25,0+klodsListe[i-1].height])
                
	        #return pathen
        
# 		self.client = actionlib.SimpleActionClient(server_name, FollowJointTrajectoryAction)
        
#		print("Inside init")

	def on_receive(self, msg):
		objects = msg.objects
		for brick in objects:
			color = brick.color #string
			x = brick.x_pos #uint8
			y = brick.y_pos #uint8
			z = brick.z_pos #uint8
			w = brick.width #uint8
			h = brick.height #uint8
			r = brick.angle #float32
			#proccess object data
			print(brick)
		#self.send(x,y,z,r,w)

	def on_receive_temp(self, msg):
		objects = msg.blue_bricks
		for brick in objects:
			x = brick.x_center #uint8
			y = brick.y_center #uint8
			a = brick.cm_areal
			#proccess object data
			print(brick, "send", x, y, a)
		
	def on_timer(self, event):
		self.send(20,20,10,3.14,1.3)

	def send(self, x, y, z, r, g):
		print("send", x, y, z, r, g)
		msg = Arm_data_array()
		arm_data = Arm_data()
		arm_data.x = x
		arm_data.y = y
		arm_data.z = z
		arm_data.rotation = r
		arm_data.gripper = g
		msg.data_array.append(arm_data)
		self.publisher.publish(msg)

if __name__ == "__main__":
	print("In name?")
	rospy.init_node("behave")
	node= behaviourNode("/arm_controller/follow_joint_trajectory")
	rospy.spin()

# 	node.send_command()