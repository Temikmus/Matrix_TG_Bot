import numpy as np
def transpose_matrix(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def reverse_matrix(a, n1, m1):
    c=[[0 for i in range(m1)] for j in range(n1)]
    for i in range(n1):
        for j in range(m1):
            alg = (-1)**(i+j)
            b = []
            for line in range(n1):
                for column in range(m1):
                    if line != i and column != j:
                        b.append(a[line][column])
            B = [[0 for i in range(m1 - 1)] for j in range(n1 - 1)]
            ind = 0
            for line in range(n1-1):
                for column in range(m1-1):
                    B[line][column] = b[ind]
                    ind += 1
            alg *= np.linalg.det(B)
            c[i][j] = alg
    print(c)
    trans = transpose_matrix(c)
    print(trans)

transposed_matrix = transpose_matrix([[1,2,3],[4,5,6],[7,9,9]])
for row in transposed_matrix:
    print(row)
reverse_matrix([[1,2,3],[4,5,6],[7,9,9]],3,3)




