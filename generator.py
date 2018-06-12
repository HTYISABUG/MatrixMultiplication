#!bin/python3

import argparse
import numpy as np

def main(args):
    with open('test.txt', 'w') as fp:
        for exp in range(args.exp):
            e = 2 ** (exp + 1)
            a = np.random.randint(100, 1000, size=(e, e))
            b = np.random.randint(100, 1000, size=(e, e))

            fp.write('%d %d\n' % (e, e))
            for row in a:
                fp.write(' '.join(row.astype(str)) + '\n')

            fp.write('%d %d\n' % (e, e))
            for row in b:
                fp.write(' '.join(row.astype(str)) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--exp', '-e', type=int,
            default=10, help='max 2\'s exponential')

    args = parser.parse_args()

    main(args)
