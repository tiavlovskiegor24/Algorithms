import numpy as np
def FFT(a,w = None):
    # fuction computues the fourier transform of coefficiants array of length n using the primitive nth root of unity w.
    # Input:
    #   a  - array of coefficients of size n, where n is a power of 2
    #   w  - nth root of unity. If w is not provided, it is calculated from the length of the vector a, extended with zero elements up until the nearest power of 2
    
    # Output:
    #   r - array of calculated values
    
    na = a.shape[0]
    n = 2**np.ceil(np.log2(na)).astype(int)
    a = np.array([a[i] if i < na else 0 for i in xrange(n)],dtype=complex)
    
    if w == None:
        w = np.exp(2*np.pi*1j/n)
        
    n = a.shape[0]
    
    if np.isclose(w,1):
        return a
    else:
        a_even = np.array([a[i] for i in xrange(0,n,2)],dtype=complex)
        a_odd = np.array([a[i] for i in xrange(1,n,2)],dtype=complex)
        s1 = FFT(a_even,w**2)
        s2 = FFT(a_odd,w**2)
        r = np.zeros_like(a).astype(np.complex)
        
        w_vector = np.array([w**i for i in xrange(n/2)],dtype=complex)
        r[:n/2] = s1 + w_vector*s2
        r[n/2:] = s1 - w_vector*s2
        
        return r
        


    
     
     
    