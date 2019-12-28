#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 12:12:13 2019

@author: grottrup
"""

import vision_util as vs
import cv2
i = 0
while i == 0:
    dlink_video_jpg_url = 'http://192.168.1.108/image.jpg'
    ret, img = vs.get_video_capture_frame(dlink_video_jpg_url)
    if ret:      
        cv2.imshow('orig', img)
        status = cv2.imwrite('~/catkin_ws/src/crustcrawler_vision/test1.jpg',img)
        print("Image written to file-system : ",status)
        #cropped_img = img[52:img.shape[0]-197, 80:img.shape[1]-80] # crop so it only shows table
        #img = cropped_img
        #cv2.imshow('im', img)
        
        #blue_bricks, blue_frame = vs.filter_blue_bricks(img)
        #cv2.imshow('blue', blue_frame)
    #    blue_bricks = filter_blue_bricks(cropped_img)
    #    cv2.imshow('blue', blue_bricks)       
        
        # red_bricks = filter_red_bricks(cropped_img)
        # cv2.imshow('red', red_bricks)
        
        #img2 = get_video_capture_frame(dlink_video_jpg_url2)
        #cv2.imshow('vid2', img2)
        i = 1
        if cv2.waitKey(1) != -1:
            cv2.destroyAllWindows()
            break
        
