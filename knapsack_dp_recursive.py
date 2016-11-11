import sys
sys.setrecursionlimit(3000)
from time import time


def read_file(filename):
    with open(filename,"r") as f:
        
        caps = []
        vals = []
        count = 0
        for line in f:
            line = line.split()
            if count == 0:
                W = int(line[0])
                n = int(line[1])
                count += 1
                continue
            
            vals.append(int(line[0]))
            caps.append(int(line[1]))
                
            count += 1
            
    return W,n,vals,caps 
    
def kanpsack_recursive(problem,ht,vals,caps):
    
    (i,x) = problem
    
    if i == 0:
        return 0
    
    
    if (i-1,x) in ht:
        cand_1 = ht[(i-1,x)]
    else:
        cand_1 = kanpsack_recursive((i-1,x),ht,vals,caps)
    
    if x >= caps[i]:
        if (i-1,x-caps[i]) in ht:
            cand_2 = ht[(i-1,x-caps[i])] + vals[i]
        else:
            cand_2 = kanpsack_recursive((i-1,x-caps[i]),ht,vals,caps) + vals[i]
    else:
        ht[problem] = cand_1
        return cand_1
        
    if cand_1 >= cand_2:
        ht[problem] = cand_1
        return cand_1
    else:
        ht[problem] = cand_2
        return cand_2

ht = {}  

print "Reading file"
t1 = time()
W,n,vals,caps = read_file("assignment_2_3_2.txt") 
print time()-t1,"\n" 

print "Calculating"
t2 = time()
max_val = kanpsack_recursive((n-1,W),ht,vals,caps)
print time()-t2,"\n" 

print "Max value is ",max_val

print "Number of subproblems needed",len(ht)

assert max_val == 4243395, "Correct max_val is 4243395"
     