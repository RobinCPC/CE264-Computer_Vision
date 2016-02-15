"""
OpenCV Tutorials Performance Measurement and Improvement Techniques
"""

import cv2
import numpy as np

img1 = cv2.imread('messi5.jpg')

e1 = cv2.getTickCount()
for i in xrange(5,49,2):
    img1 = cv2.medianBlur(img1, i)
e2 = cv2.getTickCount()
t = (e2-e1)/cv2.getTickFrequency()
print t

#%timeit res = cv2.medianBlur(img,49)   # can run in ipython mode

cv2.setUseOptimized(False)
#%timeit res = cv2.medianBlur(img,49)   # can run in ipython mode

cv2.setUseOptimized(True)


