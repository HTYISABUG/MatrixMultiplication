#!/usr/bin/python3
def readFile():
    print('ANOTHER MATRIX MULTUPLICATION')
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
        f.close()
        return matrix_A, matrix_B
    
def mul(A, B):
    length = len(A)
    length2 = len(A[0])
    length3 = len(B[0])
    if len(A[0])!=len(B):
        print("Size error")
        return
    C = [[0 for j in range(0, length)] for i in range(0, length3)] #length*length2
    for k in range(0, length2):
        for i in range(0, length):
            for j in range(0, length3):
                C[i][j] += A[i][k] * B[k][j] #cache hit max 
    return C

def print_matrix(result_m):
    for line in result_m:
        print(" ".join(map(str,line)))

def div_matrix(matrix1,matrix2):
    print(len(matrix1))
    print(len(matrix2))

if __name__ == '__main__':
        matrix_A, matrix_B = readFile()
        print_matrix(mul(matrix_A,matrix_B))
        div_matrix(matrix_A,matrix_B)
