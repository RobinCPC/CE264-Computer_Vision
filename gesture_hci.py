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


class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('gesture_hci')

        self.cmd_switch = False
        self.mask_lower_yrb = np.array([54, 131, 110])
        self.mask_upper_yrb = np.array([163, 157, 135])
        
        self.fgbg = cv2.BackgroundSubtractorMOG2(history=120, varThreshold=50, bShadowDetection=True)
    
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
            #fgmask = self.fgbg.apply(org_vis)
            #org_fg = cv2.bitwise_and(org_vis, org_vis, mask=fgmask)
            #hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            
            # Skin detect filter
            yrb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YCR_CB) 
            mask_skin = cv2.inRange(yrb, self.mask_lower_yrb, self.mask_upper_yrb)
            res_skin = cv2.bitwise_and( org_vis, org_vis, mask= mask_skin)
            
            fgmask = self.fgbg.apply(res_skin)
            org_fg = cv2.bitwise_and(res_skin, res_skin, mask=fgmask)

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

        cv2.destroyAllWindows()




if __name__ == '__main__':
    # main function start here
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()

