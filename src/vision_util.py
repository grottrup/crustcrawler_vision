#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

import cv2
import numpy as np
import imageio

class Brick:
    x_center = 0
    y_center = 0
    pixel_width = 0
    pixel_height = 0
    rotation_degrees = 0.0
    
class Crustcrawler:
    base_pixel_width = 0
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


def filter_max_rgb(img_frame):
    (B, G, R) = cv2.split(img_frame)
    M = np.maximum(np.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0
    result = cv2.merge([B, G, R])
    return result
'''
https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape????
'''
def blue_color_mask(img_frame):
    result = img_frame       
#    result = cv2.convertScaleAbs(result, alpha=1.95, beta=0) 
    result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([50,50,80])
    upper_blue = np.array([140,255,255])
    result = cv2.inRange(result, lower_blue, upper_blue)

    ret, result = cv2.threshold(result, 50, 255, cv2.THRESH_BINARY)
    return result

def filter_blue_bricks(img_frame):
    frame = img_frame
    frame = blue_color_mask(frame)
    frame = remove_noise(frame)
    blue_brick_arr = find_brick_centers(frame) 
    return blue_brick_arr

def filter_red_bricks(img_frame):
    result = img_frame
    # result = filter_excess_red_frame(img_frame)
    result = threshold_frame(result, 200)
    #result = remove_noise(result)
    result = find_brick_centers(result)    
    return result

def find_brick_centers(img_frame):
    frame = img_frame
    contours, hierarchy = cv2.findContours(frame.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    brick_arr = []
    for contour in contours:
        pixel_areal = cv2.contourArea(contour)
        if(pixel_areal > 1500):
            brick = Brick()
            M = cv2.moments(contour)
            brick.x_center = int(M['m10']/M['m00'])
            brick.y_center = int(M['m01']/M['m00'])
            rectangle_w_rotation = cv2.minAreaRect(contour)
            brick.pixel_width = rectangle_w_rotation[1][0]
            brick.pixel_height = rectangle_w_rotation[1][1]
            brick.rotation_degrees = rectangle_w_rotation[2]
            #box_points = cv2.cv.BoxPoints(rectangle_w_rotation)
            #print(rectangle_w_rotation)
            print(brick.rotation_degrees)
            #print(brick.pixel_width)
            #print(brick.pixel_height)
            brick_arr.append(brick)
            # frame = cv2.circle(frame,(cx, cy),10,(0,255,0))
            # cv2.imshow('blue', frame)
        elif(pixel_areal > 600):
            brick = Brick()
            M = cv2.moments(contour)
            brick.x_center = int(M['m10']/M['m00'])
            brick.y_center = int(M['m01']/M['m00'])
            brick_arr.append(brick)
            #result = cv2.circle(result,(cx, cy),5,(0,255,0))
    return brick_arr