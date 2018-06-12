#!bin/python3

import time
import numpy as np
import threadpool
import matplotlib.pyplot as plt

pool = threadpool.ThreadPool(16)

def read_data():
    a = np.zeros([int(s) for s in input().split()])

    for r in range(a.shape[0]):
        a[r] = np.array([float(s) for s in input().split()])

    b = np.zeros([int(s) for s in input().split()])

    for r in range(b.shape[0]):
        b[r] = np.array([float(s) for s in input().split()])

    return a, b

def control(a, b):
    return np.matmul(a, b)

def tradition(a, b):
    res = np.zeros((a.shape[0], b.shape[1]))

    def calculate(r):
        for c in range(b.shape[1]):
            for i in range(a.shape[1]):
                res[r, c] += a[r, i] * b[i, c]

    global pool
    requests = threadpool.makeRequests(calculate, range(a.shape[0]))
    [pool.putRequest(req) for req in requests]
    pool.wait()

    return res

def expand(a, b):
    edge = max(max(a.shape), max(b.shape))
    e = 1

    while e < edge:
        e *= 2

    a_, b_ = np.zeros((e, e)), np.zeros((e, e))
    a_[:a.shape[0], :a.shape[1]] = a
    b_[:b.shape[0], :b.shape[1]] = b

    return a_, b_, e

def mul(a, b):
    x = np.zeros((a.shape[0], b.shape[1]))

    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            for k in range(a.shape[1]):
                x[i, j] += a[i, k] * b[k, j]

    return x

def rise_hit_mul(A, B):
    length = len(A)	
    result = np.zeros((length,length))	
    for i in range(0, length):	
        for j in range(0, length):	
            for k in range(0, length):	
                result[i][j] += A[i][k] * B[j][k]	
    return result

def divide(x, n):
    x11 = x[:n, :n]
    x12 = x[:n, -n:]
    x21 = x[-n:, :n]
    x22 = x[-n:, -n:]

    return x11, x12, x21, x22

def strassen(a, b):
    a_, b_, n = expand(a, b)

    n = int(n / 2)

    a11, a12, a21, a22 = divide(a_, n)
    b11, b12, b21, b22 = divide(b_, n)


    if n <= 8:
        p = [None, None, None, None, None, None, None, None,]

        def calculate(a, b, i):
            p[i] = mul(a, b)

        arg = [([a11+a22, b11+b22, 1], {}),
               ([a21+a22, b11    , 2], {}),
               ([a11    , b12-b22, 3], {}),
               ([a22    , b21-b11, 4], {}),
               ([a11+a12, b22    , 5], {}),
               ([a21-a11, b11+b12, 6], {}),
               ([a12-a22, b21+b22, 7], {}),]

        global pool
        requests = threadpool.makeRequests(calculate, arg)
        [pool.putRequest(req) for req in requests]
        pool.wait()

        _, p1, p2, p3, p4, p5, p6, p7 = p
    else:
        p1 = strassen(a11+a22, b11+b22)
        p2 = strassen(a21+a22, b11,   )
        p3 = strassen(a11,     b12-b22)
        p4 = strassen(a22,     b21-b11)
        p5 = strassen(a11+a12, b22,   )
        p6 = strassen(a21-a11, b11+b12)
        p7 = strassen(a12-a22, b21+b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 + p3 - p2 + p6

    c1 = np.concatenate((c11, c12), axis=1)
    c2 = np.concatenate((c21, c22), axis=1)
    c  = np.concatenate((c1, c2), axis=0)

    return c[:a.shape[0], :b.shape[1]]

def anotherway(a, b):
    a_, b_, n = expand(a, b)
    b_= b_.T

    n = int(n / 2)

    a11, a12, a21, a22 = divide(a_, n)
    b11, b12, b21, b22 = divide(b_, n)
    
    p = [None, None, None, None, None, None, None, None]

    def calculate(a, b, i):
        p[i] = rise_hit_mul(a, b)

    arg = [([a11, b11, 0], {}),
           ([a12, b12, 1], {}),
           ([a11, b21, 2], {}),
           ([a12, b22, 3], {}),
           ([a21, b11, 4], {}),
           ([a22, b12, 5], {}),
           ([a21, b21, 6], {}),
           ([a22, b22, 7], {}),]

    global pool
    requests = threadpool.makeRequests(calculate, arg)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    p0, p1, p2, p3, p4, p5, p6, p7 = p

    c11 = p0 + p1
    c12 = p2 + p3
    c21 = p4 + p5
    c22 = p6 + p7

    c1 = np.concatenate((c11, c12), axis=1)
    c2 = np.concatenate((c21, c22), axis=1)
    c  = np.concatenate((c1, c2), axis=0)

    return c
    
def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', '-m', type=int,
            default=0, help='-1 for control, 0 for tradition, 1 for strassen, 2 for anotherway')

    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    if not args.test:
        a, b = read_data()

        res = None

        if args.mode == -1:
            res = control(a, b)
        elif args.mode == 0:
            res = tradition(a, b)
        elif args.mode == 1:
            res = strassen(a, b)
        elif args.mode == 2:
            res = anotherway(a, b)

        print(res)
    else:
        e, t = [], []

        while True:
            try:
                et = [None, None, None, None]

                a, b = read_data()

                ts = time.time()
                print(control(a, b))
                et[0] = time.time() - ts

                ts = time.time()
                print(tradition(a, b))
                et[1] = time.time() - ts

                ts = time.time()
                print(strassen(a, b))
                et[2] = time.time() - ts

                ts = time.time()
                print(anotherway(a, b))
                et[3] = time.time() - ts

                e.append(a.shape[0])
                t.append(et)
            except EOFError:
                e = np.array(e)
                t = np.array(t).T
                break

        plt.semilogx(e, t[0], '.-', label='numpy')
        plt.semilogx(e, t[1], '.-', label='tradition')
        plt.semilogx(e, t[2], '.-', label='strassen')
        plt.semilogx(e, t[3], '.-', label='anotherway')

        plt.grid()
        plt.legend()
        plt.xlabel('2\'s exponential')
        plt.ylabel('time(s)')
        plt.title('performance')
        plt.savefig('exp-time.png')

if __name__ == "__main__":
    main()
