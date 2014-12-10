import time
from threading import Timer

def timeout_handler(timeout=10):
    print time.time()
    timer = Timer(timeout, timeout_handler)
    timer.start()

timeout_handler()
while True:
    print "loop"
    time.sleep(1)
