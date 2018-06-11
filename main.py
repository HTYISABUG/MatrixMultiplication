#!bin/python3

from threading import Thread, Lock
import threadpool
import numpy as np

def read_data():
    mat1 = np.zeros([int(s) for s in input().split()])

    for r in range(mat1.shape[0]):
        mat1[r] = np.array([float(s) for s in input().split()])

    mat2 = np.zeros([int(s) for s in input().split()])

    for r in range(mat2.shape[0]):
        mat2[r] = np.array([float(s) for s in input().split()])

    return mat1, mat2

def tradition(mat1, mat2):
    res = np.zeros((mat1.shape[0], mat2.shape[1]))

    threads = list()
    thread_lock = Lock()

    def calculate(r):
        for c in range(mat2.shape[1]):
            for i in range(mat1.shape[1]):
                res[r, c] += mat1[r, i] * mat2[i, c]

    pool = threadpool.ThreadPool(16)
    requests = threadpool.makeRequests(calculate, range(len(mat1)))
    [pool.putRequest(req) for req in requests]
    pool.wait()

    return res

def strassen(a, b):

    def expand(x, y):
        edge = max(max(x.shape), max(y.shape))
        e = 1

        while e < edge:
            e *= 2

        x_, y_ = np.zeros((e, e)), np.zeros((e, e))
        x_[:x.shape[0], :x.shape[1]] = x
        y_[:y.shape[0], :y.shape[1]] = y

        return x_, y_, e

    a_, b_, n = expand(a, b)

    if n <= 2:
        x = np.zeros((n, n))

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    x[i, j] += a_[i, k] * b_[k, j]

        return x[:a.shape[0], :b.shape[1]]
    else:
        n = int(n / 2)

        def divide(x, n):
            x11 = x[:n, :n]
            x12 = x[:n, -n:]
            x21 = x[-n:, :n]
            x22 = x[-n:, -n:]

            return x11, x12, x21, x22

        a11, a12, a21, a22 = divide(a_, n)
        b11, b12, b21, b22 = divide(b_, n)

        thread_lock = Lock()

        p = [None, None, None, None, None, None, None, None]

        def calculate(x, y, i):
            tmp = strassen(x, y)

            thread_lock.acquire()
            p[i] = tmp.copy()
            thread_lock.release()

        threads = list()
        threads.append(Thread(target=calculate, args=(a11+a22, b11+b22, 1)))
        threads.append(Thread(target=calculate, args=(a21+a22, b11, 2)))
        threads.append(Thread(target=calculate, args=(a11, b12-b22, 3)))
        threads.append(Thread(target=calculate, args=(a22, b21-b11, 4)))
        threads.append(Thread(target=calculate, args=(a11+a12, b22, 5)))
        threads.append(Thread(target=calculate, args=(a21-a11, b11+b12, 6)))
        threads.append(Thread(target=calculate, args=(a12-a22, b21+b22, 7)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        _, p1, p2, p3, p4, p5, p6, p7 = p

        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 + p3 - p2 + p6

        c1 = np.concatenate((c11, c12), axis=1)
        c2 = np.concatenate((c21, c22), axis=1)
        c  = np.concatenate((c1, c2), axis=0)

        return c[:a.shape[0], :b.shape[1]]
def anotherway(a, b):
    threads = list()
    thread_lock = Lock()
    def mul(A, B):
        length = len(A)
        result = np.zeros((length,length)) #length*length
        for i in range(0, length):
            for j in range(0, length):
                for k in range(0, length):
                    result[i][j] += A[i][k] * B[j][k]
        return result
    
    def expand(x, y):
        edge = max(max(x.shape), max(y.shape))
        e = 1

        while e < edge:
            e *= 2

        x_, y_ = np.zeros((e, e)), np.zeros((e, e))
        x_[:x.shape[0], :x.shape[1]] = x
        y_[:y.shape[0], :y.shape[1]] = y

        return x_, y_, e


    def divide(x, n):
        x11 = x[:n, :n]
        x12 = x[:n, -n:]
        x21 = x[-n:, :n]
        x22 = x[-n:, -n:]

        return x11, x12, x21, x22


    a_, b_, n = expand(a, b)
    b_= b_.T #transport
    n = int(n / 2)
    a11, a12, a21, a22 = divide(a_, n)
    b11, b12, b21, b22 = divide(b_, n)
    c11=mul(a11,b11)+mul(a12,b12)
    c12=mul(a11,b21)+mul(a12,b22)
    c21=mul(a21,b11)+mul(a22,b12)
    c22=mul(a21,b21)+mul(a22,b22)
    c1 = np.concatenate((c11, c12), axis=1)
    c2 = np.concatenate((c21, c22), axis=1)
    c  = np.concatenate((c1, c2), axis=0)
    return c
    
def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', '-m',
            default=0, help='0 for tradition, 1 for strassen , 2 for anotherway')

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    mat1, mat2 = read_data()
    res = tradition(mat1, mat2) if args.mode == 0 else strassen(mat1, mat2) if args.mode == 1  else  anotherway(mat1, mat2)
    print(res)

if __name__ == "__main__":
    main()

