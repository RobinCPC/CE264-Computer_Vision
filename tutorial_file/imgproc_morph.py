import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('j.png', 0 )
kernel = np.ones((5,5),np.uint8)
import pdb; pdb.set_trace()
erosion = cv2.erode(img, kernel, iterations= 1)
dilation = cv2.dilate(img, kernel, iterations = 1)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

images = [img, erosion, dilation, opening, 
        closing, gradient, tophat, blackhat]

titles = ['original', 'erosion', 'dilation', 'opening', 'closing', \
        'gradient', 'tophat', 'blackhat']


for i in xrange(8):
    plt.subplot(4,2,i+1), plt.imshow( images[i])
    plt.title(titles[i]), plt.xticks([]), plt.yticks([])

plt.show()
