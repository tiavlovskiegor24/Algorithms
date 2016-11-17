from FFT import *
from time import time

def evaluate_poly(a,x):
    # function evaluate polynomial A specified by coefficients in a at location x
    # Input:
    #   a - array of polynomial coefficients of size n
    #   x - position to evaluate polynomial at
    # Output:
    #   A(x)
    
    n = a.shape[0]
    
    v = a[-1]
    for i in xrange(n-2,-1,-1):
        v = v*x + a[i]
        
    return v

def nth_root(n):
    return np.exp(2*np.pi*1j/n) 
    
def poly_mult(a,b):
    na = a.shape[0]
    nb = b.shape[0]
    c = np.zeros(na+nb-1).astype(complex)
    #c[0] = a[0]*b[0]
    for k in xrange(na+nb):
        for i in xrange(k+1):
            if i < na and k-i < nb:
                c[k] += a[i]*b[k-i] 
    return c

def poly_mult_FFT(a,b):
    na = a.shape[0]
    nb = b.shape[0]
    wa = nth_root(na)
    wb = nth_root(nb)
    nc = na+nb-1
    n = 2**np.ceil(np.log2(nc)).astype(int)
    wc = nth_root(n)
    
    a = np.array([a[i] if i < na else 0 for i in xrange(n)],dtype=complex)
    b = np.array([b[i] if i < nb else 0 for i in xrange(n)],dtype=complex)
    #print "a is",a,"\n"
    #print "b is",b,"\n"
    
    A = FFT(a,wc)
    B = FFT(b,wc)
    
    C = A*B
    #print "C is",C,"\n"
    
    c = (1./n)*FFT(C,wc**-1)
    
    return c[:nc]    





na = 3
n = 2**np.ceil(np.log2(na)).astype(int)
w = np.exp(2*np.pi*1j/n)

a = np.random.randint(-10,10,na).astype(complex)
b = np.random.randint(-10,10,5).astype(complex)

#print w,w**n,w**-1,np.isclose(w,1),np.isclose(w**(n-1),1)
#print

'''A1 = FFT(a)
print a
print
print A1
print 
print np.fft.fft(a)
print 

A2 = np.array([evaluate_poly(a,w**i) for i in xrange(n)],dtype=complex)
print A2

print "FFT is correct?",np.isclose(A1,A2).all()'''

t1 = time()
c1 = poly_mult_FFT(a,b)
print "Polynomial multiplication using FFT took:",time()-t1,"seconds\n"
#print abs(c1)
#print c1

t1 = time()
c2 = poly_mult(a,b)
print "Standard polynomial multiplication took:",time()-t1,"seconds\n"
#print 
#print c2

print "Poly product using FFT is correct?",np.isclose(c1,c2).all()

nc = c1.shape[0]
t1 = time()
C1 = FFT(c1)
#print C1
print "FFT on %d degree polynomial took %.3f seconds\n"%(nc-1,time()-t1)

n = 2**np.ceil(np.log2(nc)).astype(int)
wc = nth_root(n)
#print C1
print
#print np.fft.fft(c1)

C2 = np.array([evaluate_poly(a,wc**i)*evaluate_poly(b,wc**i) for i in xrange(n)],dtype=complex)
#print C2

print "Poly product using FFT is correct?",np.isclose(C1,C2).all()


