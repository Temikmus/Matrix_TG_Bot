def transpose_matrix(matrix):
    # transpose the matrix
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]
transposed_matrix = transpose_matrix([[1,2,3],[4,5,6],[7,8,9]])
for row in transposed_matrix:
    print(row)

