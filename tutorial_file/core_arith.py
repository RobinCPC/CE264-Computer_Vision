"""
OpenCV tutorials Core Operations: Arithmetic Operation on Images 
"""

import cv2
import numpy as np

def nothing(x):
    pass

# excersice: create track bar to smooth transition
cv2.namedWindow('dst')
cv2.createTrackbar('Alpha', 'dst', 0, 10, nothing)

img1 = cv2.imread('chicky_512.png')
img2 = cv2.imread('baboon.jpg')

'''
Image Blending
'''
while(1):
    alpha = cv2.getTrackbarPos('Alpha','dst')
    alpha /=10.
    #import pdb; pdb.set_trace()
    dst = cv2.addWeighted(img1, 1-alpha, img2, alpha, 0)
    
    cv2.imshow('dst', dst)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()

'''
Bitwise Operations
'''

# Load two images
img1 = cv2.imread('messi5.jpg')
img2 = cv2.imread('opencv_logo.png')

# I want to put logo on top-left corner, So I create a ROI
rows, cols, channels = img2.shape
roi = img1[0:rows,0:cols]

# Now creat e a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold( img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

# Now Black-out the area of logo in ROI
img1_bg = cv2.bitwise_and( roi, roi, mask=mask_inv)

# Take only region of logo from logo image.
img2_bg = cv2.bitwise_and( img2, img2, mask=mask)

# Put logo in ROI and mofidy the main image
dst = cv2.add(img1_bg, img2_bg)
img1[0:rows, 0:cols] = dst

cv2.imshow('res', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

