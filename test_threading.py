
from threading import Thread, RLock
from random import randint
import time
import numpy as np
from tqdm import tqdm

lock = RLock()

def compute_part(number, from_to, array, d):

    # Sleeps a random 1 to 10 second
    t0 = time.time()
    # sleep(rand_int_var)

    for idx_b in range(from_to[1], from_to[0],-1):
        with lock:
            d[array[idx_b]] = np.sqrt(time.time())

    print ("Thread " + str(number) + " slept for " +str(time.time()-t0) + " seconds", from_to)

thread_list = []
array = np.arange(0,12345678)
total_lenght = array.shape[0]

num_of_proc = 6
steps_1 = np.arange(0, total_lenght,total_lenght//num_of_proc)
steps = []
for idx in range(len(steps_1)-1):

    if idx == len(steps_1) -2:
        _to = total_lenght-1
    else:
        _to = steps_1[idx+1]
    _from = steps_1[idx]
    steps.append((_from, _to))


print(steps)
#
d = {}
for number, from_to in enumerate(steps):

    # Instantiates the thread
    # (i) does not make a sequence, so (i,)

    t = Thread(target=compute_part, args=(number+1, from_to,array,d))
    # Sticks the thread in a list so that it remains accessible
    thread_list.append(t)

# Starts threads
for thread in thread_list:
    thread.start()

# This blocks the calling thread until the thread whose join() method is called is terminated.
# From http://docs.python.org/2/library/threading.html#thread-objects
for thread in thread_list:
    thread.join()

# Demonstrates that the main process waited for threads to complete

# [print(dd, dv) for dd, dv in d.items()]
print ("Done")