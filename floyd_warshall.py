def floyd_warshall(graph):
    print "\nRunning floyd_warshall...\n"
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    A = [[],[]]
    B = []
    
    for _ in xrange(n):
        A[0].append([float("inf") for _ in xrange(n)])
        A[1].append([float("inf") for _ in xrange(n)])
        B.append([None for _ in xrange(n)])
    
    #print "A has length",len(A)
    
    for i in xrange(n):
        A[0][i][i] = 0.
        
    for e in graph["edges"]:
        vertices = graph["edges"][e]["vertices"]
        A[0][vertices[0]-1][vertices[1]-1] = graph["edges"][e]["length"]
        A[1][vertices[0]-1][vertices[1]-1] = graph["edges"][e]["length"]
    
    for k in xrange(1,n):
        #print k
        ind = k % 2
        for i in xrange(n):
            for j in xrange(n):
                cand_1 = A[ind-1][i][j]
                cand_2 = A[ind-1][i][k]+A[ind-1][k][j]
                if cand_1 < cand_2:
                    #print ind,i,j
                    A[ind][i][j] = cand_1
                else:
                    A[ind][i][j] = cand_2
                    B[i][j] = k
        
        for i in xrange(n):
            if A[ind][i][i] < 0:
                print "Negative cycle detected."
                return None,None
    
    return A[ind],B





