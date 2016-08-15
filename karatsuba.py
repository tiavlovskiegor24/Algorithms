def karatsuba_1(num,digit):
    l = len(num)
    if l == 1:
        return int(num) * int(digit)
    
    A = num[0:l-l/2]
    B = num[l-l/2:l]
    
    prod1 = karatsuba_1(A,digit)
    prod2 = karatsuba_1(B,digit)
    
    return prod1*(10**(l/2)) + prod2
    

def karatsuba(num1,num2):
    n1 = len(num1)
    n2 = len(num2)
    
    if n1 >= n2:
        large = num1
        l = n1
        small = num2
        s = n2
    else:
        large = num2
        l = n2
        small = num1
        s = n1
    
    small = (l-s)*"0" + small
    s = len(small)
    
    if int(small) == 0 or int(large) == 0:
        return 0 
    
    if s == 1:
        return int(large)*int(small)
        
    A = large[0:l-l/2]
    B = large[l-l/2:l]
    C = small[0:s-s/2]
    D = small[s-s/2:s]
    prod1 = karatsuba(A,C)
    prod2 = karatsuba(B,D)
    prod3 = karatsuba(str(int(A) + int(B)),str(int(C) + int(D)))
    
    return prod1*(10**(l/2))*(10**(l/2)) + (prod3-prod2-prod1)*(10**(l/2)) + prod2
    
    
def karatsuba_slow(num1,num2):
    n1 = len(num1)
    n2 = len(num2)
    
    if n1 >= n2:
        large = num1
        l = n1
        small = num2
        s = n2
    else:
        large = num2
        l = n2
        small = num1
        s = n1
    
    if s == 1:
        return karatsuba_1(large,small)
    
        
    A = large[0:l-l/2]
    B = large[l-l/2:l]
    C = small[0:s-s/2]
    D = small[s-s/2:s]
    prod1 = karatsuba_slow(A,C)
    prod2 = karatsuba_slow(B,D)
    prod3 = karatsuba_slow(A,D)
    prod4 = karatsuba(B,C)
    
    return prod1*(10**(l/2))*(10**(s/2)) + prod3*(10**(l/2)) + prod4*(10**(s/2)) + prod2
    
def karatsuba_very_slow(num1,num2):
    n1 = len(num1)
    n2 = len(num2)
    
    if n1 >= n2:
        large = num1
        l = n1
        small = num2
        s = n2
    else:
        large = num2
        l = n2
        small = num1
        s = n1
    
    if s == 1:
        return karatsuba_1(large,small)
    
        
    A = large[0:l-s/2]
    B = large[l-s/2:l]
    C = small[0:s-s/2]
    D = small[s-s/2:s]
    prod1 = karatsuba_slow(A,C)
    prod2 = karatsuba_slow(B,D)
    prod3 = karatsuba(str(int(A) + int(B)),str(int(C) + int(D)))
  
    return prod1*(10**(s/2))*(10**(s/2)) + (prod3-prod2-prod1)*(10**(s/2)) + prod2
  
from time import time  
    
num1 = "57985770987980723458709868768659871283410298377198475092387502983475092868118097236"*64
num2 = "12032985709387856889750982347509823740987502983820945029384601265412387561459012346"*64

print

t0 = time()
r0 = int(num1)*int(num2)
print time()-t0
print

t1 = time()
r1 = karatsuba(num1,num2)
print time()-t1
print

t2 = time()
r2 = karatsuba_slow(num1,num2)
print time()-t2
print

t3 = time()
r3 = karatsuba_very_slow(num1,num2)
print time()-t3
print

print r0 == r1 and r0 == r2 and r0 == r3 