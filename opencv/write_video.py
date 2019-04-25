import cv2
import numpy as np

writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))

for frame in range(1000):
    writer.write(np.random.randint(0, 255, (480,640,3)).astype('uint8'))

writer.release()
