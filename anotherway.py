#!/usr/bin/python3
import sys
from threading import Thread, Lock
import numpy as np

def readFile():
    for line in sys.stdin:
        mat1 = np.zeros([int(s) for s in line.split()])

        for r in range(mat1.shape[0]):
            mat1[r] = np.array([float(s) for s in input().split()])

        mat2 = np.zeros([int(s) for s in input().split()])

        for r in range(mat2.shape[0]):
            mat2[r] = np.array([float(s) for s in input().split()])
    return (mat1.tolist(), mat2.tolist())

def mul(A, B):
    length = len(A)
    result = [[0 for j in range(0, length)] for i in range(0, length)] #length*length3
    #for k in range(0, length2):
    #    for i in range(0, length):
    #        for j in range(0, length3):
    #            result[i][j] += A[i][k] * B[k][j] #cache hit max

    for i in range(0, length):
        for j in range(0, length):
            for k in range(0, length):
                result[i][j] += A[i][k] * B[j][k]
    return result

def print_matrix(result_m):
    answer = open('answer.txt', 'w')
    for line in result_m:
        answer.write(" ".join(map(str,line)))
        answer.write("\n")
    answer.close()

def add(A, B):
    n = len(A)
    C = []
    for i in range(0, n):
        C.append([x+y for x,y in zip(A[i], B[i])])
    return C

def ToSquare(matrix):
    if(len(matrix)!=len(matrix[0])):
        max_value=max(len(matrix),len(matrix[0]))
        new_matrix=[[0 for j in range(0, max_value)] for i in range(0, max_value)]
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                new_matrix[i][j]=matrix[i][j]
        return new_matrix
    else:
        return matrix
    
def ToOriginalSize(result,matrixA,matrixB):
    length = len(matrixA)
    length2 = len(matrixB[0])
    new_matrix=[[0 for j in range(0, length)] for i in range(0, length2)]
    for i in range(0, length):
            for j in range(0, (length2)):
                new_matrix[i][j]=result[i][j]
    return new_matrix

def div_matrix(matrix1,matrix2):
    n = len(matrix1)
    matrix2= (list(map(list, zip(*matrix2))))
   # print(matrix2)
    if n <= 2:
        return mul(matrix1,matrix2)
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
        for i in range(0, new_size):
            for j in range(0, new_size):
                a11[i][j] = matrix1[i][j]
                a12[i][j] = matrix1[i][j+new_size]
                a21[i][j] = matrix1[i+new_size][j]
                a22[i][j] = matrix1[i+new_size][j+new_size]
            
                b11[i][j] = matrix2[i][j]
                b12[i][j] = matrix2[i][j+new_size]
                b21[i][j] = matrix2[i+new_size][j]
                b22[i][j] = matrix2[i+new_size][j+new_size]
        c11=add(mul(a11,b11),mul(a12,b12))
        c12=add(mul(a11,b21),mul(a12,b22))
        c21=add(mul(a21,b11),mul(a22,b12))
        c22=add(mul(a21,b21),mul(a22,b22))
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
        #matrixB= (list(map(list, zip(*matrix_B))))
        #print_matrix(ToOriginalSize(mul(ToSquare(matrix_A),ToSquare(matrixB)),matrix_A, matrix_B ))
        print_matrix(ToOriginalSize(div_matrix(ToSquare(matrix_A),ToSquare(matrix_B)),matrix_A, matrix_B ))
