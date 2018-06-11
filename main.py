#!bin/python3

from threading import Thread, Lock
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

        for i in range(n):
            for j in range(n):
                for k in range(n):
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

def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', '-m',
            default=0, help='0 for tradition, 1 for strassen')

    args = parser.parse_args()

def main():
    args = get_args()

    mat1, mat2 = read_data()

    res = tradition(mat1, mat2) if args.mode == 0 else strassen(mat1, mat2)

    print(res)

if __name__ == "__main__":
    main()
