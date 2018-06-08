#!bin/python3

import sys
from threading import Thread, Lock
import numpy as np

def tradition(mat1, mat2):
    res = np.zeros((mat1.shape[0], mat2.shape[1]))

    threads = list()
    thread_lock = Lock()

    def calculate(r, c):
        tmp = float(0)

        for i in range(mat1.shape[1]):
            tmp += mat1[r, i] * mat2[i, c]

        thread_lock.acquire()
        res[r, c] = tmp
        thread_lock.release()

    for r in range(mat1.shape[0]):
        for c in range(mat2.shape[1]):
            thread = Thread(target=calculate, args=(r, c))
            thread.start()
            threads.append(thread)

    for t in threads:
        t.join()

    return res

def main():
    for line in sys.stdin:
        mat1 = np.zeros([int(s) for s in line.split()])

        for r in range(mat1.shape[0]):
            mat1[r] = np.array([float(s) for s in input().split()])

        mat2 = np.zeros([int(s) for s in input().split()])

        for r in range(mat2.shape[0]):
            mat2[r] = np.array([float(s) for s in input().split()])

        res = tradition(mat1, mat2)

        res = res.tolist()

        for r in res:
            print(' '.join(['%g' % (c) for c in r]))

if __name__ == "__main__":
    main()
