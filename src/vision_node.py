#!/usr/bin/env python
import rospy
#from std_msgs.msg import String
from crustcrawler_vision.msg import BrickArray, Brick
import vision_util as vision

class VisionNode():
    def __init__(self):
        #self.publisher = rospy.Publisher("/vision_topic", String, queue_size=1)
        self.publisher = rospy.Publisher("/vision_topic", BrickArray, queue_size=1)

        self.timer = rospy.Timer(rospy.Duration(1.1), self.onTimer)

    def onTimer(self, event):
        ret, frame = vision.get_video_capture_frame('http://192.168.1.101/image.jpg')
        if ret:
            print('image :)')
            print(frame.shape)
            cropped_frame = frame[42:frame.shape[0]-80, 0:frame.shape[1]]
            blue_contours = vision.filter_blue_bricks(cropped_frame)


            data = BrickArray()
            for contour in blue_contours:
                brick = Brick()
                brick.pixel_areal = contour.pixel_areal
                brick.x_center = contour.x_center
                brick.y_center = contour.y_center
                data.blue_bricks.append(brick)
            msg = data
            self.publisher.publish(msg)
        


        

if __name__ == '__main__':
    rospy.init_node("vision")
    node = VisionNode()
    rospy.spin()
