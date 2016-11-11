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
 
def knapsack(W,n,vals,caps):
    A = [[],[]]
    
    for x in range(W):
        A[0].append(0)
        A[1].append(0)
        
    for i in range(1,n):
        for x in range(W):
            cand_1 = A[0][x]
            
            if x >= caps[i]: 
                cand_2 = A[0][x-caps[i]] + vals[i]
            else:
                cand_2 = 0
                
            if cand_1 >= cand_2:
                A[1][x] = cand_1
            else:
                A[1][x] = cand_2
        
        A[0] = A[1][:]
                 
    return A[0][W-1]
    
W,n,vals,caps = read_file("assignment_2_3_1.txt")

max_val = knapsack(W,n,vals,caps)

print max_val

print "Reading file"
t1 = time()
W,n,vals,caps = read_file("assignment_2_3_2.txt") 
print time()-t1,"\n" 

print "Calculating"
t2 = time()
max_val = knapsack(W,n,vals,caps)
print time()-t2,"\n" 

print "Max value is ",max_val


assert max_val == 4243395, "Correct max_val is 4243395"
     

assert max_val == 2493893, "The correct answer is 2493893"