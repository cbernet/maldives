import cv2
img = cv2.imread('/Users/cbernet/Desktop/pandas.jpg')
cv2.startWindowThread()
cv2.imshow('image', img)
cv2.waitKey(10000) 
# << needed to display. 
# if key pressed, the program continues
# this only works if the image window is in focus
cv2.destroyAllWindows()
cv2.waitKey(1) # << needed to destroy 
