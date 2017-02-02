### Optimal Binary Tree

T = [0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25]
sizeTree = len(T)

A = [[0 for x in range(sizeTree)] for x in range(sizeTree)]

for s in range(sizeTree):
    for i in range(sizeTree):
        if i+s >= sizeTree:
            break    
        minSplit = 9999
        pkSum = 0
        for r in range(i, i+s+1):
            pkSum += T[r]
            if r - 1 < i:
                split1 = 0
            else: 
                split1 = A[i][r-1]
            if r + 1 > s + i:
                split2 = 0
            else: 
                split2 = A[r+1][i+s]
            minSplit = min(minSplit, split1+split2)
        A[i][i+s] = minSplit + pkSum
        
print A[0][6]