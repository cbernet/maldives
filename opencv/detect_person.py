# import the necessary packages
import numpy as np
import cv2
from framecounter import FrameCounter

do_write = False
do_display = True
do_detection = True
# open webcam video stream
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('walking.mp4')

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

if do_write:
    # the output will be written to output.avi
    out = cv2.VideoWriter(
        'output.avi',
        cv2.VideoWriter_fourcc(*'MJPG'),
        15.,
        (640,480))

fcount = FrameCounter()

i=0
while(True):
    i+=1
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret is False:
        break

    fcount.start()

    if do_detection:
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

    if do_write:
        # Write the output video 
        out.write(frame.astype('uint8'))
        
    if do_display:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    fcount.stop()
    
    if i%10 == 0:
        print(fcount)
    
# When everything done, release the capture
cap.release()
# and release the output
if do_write: 
    out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
