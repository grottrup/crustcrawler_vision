#!/usr/bin/env python
import rospy
from crustcrawler_vision.msg import TrackedObject, TrackedObjectArray
from crustcrawler_vision.msg import Brick, BrickArray #temp
import message_filters

class ObjectTrackingNode():
    crustcrawler_base_width_cm = 11.5

	def __init__(self):
		#xy_sub = message_filters.Subscriber("/img_xy", Image_brick_data_array)
		#xz_sub = message_filters.Subscriber("/img_xz", Image_brick_data_array)
		#ts = message_filters.ApproximateTimeSynchronizer([xy_sub, xz_sub], 10, 0.1, allow_headerless = True)
		#ts.registerCallback(self.on_receive)
		self.publisher = rospy.Publisher("/objects", TrackedObjectArray, queue_size=1)
		xy_sub = rospy.Subscriber("/vision_topic", BrickArray, self.on_receive_temp) #temp

	#def on_receive(self, xy_brick_array, xz_brick_array):
		#for brick in range xy_brick_array.bricks:
		#	print(brick,brick.color,brick.x_pos,brick.y_pos, brick.height, brick.width)
		#for brick in range xz_brick_array.bricks:
		#	print(brick,brick.color,brick.x_pos,brick.y_pos, brick.height, brick.width)

		#calculate object
		#generate message
		#msg = Object_data_array()
		#data = Object_data()
		#for brick in range(len(bricks)):
			#fill data
		#msg.objects.append(data)
		
		#self.publisher.publish(msg)

	def on_receive_temp(self, in_msg):
		out_msg = TrackedObjectArray()
		blue_bricks = in_msg.blue_bricks
		for brick in blue_bricks:
			#print('x center: ', brick.x_center, 'y center: ', brick.y_center)	
			print('rot: ', brick.rotation_degrees)	
			data = TrackedObject()
			data.x_center = 10
			data.y_center = 20
			out_msg.blue_bricks.append(data)
		
		self.publisher.publish(out_msg)


if __name__ == '__main__':
	rospy.init_node("object_tracking")
	node = Object_tracking_node()
	rospy.spin()
