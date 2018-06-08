import sys
from threading import Thread, Lock
import numpy as np

thread_lock = Lock()
threads = list()

def main():
    for line in sys.stdin:
        row1, col1 = [int(s) for s in line.split()]
        mat1 = np.zeros((row1, col1))

        for r in range(row1):
            mat1[r, :] = np.array([float(s) for s in input().split()])

        row2, col2 = [int(s) for s in input().split()]
        mat2 = np.zeros((row2, col2))

        for r in range(row2):
            mat2[r, :] = np.array([float(s) for s in input().split()])

        res = np.zeros((row1, col2))

        def calculate(r, c):
            tmp = float(0)

            for i in range(col1):
                tmp += mat1[r, i] * mat2[i, c]

            thread_lock.acquire()
            res[r, c] = tmp
            thread_lock.release()

        for r in range(row1):
            for c in range(col2):
                thread = Thread(target=calculate, args=(r, c))
                thread.start()
                threads.append(thread)

        for t in threads:
            t.join()

        threads.clear()

        res = res.tolist()

        for r in res:
            print(' '.join(['%g' % (c) for c in r]))

if __name__ == "__main__":
    main()
