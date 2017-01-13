'''
Image Processing: rotating and Otsu's Binarization
'''


import sys
import argparse

import cv2
import numpy as np
from matplotlib import pyplot as plt


def parse_arg(argv):
    '''
    parsing cli arguments
    '''
    parser = argparse.ArgumentParser(description='image processing: rotation and binarization.')
    parser.add_argument('-i', '--inpf', default='IMG_0531-2.jpg', help='input image file')
    parser.add_argument('-r', '--rotate', type=float, default=0, help='the angle (deg) of rotation (CCW).')
    parser.add_argument('-b', '--binarize', type=int, default=0, help='method of binarize. 0->THRESH_BINARY, 1->THRESH_BINARY_INV')
    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    # pasring arguments
    args = parse_arg(sys.argv)

    try:
        inp = args.inpf     # 'IMG_0531-2.jpg'
        print inp
        img = cv2.imread(inp, 0)

        # === rotate image ===
        row, col = img.shape
        plt.imshow(img, 'gray')
        plt.show()
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        rot_ang = args.rotate
        M = cv2.getRotationMatrix2D((col/2, row/2), rot_ang, 1)   # (center, angle, scale)
        img_r = cv2.warpAffine(img, M, (col, row))

        # === smooth image ===
        blur = cv2.GaussianBlur(img_r, (5, 5), 0)    # (k_size, sigma_x)
        #blur = img

        # === binarize image ===
        bin_method = args.binarize
        # binarize method: THRESH_BINARY, THRESH_BINARY_INV, THRESH_OTSU
        if bin_method == 0:
            ret, th = cv2.threshold(blur, 5, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif bin_method == 1:
            ret, th = cv2.threshold(blur, 5, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        plt.imshow(th, 'gray')
        plt.show()
        cv2.imwrite(inp[0:-3]+'png', th)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    except:
        print 'no input file or not image type file'

    # return 0
