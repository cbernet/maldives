import numpy as np
import cv2

cv2.startWindowThread()
cap = cv2.VideoCapture(0)
person_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.resize(frame,(640,360)) # Downscale to improve frame rate
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    rects = person_cascade.detectMultiScale(gray_frame)
    
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
