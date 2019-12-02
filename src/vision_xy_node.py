#!/usr/bin/env python
import rospy
from crustcrawler_vision.msg import BrickArray, Brick
import vision_util as vision

class VisionNodeXY():
    def __init__(self):
        self.publisher = rospy.Publisher("/imgXY", BrickArray, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(0.1), self.onTimer)

    def onTimer(self, event):
        msg = BrickArray()
        dlink_video_jpg_url = 'http://192.168.0.20/image.jpg'
        img = vision.get_video_capture_frame(dlink_video_jpg_url)
        print(img.shape[1])
        self.publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node("visionXY")
    node = VisionNodeXY()
    rospy.spin()
