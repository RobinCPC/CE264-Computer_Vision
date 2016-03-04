'''
    OpenCV tutorial: Image processing: Contour 1
'''

import cv2
import numpy as np

im = cv2.imread('noisy2.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255,0)
_, contours, hierarchy = cv2.findContours( thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )

cv2.drawContours(im, contours, -1, (0,255,0), 3)
#cv2.drawContours(im, contours, 3, (0,255,0), 3)

#cnt = contours[4]
#cv2.drawContours( im, [cnt], 0, (0,255,0),3)

cv2.imshow('img', im)
