import cv2

import imageio


im = imageio.imread('http://192.168.1.103/image.jpg')[:,:,::-1] #JPG to BGR

frame = im

if frame is None :
    print('No image')
print(frame.shape)
cv2.imshow('frame', frame)
if cv2.waitKey(1) != -1:
    cv2.destroyAllWindows()

#cap = cv2.VideoCapture('http://192.168.1.103/image.jpg')

#print(cap.isOpened)
#while cap.isOpened:
#    ret, frame = cap.read()
#    #if ret is False:
#    #    print('No video')
#    #    break
#    
#    if frame is None :
#        print('No image')
#        break
#    print(frame.shape)
#    cv2.imshow('frame', frame)
#    if cv2.waitKey(1) != -1:
#        cv2.destroyAllWindows()
#        break