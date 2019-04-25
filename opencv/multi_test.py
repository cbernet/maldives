from multiprocessing import Process, Queue, Pool
import time
import random
from queue import PriorityQueue

def generate(inq):
    i = 0
    while 1:
        inq.put((i,i))
        i+=1

def times2(val):
    val *= 2
    time.sleep(max(0,random.gauss(0.5,0.2)))
    return val

def work(inq, outq, func):
    while 1:
        data = inq.get()
        val = func(data[1])
        outq.put(data)

def write(outq, write_function=None):
    if not write_function:
        write_function = print
    write_queue = PriorityQueue(500)
    before = time.time()
    lastval = -1
    while 1:
        now = time.time()
        dt = now - before
        if dt>0.1:
            data = outq.get()
            write_queue.put(data)
            data = write_queue.get()
            index, to_write = data
            if index == lastval+1:
                write_function(to_write)
                before = time.time()
                lastval = index
            else:
                time.sleep(0.01)
                write_queue.put(data)

def test_1():
    inq = Queue()
    outq = Queue()
    reader = Process(target=generate, args=(inq,))
    workers = []
    for i in range(8):
        worker = Process(target=work, args=(inq, outq, times2))
        workers.append(worker)
        worker.start()       
    writer = Process(target=write, args=(outq,))
    writer.start()
    reader.start()

    
class Processor(object):

    def __init__(self, nworkers,
                     read_function,
                     work_function,
                     write_function ):
        self.inq = Queue()
        self.outq = Queue()
        self.reader = Process(target=read_function, args=(self.inq,))
        self.workers = []
        for i in range(nworkers):
            worker = Process(target=work, args=(self.inq, self.outq, work_function))
            self.workers.append(worker)
            worker.start()       
        self.writer = Process(target=write, args=(self.outq, write_function))
        self.writer.start()
        self.reader.start()

def process(nworkers, read_function, work_function, write_function):
    inq = Queue()
    outq = Queue()
    reader = Process(target=read_function, args=(inq,))
    workers = []
    for i in range(nworkers):
        worker = Process(target=work, args=(inq, outq, work_function))
        workers.append(worker)
        worker.start()       
    writer = Process(target=write, args=(outq, write_function))
    writer.start()
    reader.start()    
        
def test_3():
    processor = Processor(8, generate, times2, print)

def test_4():
    process(8, generate, times2, print)
        
def test_2():
    with Pool(8) as p:
        queue = Queue()
        before = time.time()
        for res in p.imap(do_work, generate()):
            queue.put(res)
            now = time.time()
            if now - before>0.1:
                print(queue.get())
            else:
                time.sleep(0.01)
            
if __name__ == '__main__':
    test_3()
            
