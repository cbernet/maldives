import numpy as np
import cv2
import time
from multi_test_2 import process
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def read_video(inq):
    cap = cv2.VideoCapture(0)
    i = 0
    while 1:
        ret, frame = cap.read()
        inq.put((i,frame))
        i+=1

def bwthreshold(frame):
    print('processing')
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    ret,frame = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)
    return frame

def detect_people(frame):
    # resizing for faster detection
    # frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    return frame

cv2.startWindowThread()
nframes = 0
last = time.time()
for frame in process(6, read_video, detect_people):
    cv2.imshow('frame',frame)
    nframes += 1
    if nframes == 100:
        now = time.time()
        dt = now - last
        print(nframes/dt)
        last = now
        nframes = 0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break

# cap.release()
# cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
# cv2.waitKey(1)

