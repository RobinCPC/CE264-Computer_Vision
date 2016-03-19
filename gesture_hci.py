'''
Hand gesture recognization
==========================

This is main function for the project.

Source Code:
https://github.com/RobinCPC/CE264-Computer_Vision

Usage:
------
    gesture_hci.py [<video source>] (default: 0)

Keys:
-----
    ESC     - exit
    c       - toggle mouse control (default: False)
    t       - toggle hand tracking (defualt: Fasle)
    s       - toggle skin calibration (need debug)

'''

import cv2
import numpy as np
import math
import time

# for controlling mouse and keyboard
import pyautogui
import sys

# Fail-safe mode (prevent from ou of control)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1 # pause each pyautogui function 0.1 sec


# BUild fixed-length Queue
class FixedQueue:
    '''
    A container with First-In-First-Out (FIFO) queuing policy
    But can only sotrage maximum number of items in container
    '''
    def __init__(self):
        self.list = []
        self.max_item = 5
        self.n_maj = 4

    def __str__(self):
        "Return list as string for printing"
        return str(self.list)

    def push(self, item):
        "Enqueue the item into the queue, but check length before add in"
        if self.list.__len__() == self.max_item:
            self.list.pop()
        self.list.insert(0, item)

    def pop(self):
        "Dequeue the earliest enqueued item still in the queue."
        return self.list.pop()

    def major(self):
        "Return the number that shows often in list"
        maj = 0
        count = 0
        for i in xrange(5):
            cur_cnt = self.list.count(i)
            if cur_cnt > count:
                maj = i
                count = cur_cnt
        return maj

    def count(self, value):
        "Return how many times that value show up in the queue"
        return self.list.count(value)

    def isEmpty(self):
        "Return true if the queue is empty"
        return len(self.list) == 0


# Dummy callback for trackbar
def nothing(x):
    pass

# uncomment if want to do on-line skin calibration
cv2.namedWindow('YRB_calib')
cv2.createTrackbar('Ymin', 'YRB_calib', 54, 255, nothing)
cv2.createTrackbar('Ymax', 'YRB_calib', 143, 255, nothing)
cv2.createTrackbar('CRmin', 'YRB_calib', 131, 255, nothing)
cv2.createTrackbar('CRmax', 'YRB_calib', 157, 255, nothing)
cv2.createTrackbar('CBmin', 'YRB_calib', 110, 255, nothing)
cv2.createTrackbar('CBmax', 'YRB_calib', 155, 255, nothing)

# Main part of gesture_hci
class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('gesture_hci')
        
        # set channel range of skin detection 
        self.mask_lower_yrb = np.array([44, 131, 80])       # [54, 131, 110]
        self.mask_upper_yrb = np.array([163, 157, 155])     # [163, 157, 135]
        # create trackbar for skin calibration
        self.calib_switch = False

        # create background subtractor 
        self.fgbg = cv2.BackgroundSubtractorMOG2(history=120, varThreshold=50, bShadowDetection=True)

        # define dynamic ROI area
        self.ROIx, self.ROIy = 200, 200
        self.track_switch = False
        # record previous positions of the centroid of ROI
        self.preCX = None
        self.preCY = None

        # A queue to record last couple gesture command
        self.last_cmds = FixedQueue()
        
        # prepare some data for detecting single-finger gesture  
        self.fin1 = cv2.imread('./test_data/index1.jpg')
        self.fin2 = cv2.imread('./test_data/index2.jpg')
        self.fin3 = cv2.imread('./test_data/index3.jpg')

        # swtich to turn on mouse input control
        self.cmd_switch = False
        
        # count loop (frame), for debuging 
        self.n_frame = 0


    # On-line Calibration for skin detection (bug, not stable)
    def skin_calib(self, raw_yrb):
        mask_skin = cv2.inRange(raw_yrb, self.mask_lower_yrb, self.mask_upper_yrb)
        cal_skin = cv2.bitwise_and(raw_yrb, raw_yrb, mask = mask_skin)
        cv2.imshow('YRB_calib', cal_skin)
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


	# Do skin dection with some filtering
    def skin_detect(self, raw_yrb, img_src):
        # use median bluring to remove signal noise in YCRCB domain
        raw_yrb = cv2.medianBlur(raw_yrb, 5)
        mask_skin = cv2.inRange(raw_yrb, self.mask_lower_yrb, self.mask_upper_yrb)

        # morphological transform to remove unwanted part
        kernel = np.ones( (5,5), np.uint8 )
        #mask_skin = cv2.morphologyEx(mask_skin, cv2.MORPH_OPEN, kernel)
        mask_skin = cv2.dilate(mask_skin, kernel, iterations=2)

        res_skin = cv2.bitwise_and( img_src, img_src, mask= mask_skin)
        #res_skin_dn = cv2.fastNlMeansDenoisingColored(res_skin, None, 10, 10, 7,21)

        return res_skin


	# Do background subtraction with some filtering
    def background_subtract(self, img_src):
        fgmask = self.fgbg.apply(cv2.GaussianBlur( img_src,(25,25),0 ))
        kernel = np.ones( (5,5), np.uint8 )
        fgmask = cv2.dilate(fgmask, kernel, iterations=2)
        #fgmask = self.fgbg.apply(cv2.medianBlur(img_src, 11))
        org_fg = cv2.bitwise_and(img_src, img_src, mask=fgmask)
        return org_fg

	# Update Position of ROI
    def update_ROI(self, img_src):
        # setting flexible ROI range
        Rxmin,Rymin,Rxmax,Rymax = (0,)*4
        if self.ROIx - 100 < 0:
            Rxmin = 0
        else:
            Rxmin = self.ROIx - 100
        
        if self.ROIx + 100 > img_src.shape[0]:
            Rxmax = img_src.shape[0]
        else:
            Rxmax = self.ROIx + 100
        
        if self.ROIy - 100 < 0:
            Rymin = 0
        else:
            Rymin = self.ROIy - 100
        
        if self.ROIy + 100 > img_src.shape[1]:
            Rymax = img_src.shape[1]
        else:
            Rymax = self.ROIy + 100
        
        return Rxmin,Rymin,Rxmax,Rymax


	# Find contour and track hand inside ROI
    def find_contour(self, img_src, Rxmin, Rymin, Rxmax, Rymax):
        cv2.rectangle(img_src, (Rxmax, Rymax), (Rxmin, Rymin), (0,255,0), 0)
        crop_res = img_src[Rymin: Rymax, Rxmin:Rxmax]
        grey = cv2.cvtColor(crop_res, cv2.COLOR_BGR2GRAY)

        _, thresh1 = cv2.threshold( grey, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        cv2.imshow('Thresh', thresh1)
        contours, hierchy = cv2.findContours( thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # draw countour on threshold image
        if len(contours) > 0:
            cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
            
        return contours, crop_res


	# Check ConvexHull  and Convextity Defects
    def get_defects(self, cnt, drawing):
        defects = None        
        hull = cv2.convexHull(cnt)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull( cnt, returnPoints = False)       # For finding defects
        if hull.size > 2:
            defects = cv2.convexityDefects(cnt, hull)        
        
        return defects


	# Gesture Recognization
    def gesture_recognize(self, cnt, defects, count_defects, crop_res):
        # use angle between start, end, decfect to recognize # of finger show up
        if not type(defects) == None and cv2.contourArea(cnt) >= 5000:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                angle = math.acos( (b**2 + c**2 - a**2)/(2*b*c) ) * 180/math.pi
                if angle <= 90:
                    count_defects += 1
                    cv2.circle( crop_res, far, 5, [0,0,255], -1)
                cv2.line(crop_res, start, end, [0,255,0], 2)
                
        ## single fingertip check
        if count_defects == 0 and cv2.contourArea(cnt) >= 5000:
            count_defects = self.single_finger_check(cnt)
        
        # return the result of gesture recognization
        return count_defects


	# Check if single-finger show up (OpenCV API using matchShape)
    def single_finger_check(self, cnt):
        # use single fingle image to check current fame has single finger
        grey_fin1 = cv2.cvtColor(self.fin1, cv2.COLOR_BGR2GRAY)
        _, thresh_fin1 = cv2.threshold(grey_fin1, 127, 255, 0)
        countour_fin1, hierarchy = cv2.findContours(thresh_fin1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt1 = countour_fin1[0]
        ret1 = cv2.matchShapes(cnt, cnt1, 1, 0)
        
        grey_fin2 = cv2.cvtColor(self.fin2, cv2.COLOR_BGR2GRAY)
        _, thresh_fin2 = cv2.threshold(grey_fin2, 127, 255, 0)
        countour_fin2, hierarchy = cv2.findContours(thresh_fin2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt2 = countour_fin2[0]
        ret2 = cv2.matchShapes(cnt, cnt2, 1, 0)
        
        grey_fin3 = cv2.cvtColor(self.fin3, cv2.COLOR_BGR2GRAY)
        _, thresh_fin3 = cv2.threshold(grey_fin3, 127, 255, 0)
        countour_fin3, hierarchy = cv2.findContours(thresh_fin3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt3 = countour_fin3[0]
        ret3 = cv2.matchShapes(cnt, cnt3, 1, 0)
        reta = (ret1 + ret2 + ret3)/3
        if reta <= 0.3:
            return 5        # set as one-finger module
        else:
            return 0        # not detect, still 0


	# Use PyAutoGUI to control mouse event
    def input_control(self, count_defects, img_src):
        # update position difference with prevous frame (for move mouse)        
        d_x, d_y = 0, 0
        if not self.preCX == None:
            d_x = self.ROIx - self.preCX
            d_y = self.ROIy - self.preCY
        
        # checking current command, and filter out unstable hand hesture
        cur_cmd = 0
        if self.cmd_switch:
            if self.last_cmds.count(count_defects) >= self.last_cmds.n_maj:
                cur_cmd = count_defects
                #print 'major command is ', cur_cmd
            else:
                cur_cmd = 0     # self.last_cmds.major()
        else:
            cur_cmd = count_defects
        
        # send mouse input event depend on hand gesture
        if cur_cmd == 1:
            str1 = '2, move mouse dx,dy = ' + str(d_x*3) + ', '+ str(d_y*3)
            cv2.putText(img_src, str1 , (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255),2)
            if self.cmd_switch:
                pyautogui.moveRel(d_x*3, d_y*3)
                self.last_cmds.push(count_defects)
                #pyautogui.mouseDown(button='left')
                #pyautogui.moveRel(d_x, d_y)
            #else:
            #    pyautogui.mouseUp(button='left')
        elif cur_cmd == 2:
            cv2.putText(img_src, '3 Left (rotate)', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 2)
            if self.cmd_switch:
                pyautogui.dragRel(d_x, d_y, button='left')
                self.last_cmds.push(count_defects)
                #pyautogui.scroll(d_y,pause=0.2) 
        elif cur_cmd == 3:
            cv2.putText(img_src, '4 middle (zoom)', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 2)
            if self.cmd_switch:
                pyautogui.dragRel(d_x, d_y, button='middle')
                self.last_cmds.push(count_defects)
        elif cur_cmd == 4:
            cv2.putText(img_src, '5 right (pan)', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 2)
            if self.cmd_switch:
                pyautogui.dragRel(d_x, d_y, button='right')
                self.last_cmds.push(count_defects)
        elif cur_cmd == 5:
            cv2.putText(img_src, '1 fingertip show up', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 2)
            if self.cmd_switch:
                self.last_cmds.push(count_defects)
        else:
            cv2.putText(img_src, 'No finger detect!', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 2)
            if self.cmd_switch:
                self.last_cmds.push(count_defects)  # no finger detect or wrong gesture


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

	# main function of the project (run all processes)
    def run(self):
        while self.cam.isOpened():
            if self.n_frame == 0:
                ini_time = time.time()
            ret, self.frame = self.cam.read()
            org_vis = self.frame.copy()
            #org_vis = cv2.fastNlMeansDenoisingColored(self.frame, None, 10,10,7,21) # try to denoise but time comsuming


            ### Skin detect filter
            yrb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2YCR_CB)
            res_skin = self.skin_detect( yrb, org_vis)


            ## check if want to do skin calibration
            if self.calib_switch:
                self.skin_calib(yrb)
            
            ### Background Subtraction
            org_fg = self.background_subtract(org_vis)
            

            ### Find Contours and track hand inside ROI
            Rxmin,Rymin,Rxmax,Rymax = self.update_ROI(org_fg)
            contours, crop_res =  self.find_contour(org_fg, Rxmin, Rymin, Rxmax, Rymax)

            ### Get Convexity Defects if Contour in ROI is bigger enough 
            drawing = np.zeros(crop_res.shape, np.uint8)
            max_area = -1
            ci = 0
            if len(contours) > 0:
                for i in range(len(contours)):
                    cnt = contours[i]
                    area = cv2.contourArea(cnt)
                    if area > max_area:
                        max_area = area
                        ci = i
                cnt = contours[ci]

                # use minimum rectangle to crop contour for faster gesture checking
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(crop_res, (x,y), (x+w, y+h), (0,0,255), 0 )

                # check if start to track hand
                if self.track_switch:
                    M = cv2.moments(cnt)
                    if not M['m00'] == 0:
                        self.ROIx = int(M['m10']/M['m00']) + Rxmin
                        self.ROIy = int(M['m01']/M['m00']) + Rymin - 30
                    else:
                        self.ROIx = 200
                        self.ROIy = 200

                # debug draw a  circle at center
                M = cv2.moments(cnt)
                if not M['m00'] == 0:
                    cx =  int(M['m10']/M['m00'])
                    cy =  int(M['m01']/M['m00'])
                    cv2.circle(org_fg, (cx+Rxmin,cy+Rymin), 10, [0,255,255],-1)
                
                ### Check ConvexHull  and Convextity Defects
                defects = self.get_defects(cnt, drawing)
                                

                ### Gesture Recognization
                count_defects = 0
                count_defects = self.gesture_recognize(cnt, defects, count_defects, crop_res)
                
                
                ### Input Control (Mouse Event)
                self.input_control(count_defects, org_fg)


                # update center position of ROI for next frame
                self.preCX = self.ROIx
                self.preCY = self.ROIy


            ### Display Image
            #cv2.imshow('original_view', org_vis)
            #cv2.imshow('YCR_CB', yrb)
            #cv2.imshow('YRB_skin', res_skin)
            #cv2.imshow('fgmask', fgmask)
            cv2.imshow('gesture_hci', org_fg)         # final result shows Here

            all_img = np.hstack((drawing, crop_res))
            cv2.imshow('Contours', all_img)

            #self.test_auto_gui()

            ch = cv2.waitKey(5) & 0xFF
            if ch == 27:
                break
            elif ch == ord('c'):
                self.cmd_switch = not self.cmd_switch
            elif ch == ord('s'):
                self.calib_switch = not self.calib_switch
            elif ch == ord('t'):
                self.track_switch = not self.track_switch

            if self.n_frame == 3:
                cur_time = time.time()
                #print 'time for one loop:',(cur_time - ini_time)
            self.n_frame = (self.n_frame + 1) % 4

        cv2.destroyAllWindows()




if __name__ == '__main__':
    # main function start here
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()

