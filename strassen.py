import numpy as np

def readFile():
    print('TRANDITIONAL MATRIX MULTUPLICATION')
    filename = input('Filename: ')

    with open(filename) as f:
        matrix_A = []
        matrix_B = []
        i = 1
        for line in f:
            if i == 1:
                A_row, A_col = [int(x) for x in line.split()] 
                matrix = matrix_A
            elif i == A_row+2:
                B_row, B_col = [int(x) for x in line.split()] 
                matrix = matrix_B
            else:
                matrix.append([int(x) for x in line.split()])
            i = i + 1;
        return matrix_A, matrix_B

def print_matrix(result_m):
    for line in result_m:
        print(" ".join(map(str,line)))

def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def sub(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def mul(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def strassen_rec(A, B):
    n = len(A)
    if n <= 2:
        return mul(A, B)
    else:
        new_size = int(n/2)
        a11 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a12 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a21 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        a22 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        
        b11 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b12 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b21 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]
        b22 = [[0 for j in range(0, new_size)] for i in range(0, new_size)]

        # divide matrix
        for i in range(0, new_size):
            for j in range(0, new_size):
                a11[i][j] = A[i][j]
                a12[i][j] = A[i][j+new_size]
                a21[i][j] = A[i+new_size][j]
                a22[i][j] = A[i+new_size][j+new_size]
            
                b11[i][j] = B[i][j]
                b12[i][j] = B[i][j+new_size]
                b21[i][j] = B[i+new_size][j]
                b22[i][j] = B[i+new_size][j+new_size]
        
        rec_A = add(a11, a22)
        rec_B = add(b11, b22)
        p1 = strassen_rec(rec_A, rec_B)
        
        rec_A = add(a21, a22)
        p2 = strassen_rec(rec_A, b11)

        rec_B = sub(b12, b22)
        p3 = strassen_rec(a11, rec_B)
        
        rec_B = sub(b21, b11)
        p4 = strassen_rec(a22, rec_B)
        
        rec_A = add(a11, a12)
        p5 = strassen_rec(rec_A, b22)

        rec_A = sub(a21, a11)
        rec_B = add(b11, b12)
        p6 = strassen_rec(rec_A, rec_B)

        rec_A = sub(a12, a22)
        rec_B = add(b21, b22)
        p7 = strassen_rec(rec_A, rec_B)

       # merge matrix
        c11 = add(sub(add(p1, p4), p5), p7)
        c12 = add(p3, p5)
        c21 = add(p2, p4)
        c22 = add(sub(add(p1, p3), p2), p6)

        C = [[0 for j in range(0, n)] for i in range(0, n)]
        for i in range(0, new_size):
            for j in range(0, new_size):
                C[i][j] = c11[i][j]
                C[i][j+new_size] = c12[i][j]
                C[i+new_size][j] = c21[i][j]
                C[i+new_size][j+new_size] = c22[i][j]
        return C

if __name__ == '__main__':
    matrix_A, matrix_B = readFile()
    print_matrix(strassen_rec(matrix_A,matrix_B))