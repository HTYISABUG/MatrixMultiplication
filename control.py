#!bin/python3

import numpy as np
import main as ma

def main():
    mat1, mat2 = ma.read_data()

    print(np.matmul(mat1, mat2))

if __name__ == "__main__":
    main()
