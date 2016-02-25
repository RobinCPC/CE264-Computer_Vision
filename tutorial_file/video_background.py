'''
OpenCV Tutorial Video Analysis - Background Subtraction
'''

import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')

fgbg = cv2.BackgroundSubtractorMOG2(history=120, varThreshold=50, bShadowDetection=True)


while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

