import cv2
import numpy as np
from matplotlib import pyplot as plt

BLUE = [255,0,0]
#import pdb; pdb.set_trace()
img1 = cv2.imread('opencv-logo.png')

replicate = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_REFLECT)
reflect_101 = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_WRAP)
constant = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_CONSTANT)
#transparent = cv2.copyMakeBorder(img1, 10, 10,10,10, cv2.BORDER_TRANSPARENT)

plt.subplot(231), plt.imshow(img1, 'gray'), plt.title('ORIGINAL')
plt.subplot(232), plt.imshow(replicate, 'gray'), plt.title('replicate')
plt.subplot(233), plt.imshow(reflect, 'gray'), plt.title('reflect')
plt.subplot(234), plt.imshow(reflect_101, 'gray'), plt.title('reflect_101')
plt.subplot(235), plt.imshow(wrap, 'gray'), plt.title('wrap')
plt.subplot(236), plt.imshow(constant, 'gray'), plt.title('constant')
#plt.subplot(337), plt.imshow(transparent, 'gray'), plt.title('trans')

plt.show()
