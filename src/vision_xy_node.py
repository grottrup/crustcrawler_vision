#!/usr/bin/env python
import rospy
from crustcrawler_vision.msg import BrickArray, Brick
#import vision_utilitites as vision

class VisionNodeXY():
	def __init__(self):
		self.publisher = rospy.Publisher("/imgXY", BrickArray, queue_size=1)
		self.timer = rospy.Timer(rospy.Duration(0.1), self.onTimer)

	def onTimer(self, event):
    		msg = BrickArray()
    		print('hej')
    		self.publisher.publish(msg)

if __name__ == '__main__':
	rospy.init_node("visionXY")
	node = VisionNodeXY()
	rospy.spin()
