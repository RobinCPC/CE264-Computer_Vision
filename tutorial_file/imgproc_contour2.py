import cv2
import numpy as np

im = cv2.imread('star.jpg')
img =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img, 127, 255, 0)
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cnt = contours[0]
M = cv2.moments(cnt)
print M

# Contour Area
area = cv2.contourArea(cnt)
# Contour Perimeter
perimeter = cv2.arcLength(cnt, True)

# Contour Approximation
epsilon = 0.0000001 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)

cv2.imshow('org', img)

img2 = im.copy()
cv2.drawContours(img2,cnt, -1, (100,255,0), 3)
cv2.imshow('img2', img2)

img3 = im.copy()
cv2.drawContours(img3, approx, -1, (100,255,0),3)
cv2.imshow('img3', img3)

