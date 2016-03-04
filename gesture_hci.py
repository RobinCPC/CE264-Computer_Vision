'''
Hand gesture recognization
==========================

This is main function for the project.

Usage:
------
    gesture_hci.py [<video source>] (default: 0)

Keys:
-----
    ESC     - exit
    c       - toggle mouse control (default: False)

'''

import cv2
import numpy as np

# for controlling mouse and keyboard
import pyautogui
import sys

# Fail-safe mode (prevent from ou of control)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0 # pause each pyautogui function 1. sec

# Dummy callback for trackbar
def nothing(x):
    pass

### uncomment if want to do on-line skin calibration
cv2.namedWindow('YRB_calib')
cv2.createTrackbar( 'Ymin', 'YRB_calib', 54, 255, nothing)
cv2.createTrackbar( 'Ymax', 'YRB_calib', 143, 255, nothing)
cv2.createTrackbar( 'CRmin', 'YRB_calib', 131, 255, nothing)
cv2.createTrackbar( 'CRmax', 'YRB_calib', 157, 255, nothing)
cv2.createTrackbar( 'CBmin', 'YRB_calib', 110, 255, nothing)
cv2.createTrackbar( 'CBmax', 'YRB_calib', 155, 255, nothing)


class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('gesture_hci')

        self.cmd_switch = False
        self.mask_lower_yrb = np.array([54, 131, 110])      #[54, 131, 110]
        self.mask_upper_yrb = np.array([143, 157, 155])     #[163, 157, 135]
        
        self.fgbg = cv2.createBackgroundSubtractorKNN()
        #self.fgbg = cv2.BackgroundSubtractorMOG2(history=120, varThreshold=50, bShadowDetection=True)

        # create trackbar for skin calibration
        self.calib_switch = False
    

    # On-line Calibration for skin detection (bug, not stable)
    def skin_calib(self, raw_yrb):
        mask_skin = cv2.inRange(raw_yrb, self.mask_lower_yrb, self.mask_upper_yrb)
        cal_skin = cv2.bitwise_and( raw_yrb, raw_yrb, mask = mask_skin) 
        cv2.imshow('YRB_calib', cal_skin )
        k = cv2.waitKey(5) & 0xFF
        if k == ord('s'):
            self.calib_switch = False
            cv2.destroyWindow('YRB_calib')

        ymin = cv2.getTrackbarPos( 'Ymin', 'YRB_calib')
        ymax = cv2.getTrackbarPos( 'Ymax', 'YRB_calib')
        rmin = cv2.getTrackbarPos( 'CRmin', 'YRB_calib')
        rmax = cv2.getTrackbarPos( 'CRmax', 'YRB_calib')
        bmin = cv2.getTrackbarPos( 'CBmin', 'YRB_calib')
        bmax = cv2.getTrackbarPos( 'CBmax', 'YRB_calib')
        self.mask_lower_yrb = np.array([ymin, rmin, bmin])
        self.mask_upper_yrb = np.array([ymax, rmax, bmax])

    # Do skin dection and also some filtering
    def skin_detection(self, raw_yrb, org_vis):
        raw_yrb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YCR_CB)
        # use median bluring to remove signal noise in YCRCB domain
        raw_yrb = cv2.medianBlur(raw_yrb,5) 
        mask_skin = cv2.inRange(raw_yrb, self.mask_lower_yrb, self.mask_upper_yrb)

        # morphological transform to remove unwanted part
        kernel = np.ones( (5,5), np.uint8 )
        mask_skin = cv2.morphologyEx(mask_skin, cv2.MORPH_OPEN, kernel)

        res_skin = cv2.bitwise_and( org_vis, org_vis, mask= mask_skin)
        #res_skin_dn = cv2.fastNlMeansDenoisingColored(res_skin, None, 10, 10, 7,21)
        
        return res_skin


    # testing pyautogui
    def test_auto_gui(self):
        if self.cmd_switch:
            # Drag mouse to control some object on screen (such as googlemap at webpage)
            distance = 100.
            while distance > 0:
                pyautogui.dragRel(distance, 0, duration=2 , button='left')    # move right
                distance -= 25
                pyautogui.dragRel(0, distance, duration=2 , button='left')    # move down
                distance -= 25
                pyautogui.dragRel(-distance, 0, duration=2 , button='left')    # move right
                distance -= 25
                pyautogui.dragRel(0, -distance, duration=2 , button='left')    # move down
                distance -= 25

            # scroll mouse wheel (zoon in and zoom out googlemap)
            pyautogui.scroll(10, pause=1.)
            pyautogui.scroll(-10, pause=1)

            pyautogui.scroll(10, pause=1.)
            pyautogui.scroll(-10, pause=1)

            # message box
            pyautogui.alert(text='pyautogui testing over, click ok to end', title='Alert', button='OK')
            self.cmd_switch = not self.cmd_switch   # turn off 


    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            org_vis = self.frame.copy()
            #org_vis = cv2.fastNlMeansDenoisingColored(self.frame, None, 10,10,7,21) # try to denoise but time comsuming
            #fgmask = self.fgbg.apply(org_vis)
            #org_fg = cv2.bitwise_and(org_vis, org_vis, mask=fgmask)
            #hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            
            ### Skin detect filter
            yrb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YCR_CB)
            res_skin = self.skin_detection( yrb, org_vis)
            
            ## use median bluring to remove signal noise in YCRCB domain
            #yrb = cv2.medianBlur(yrb,5) 
            #mask_skin = cv2.inRange(yrb, self.mask_lower_yrb, self.mask_upper_yrb)

            ## morphological transform to remove unwanted part
            #kernel = np.ones( (5,5), np.uint8 )
            #mask_skin = cv2.morphologyEx(mask_skin, cv2.MORPH_OPEN, kernel)

            #res_skin = cv2.bitwise_and( org_vis, org_vis, mask= mask_skin)
            ##res_skin_dn = cv2.fastNlMeansDenoisingColored(res_skin, None, 10, 10, 7,21)

            ## check if want to do skin calibration
            if self.calib_switch:
                self.skin_calib(yrb)
            
            # Background Subtraction
            fgmask = self.fgbg.apply(res_skin)
            org_fg = cv2.bitwise_and(res_skin, res_skin, mask=fgmask)

            # Find Contours inside ROI
            cv2.rectangle(res_skin, (300, 300), (100, 100), (0,255,0), 0)
            crop_res = res_skin[100:300, 100:300]
            grey = cv2.cvtColor(crop_res, cv2.COLOR_BGR2GRAY)

            _, thresh1 = cv2.threshold( grey, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            cv2.imshow('Thresh', thresh1)
            _, contours, hierchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                    cv2.CHAIN_APPROX_NONE)

            max_area = -1
            ci = 0
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    ci = i
            cnt = contours[ci]
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(crop_res, (x,y), (x+w, y+h), (0,0,255), 0 )


            cv2.imshow('gesture_hci', org_vis)
            #cv2.imshow('HSV', hsv)
            #cv2.imshow('YCR_CB', yrb)
            cv2.imshow('YRB_skin', res_skin)
            cv2.imshow('fgmask', fgmask)
            cv2.imshow('org_fg', org_fg)

            self.test_auto_gui()

            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            elif ch == ord('c'):
                self.cmd_switch = not self.cmd_switch
            elif ch == ord('s'):
                self.calib_switch = not self.calib_switch

        cv2.destroyAllWindows()




if __name__ == '__main__':
    # main function start here
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()

