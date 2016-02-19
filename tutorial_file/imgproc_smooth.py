import cv2
import numpy as np
from matplotlib import pyplot as plt

''' 2D convolution (image filter)
img =cv2.imread('opencv_logo_L.png')

kernel = np.ones((5,5), np.float32)/25
dst = cv2.filter2D(img, -1, kernel)

plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(dst), plt.title('Average')
plt.xticks([]), plt.yticks([])

plt.show()
'''

img = cv2.imread('opencv_logo_L.png')

#blur = cv2.blur(img,(5,5))
#blur = cv2.GaussianBlur(img,(5,5), 0)
blur = cv2.medianBlur(img, 5)

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur),plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()


