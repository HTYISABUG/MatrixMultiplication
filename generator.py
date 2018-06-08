import numpy as np

import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--size', type=int,
            default=10, help='max size of matrix')

    parser.add_argument('--number', type=int,
            default=10, help='number of test set')

    args = parser.parse_args()

    test   = open('test.txt', 'w')
    answer = open('answer.txt', 'w')

    for _ in range(args.number):
        size = np.random.randint(2, args.size)
        size = (size, size)

        mat1 = np.random.randint(0, 100, size)
        mat2 = np.random.randint(0, 100, size)

        test.write('%d %d\n' % size)

        for r in range(mat1.shape[0]):
            test.write('%s\n' % (' '.join(mat1[r].astype(str))))

        test.write('%d %d\n' % size)

        for r in range(mat2.shape[0]):
            test.write('%s\n' % (' '.join(mat2[r].astype(str))))

        ans = np.matmul(mat1, mat2)
        
        for r in range(ans.shape[0]):
            answer.write('%s\n' % (' '.join(ans[r].astype(str))))

    test.close()
    answer.close()

if __name__ == "__main__":
    main()
