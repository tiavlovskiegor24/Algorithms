import numpy as np

def strassen_matrix_mult(X,Y):
    
    X = np.array(X)
    Y = np.array(Y) 
    
    n = len(X)
    
    if n == 1:
        return X*Y
    
    A = X[:n/2,:n/2]
    B = X[:n/2,n/2:]
    C = X[n/2:,:n/2]
    D = X[n/2:,n/2:]
    
    E = Y[:n/2,:n/2]
    F = Y[:n/2,n/2:]
    G = Y[n/2:,:n/2]
    H = Y[n/2:,n/2:]
    
    p1 = strassen_matrix_mult(A,F-H)
    p2 = strassen_matrix_mult(A+B,H)
    p3 = strassen_matrix_mult(C+D,E)
    p4 = strassen_matrix_mult(D,G-E)
    p5 = strassen_matrix_mult(A+D,E+H)
    p6 = strassen_matrix_mult(B-D,G+H)
    p7 = strassen_matrix_mult(A-C,E+F)
    
    return np.concatenate((np.concatenate((p5+p4-p2+p6,p1+p2),axis = 1),np.concatenate((p3+p4,p1+p5-p3-p7),axis = 1)),axis = 0)
 
X = np.array([[1,4,6,4],[5,8,2,6],[9,0,3,5],[1,59,5,2]])
Y = np.array([[1,4,8,4],[5,-7,2,6],[9,0,-20,5],[1,59,5,0]])
#X = np.array([[1,2],[3,4]])
#Y = np.array([[5,6],[7,8]])

print strassen_matrix_mult(X,Y)
print
print np.dot(X,Y)   
print
print strassen_matrix_mult(X,Y)-np.dot(X,Y)


