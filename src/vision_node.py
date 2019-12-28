#!/usr/bin/env python
import rospy
from crustcrawler_vision.msg import BrickArray, Brick
import vision_util as vision

class VisionNode():
    def __init__(self):
        self.publisher = rospy.Publisher("/vision_topic", BrickArray, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(1.0), self.onTimer)
        print('Starting Vision Node...')


    def onTimer(self, event):
        ret, frame = vision.get_video_capture_frame('http://192.168.1.100/image.jpg')
        if ret:
            #print('image :)')
            #print(frame.shape)
            cropped_frame = frame[75:frame.shape[0]-140, 32:frame.shape[1]-2]
            blue_contours = vision.filter_blue_bricks(cropped_frame)


            data = BrickArray()
            for contour in blue_contours:
                brick = Brick()
                brick.x_center = contour.x_center
                brick.y_center = contour.y_center
                brick.rotation_degrees = contour.rotation_degrees
                data.blue_bricks.append(brick)
            msg = data
            self.publisher.publish(msg)
        


        

if __name__ == '__main__':
    rospy.init_node("vision")
    node = VisionNode()
    rospy.spin()
