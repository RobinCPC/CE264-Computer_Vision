import cv2
import numpy as np

def nothing(x):
    pass

# create mouse callback function
mode = False        # True if swith off (backgound in black)
drawing = False     
ix, iy = -1, -1
r,g,b = 0,0,0
radius = 0

def brush_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, r,g,b,radius

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True  # start to draw when L button down
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and mode == True:
            cv2.circle(img, (x,y), radius, (b, g, r), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False     # end drawing when L button up
        if mode == True:
            cv2.circle(img, (x,y), radius, (b, g, r), -1)



# Create a black image, a window
img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', brush_circle)

# create trackbar for color change
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

# create switch for ON/OFF for color change
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

# create trackbar for brush radius
brush = 'Brush Radius'
cv2.createTrackbar(brush, 'image', 0, 10, nothing)



while(1):
    #global r, g, b, radius
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current position of four trackbars
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    s = cv2.getTrackbarPos( switch, 'image')
    radius = cv2.getTrackbarPos( brush, 'image')

    if s == 0:
        if mode == False:   # user just change switch, make background to black
            mode = True     # and change to painting mode
            img[:] = 0
    else:
        mode = False
        img[:] = [b, g, r]

cv2.destroyAllWindows()


