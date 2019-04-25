import time

class FrameCounter(object):

    def __init__(self):
        self.sumdt = 0
        self.nframes = 0

    def start(self):
        self.now = time.time()
        self.tstart = self.now

    def stop(self):
        now = time.time()
        dt = now - self.tstart
        self.sumdt += dt
        self.nframes += 1

    def __str__(self):
        return '|FPS| = {:8.2f}'.format(self.nframes/self.sumdt)
        
