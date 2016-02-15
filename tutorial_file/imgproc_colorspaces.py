"""
OpenCV Tutorial Image Processing - Changing ColorSpaces
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110, 100, 100])
    upper_blue = np.array([130, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([70, 255, 255])
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([20, 255, 255])

    # Threshold the HSV image to get only blue object
    mask_g = cv2.inRange(hsv, lower_green, upper_green)
    mask_r = cv2.inRange(hsv, lower_red, upper_red)
    mask_b = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res_g = cv2.bitwise_and(frame, frame, mask = mask_g)
    res_r = cv2.bitwise_and(frame, frame, mask = mask_r)
    res_b = cv2.bitwise_and(frame, frame, mask = mask_b)
    
    res = cv2.add(res_r, res_g)
    res = cv2.add(res, res_b)

    cv2.imshow('frame', frame)
    cv2.imshow( 'mask_r', mask_r)
    cv2.imshow( 'mask_g', mask_g)
    cv2.imshow( 'mask_b', mask_b)
    cv2.imshow( 'res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:                 #pres "ESC"
        break

cv2.destroyAllWindows()
    
