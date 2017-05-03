def GMFPT_theory_1(A,weighted=True) :
    """
    According to the theory of Lin et al., 2012, the global mean first passage
    time can be calculated by finding the eigenspectrum of the Laplacian matrix
    of the graph. This function calculates the GMFPT from their formula, for the
    graph described by the adjacency matrix A, to all sites. Optional parameter
    'weighted' allows for the choice of having the same quantity but weighted
    with the stationary distribution.
    """
    N = A.shape[0]
    d = np.sum(A,axis=1)
    E = np.sum(d)/2.
    L = np.diag(d) - A
    l,v = np.linalg.eigh(L)
    sortidx = np.argsort(l)
    l = l[sortidx]
    #print l
    v = v[:,sortidx]
    T = np.zeros(N)
    #print v.shape,d.shape
    dv = np.dot (v.T,d)
    #print dv
    if not weighted :
        #for j in xrange(N) :
            #T[j] = np.dot(l[1:]**-1,2.0*E*v[j,1:]**2 - v[j,1:]*dv[1:])
            #print T[j]
        T = np.dot(2.0*E*v[:,1:]**2 - v[:,1:]*dv[1:],l[1:]**-1)
        
        return float(N)/(N-1.0) * T
    else :
        for j in xrange(N) :
            for k in xrange(1,N) :
                dvi = v[j,k]*dv[k]
                T[j] += 1.0/l[k]*((2*E)**2*v[j,k]**2 - 2*v[j,k]*2*E*dvi - dvi**2)
        return T/(2*E)