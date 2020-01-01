#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import imageio

class Brick:
    x_center = 0
    y_center = 0
    pixel_width = 0
    pixel_height = 0
    rotation_degrees = 0.0
    
'''
https://github.com/alexleavitt/uscplayspokemon/blob/master/tommycam.py
'''
def get_video_capture_frame(video_capture_url_jpg_str):
    img_request = imageio.imread(video_capture_url_jpg_str)[:,:,::-1] #JPG to BGR
    if (img_request is None) or (not img_request.shape):
        print('No image')
        return False, None
    return True, img_request

'''
https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
'''
def threshold_frame(img_frame, min_threshold):
    ret, thresholded_frame = cv2.threshold(img_frame, min_threshold, 255, cv2.THRESH_BINARY)
    return thresholded_frame


'''
https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed
'''
def remove_noise(img_frame):
    result = img_frame
    result = cv2.bilateralFilter(result,16,32,32) 
    
    kernel = np.ones((2, 2),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel) 
    
    kernel = np.ones((9, 9),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
   
    result = cv2.bilateralFilter(result,3,16,16)
    return result

'''
https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape????
'''
def blue_color_mask(img_frame):
    result = img_frame
    result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([50,50,80])
    upper_blue = np.array([140,255,255])
    result = cv2.inRange(result, lower_blue, upper_blue)

    ret, result = cv2.threshold(result, 50, 255, cv2.THRESH_BINARY)
    return result

def red_color_mask(img_frame):
    result = img_frame
    result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    lower_red = np.array([140,130,0])
    upper_red = np.array([255,255,255])
    result = cv2.inRange(result, lower_red, upper_red)

    ret, result = cv2.threshold(result, 50, 255, cv2.THRESH_BINARY)
    return result

def filter_blue_bricks(img_frame):
    frame = img_frame
    frame = blue_color_mask(frame)
    frame = remove_noise(frame)
    blue_brick_arr = find_bricks(frame) 
    return blue_brick_arr

def filter_red_bricks(img_frame):
    frame = img_frame
    frame = red_color_mask(frame)
    frame = remove_noise(frame)
    red_brick_arr = find_bricks(frame) 
    return red_brick_arr

def init_get_ref_pixel_width(img_frame):
    bricks = filter_blue_bricks(img_frame)
    if len(bricks) is 1:
        calibration_brick_pixel_width = bricks[0].pixel_width
        return calibration_brick_pixel_width
    return 0

def find_bricks(img_frame):
    frame = img_frame
    contours, hierarchy = cv2.findContours(frame.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    brick_arr = []
    for contour in contours:
        pixel_areal = cv2.contourArea(contour)
        if(pixel_areal > 600):
            brick = Brick()
            M = cv2.moments(contour)
            brick.x_center = int(M['m10']/M['m00'])
            brick.y_center = int(M['m01']/M['m00'])
            rectangle_w_rotation = cv2.minAreaRect(contour)
            brick.pixel_width = rectangle_w_rotation[1][0]
            brick.pixel_height = rectangle_w_rotation[1][1]
            brick.rotation_degrees = rectangle_w_rotation[2]
            brick_arr.append(brick)
    return brick_arr