#!/usr/bin/env python
import rospy
from crustcrawler_vision.msg import BrickArray, Brick
import vision_util as vision

class VisionNode():
    isCalibrated = False

    def __init__(self):
        self.publisher = rospy.Publisher("/vision_topic", BrickArray, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(1.0), self.onTimer)
        print('Starting Vision Node...')


    def onTimer(self, event):
        ret, frame = vision.get_video_capture_frame('http://192.168.1.103/image.jpg')
        if ret:
            cropped_frame = frame[75:frame.shape[0]-140, 35:frame.shape[1]-5]
            data = BrickArray()     
            blue_contours = vision.filter_blue_bricks(cropped_frame)
            red_contours = vision.filter_red_bricks(cropped_frame)

            if((self.isCalibrated is False)):
                ref_pixel_width = vision.init_get_ref_pixel_width(cropped_frame)
                rospy.set_param('ref_pixel_width', ref_pixel_width)
                print('Calibration value: {}'.format(ref_pixel_width))
                if ref_pixel_width is not 0:
                    self.isCalibrated = True
                    print('Is calibrated: {}'.format(self.isCalibrated))

            for contour in blue_contours:
                brick = Brick()
                brick.x_center = contour.x_center
                brick.y_center = contour.y_center
                brick.pixel_height = contour.pixel_height
                brick.pixel_width = contour.pixel_width
                brick.rotation_degrees = contour.rotation_degrees
                print('Blue brick\n    xy: {},{} | rotation:{} | width: {}'.format(brick.x_center, brick.y_center, brick.rotation_degrees, brick.pixel_width))
                data.blue_bricks.append(brick)
   
            for contour in red_contours:
                brick = Brick()
                brick.x_center = contour.x_center
                brick.y_center = contour.y_center
                brick.pixel_height = contour.pixel_height
                brick.pixel_width = contour.pixel_width
                brick.rotation_degrees = contour.rotation_degrees
                print('Red brick\n    xy: {},{} | rotation:{} | width: {}'.format(brick.x_center, brick.y_center, brick.rotation_degrees, brick.pixel_width))
                data.red_bricks.append(brick)
            
            msg = data
            self.publisher.publish(msg)
        


        

if __name__ == '__main__':
    rospy.init_node("vision")
    node = VisionNode()
    rospy.spin()
