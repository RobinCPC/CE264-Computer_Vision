import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWrite object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')  <-- this for 3.0
fourcc = cv2.cv.CV_FOURCC(*'XVID')          # for 2.4 ver
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

