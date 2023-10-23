import numpy as np
import random

def product_matrix(A,B,n1,m1,n2,m2):
    c=[[0 for i in range(m2)] for i in range(n1)]
    for i in range(n1):
        for j in range(m2):
            for k in range(m1):
                c[i][j]+=(A[i][k]*B[k][j])
    return c



