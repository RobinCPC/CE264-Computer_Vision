'''
Image Processing: rotating and Otsu's Binarization
'''


import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    try:
        inp = sys.argv[1]     #'IMG_0531-2.jpg'
        print inp
        img = cv2.imread(inp, 0)

        # === rotate image ===
        row, col = img.shape
        plt.imshow(img, 'gray')
        plt.show()
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        M = cv2.getRotationMatrix2D((col/2, row/2), 0, 1)   # (center, angle, scale)
        img_r = cv2.warpAffine(img, M, (col, row))

        # === smooth image ===
        blur = cv2.GaussianBlur(img_r, (5,5), 0)    # (k_size, sigma_x)
        #blur = img

        # === binarize image ===
        ret, th = cv2.threshold(blur, 5, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # binarize method: THRESH_BINARY, THRESH_BINARY_INV, THRESH_OTSU
        plt.imshow(th, 'gray')
        plt.show()
        cv2.imwrite(inp[0:-3]+'png', th)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    except:
        print 'no input file'


        #return 0
