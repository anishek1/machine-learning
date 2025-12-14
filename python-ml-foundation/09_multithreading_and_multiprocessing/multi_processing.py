##creation of processes that run in parallel
## why? CPU Bound Task that are heavy on CPU Usage
## want to use multiple core of the cpu

import multiprocessing
import time

def print_numbers():
    for num in range(5):
        time.sleep(1)
        print(f"Numbers:{num}")

def print_letters():
    for letter in "abcde":
        time.sleep(1)
        print(f"letters:{letter}")

if __name__=="__main__":

    ##create 2 process

    p1=multiprocessing.Process(target=print_numbers)
    p2=multiprocessing.Process(target=print_letters)
    t=time.time()
    ##start the process

    p1.start()
    p2.start()

    ##wait for process to complete 
    p1.join()
    p2.join()
    final_time=time.time()-t
    print(f"Final Time Taken:{final_time}")