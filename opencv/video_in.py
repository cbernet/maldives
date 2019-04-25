import numpy as np
import cv2
import time
from framecounter import FrameCounter

fcount = FrameCounter()

cv2.startWindowThread()
cap = cv2.VideoCapture('walking.mp4')

i = 0
while(True):
    i+=1
    ret, frame = cap.read()

    fcount.start()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    ret,frame = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)
    
    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    # breaking the loop if the user types q
    #    # note that the video window must be highlighted!
    #    break
    fcount.stop()
    
    if i%10==0:
        print(fcount)

cap.release()
# cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
# cv2.waitKey(1)

