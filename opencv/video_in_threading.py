import concurrent.futures

import logging
import threading
import time
import queue
import random
import cv2


def reader(pipeline, event):
    """Pretend we're getting a number from the network."""
    cap = cv2.VideoCapture(0)
    while not event.is_set():
        time.sleep(0.05)
        ret, frame = cap.read()
        pipeline.put(frame)
        # print(pipeline.qsize())


def display(pipeline, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not pipeline.empty():
        print('display')
        frame = pipeline.get()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # breaking the loop if the user types q
            # note that the video window must be highlighted!
            break


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = queue.Queue()
    event = threading.Event()
    cv2.startWindowThread()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(reader, pipeline, event)
        # executor.submit(display, pipeline, event)
        print('here')
        while 1:
            time.sleep(0.05)
            if pipeline.empty():
                continue
            frame = pipeline.get()
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # breaking the loop if the user types q
                # note that the video window must be highlighted!
                break
            print('here', pipeline.qsize())

        
