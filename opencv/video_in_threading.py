import concurrent.futures

import logging
import threading
import time
import queue
import random
import cv2
import numpy as np

from framecounter import FrameCounter

input_stream = 'walking.mp4'

def reader(pipeline, event):
    """Pretend we're getting a number from the network."""
    cap = cv2.VideoCapture(input_stream)
    while not event.is_set():
        time.sleep(0.05)
        ret, frame = cap.read()
        pipeline.put(frame)
        # print(pipeline.qsize())


def display(pipeline, event):
    """Pretend we're saving a number in the database."""
    fcount = FrameCounter()
    i=0
    while not event.is_set() or not pipeline.empty():
        i+=1
        fcount.start()
        frame = pipeline.get()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # breaking the loop if the user types q
            # note that the video window must be highlighted!
            break
        fcount.stop()
        if i%10 == 0:
            print(fcount)

def detect(pipeline, event):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    fcount = FrameCounter()
    i=0
    while not event.is_set() or not pipeline.empty():
        i+=1
        fcount.start()
        print('get')
        frame = pipeline.get()
        print('done')
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )        
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
        print('processed')
        fcount.stop()
        if i%10 == 0:
            print(fcount, pipeline.qsize())
       
        
            
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = queue.Queue()
    event = threading.Event()
#     cv2.startWindowThread()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.submit(reader, pipeline, event)
        executor.submit(detect, pipeline, event)
        # while 1:
        #     time.sleep(0.05)
        #     if pipeline.empty():
        #         continue
        #     frame = pipeline.get()
        #     cv2.imshow('frame',frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         # breaking the loop if the user types q
        #         # note that the video window must be highlighted!
        #         break
        #     print('here', pipeline.qsize())

        
