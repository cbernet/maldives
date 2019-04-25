# import the necessary packages
import numpy as np
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('people_side.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

scale = 2

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # scaling the picture down for faster detection
    small = cv2.resize(frame, (int(width/scale), int(height/scale)))
    small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(small, winStride=(4,4))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the original picture
        cv2.rectangle(frame, (xA*scale, yA*scale), (xB*scale, yB*scale),
                          (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
