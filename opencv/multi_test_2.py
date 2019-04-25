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
        try:
            data = inq.get(False)
            result = func(data[1])
            outq.put((data[0], result))
        except:
            outq.put(None)

def process(nworkers, read_function, work_function):
    nq = 50
    inq = Queue(nq)
    outq = Queue(nq)
    reader = Process(target=read_function, args=(inq,))
    workers = []
    for i in range(nworkers):
        worker = Process(target=work, args=(inq, outq, work_function))
        workers.append(worker)
        worker.start()       
    reader.start()
    # while 1:
    #     yield outq.get()[1]
    write_queue = PriorityQueue(100)
    before = time.time()
    lastval = -1
    while 1:
        now = time.time()
        dt = now - before
        if dt>0.0:
            data = outq.get()
            if data:
                write_queue.put(data)
                data = write_queue.get()
                index, to_write = data
                # yield to_write
                if index == lastval+1:
                    yield to_write
                    before = time.time()
                    lastval = index
                else:
                    time.sleep(0.001)
                    write_queue.put(data)
        
def test_1():
    for i in process(4, generate, times2):
        print(i)
        
if __name__ == '__main__':
    test_1()
            
