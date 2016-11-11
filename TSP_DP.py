import numpy as np
import matplotlib.pyplot as plt
from find_closest_pair import *
from quick_sort_class import *
from bitstring import BitArray
from time import time

def read_locations(filename):
    
    with open(filename,"r") as f:
        locs = []
        count = 0
        for line in f:
            if count < 1:
                count += 1
                continue
            #if count > 13:
             #   break
            
            line = line.split(" ")
            locs.append((float(line[0]),float(line[1])))
            count += 1
    return locs

def dist(point1,point2):
    
    dist = 0
    dim = 2
    
    for i in range(0,dim):
        dist += (point1[i]-point2[i])**2
        
    dist = np.sqrt(dist)
    return dist
    
def combinations(m,start,end,comb = None):
    if comb == None:
        comb = []
        
    if m == 1:
        for i in xrange(start,end-m+1):
            comb.append(i)
            #comb[i] = 1
            yield comb
            comb.pop() 
            #comb[i] = 0
            
    else:
        for i in xrange(start,end-m+1):
            comb.append(i)
            #comb[i] = 1
            for out in combinations(m-1,i+1,end,comb):
                yield out
            comb.pop()
            #comb[i] = 0
#for s in combinations(1,0,3):
 #   print s


def closest_pair_brute(points,given = None):    
    
    n = len(points)
    if n < 2:
        return None,float("inf")
    
    if given != None:
        closest_pair = [points[given-1],points[given]]
        min_dist = dist(points[given-1],points[given])
    else:
        closest_pair = [points[0],points[1]]
        min_dist = dist(points[0],points[1])
    
    
    if given != None:
        for i in [i for i in range(n) if i != given]:
            d = dist(points[i],points[given])
            if d < min_dist:
                closest_pair = [points[i],points[given]]
                min_dist = d
    else:
        for i in range(n):
            for j in range(i+1,n): 
                d = dist(points[i],points[j])
                if d < min_dist:
                    closest_pair = [points[i],points[j]]
                    min_dist = d
    
    return closest_pair,min_dist

def reconstruct_path(points,B,dest,last_point):
    n = len(points)
    
    path = []
    path.append(dest)
    index = BitArray(bin = "1"*n)
    to_p = last_point
    d = dist(points[dest],points[last_point])
    while True:
        #print index
        path.append(to_p)
        if index.uint in B[to_p]:
            from_p = B[to_p][index.uint]
            if from_p == to_p:
                path.append(from_p)
                break
            d += dist(points[to_p],points[from_p])
            x,y = zip(*[points[from_p],points[to_p]])
            plt.plot(x,y,color = "red")
            index[to_p] = 0
            #print index
            to_p = from_p
        else:
            print "Hello"
            #print B[to_p],index.uint,index.bin
            break
    
    print d
    return path[::-1]
    

def shortest_tour(in_points,source = 0,dest = 0):
    n = len(in_points)
    print "Number of points is",n
    print "\nSource is",source
    print "\nDestination is",dest
    
    if source != 0:
        points = in_points[source:] + in_points[:source]
        dest -= source
        source -= source
    else:
        points = in_points
    
    index = BitArray(bin = "0"*n)
    index[source] = 1
    
    A = [[],[]]
    B = []
    
    for _ in xrange(n):
        #A[0].append([float("inf") for _ in xrange((2**n))])
        #A[1].append([float("inf") for _ in xrange((2**n))])
        A[0].append({})
        A[1].append({})
        B.append({})
        
    A[0][0][index.uint] = 0
    A[1][0][index.uint] = 0
    #print A[0]
    B[0][index.uint] = 0

    for m in xrange(1,n):
        t1 = time()
        print "\nm is",m
        ind = m % 2
        #print ind
        
        #for S in combinations(m,source+1,n):
        for S in combinations(m,1,n):
            index = BitArray(bin = "0"*n)
            index[0] = 1
            #print "\nS is",S
            
            for i in S:
                index[i] = 1
            #print "S_index",index
            
            S_index = index.uint
            for j in S:#[j for j in S if j != source]:
                min_path = float('inf')
                #print "j is",j
                index[j] = 0
                #print index
                
                d = dist(points[source],points[j])
                #print "d is",d
                
                if index.uint in A[ind-1][source]:
                    new_path = A[ind-1][source][index.uint] + d
                else:
                    new_path = float("inf")
                
                if new_path < min_path:
                    #print "Hello"
                    min_path = new_path
                    A[ind][j][S_index] = min_path
                    B[j][S_index] = source
                    #del A[ind-1][0][index.uint]
                
                
                for k in [k for k in S if k != j]:
                    #print "k is",k
                    d = dist(points[k],points[j])
                    #print "d is",d
                    if index.uint in A[ind-1][k]:
                        new_path = A[ind-1][k][index.uint] + d
                    else: 
                        new_path = float("inf")
                    
                    if new_path < min_path:
                        #print "Hello"
                        min_path = new_path
                        A[ind][j][S_index] = min_path
                        B[j][S_index] = k
                        #del A[ind-1][k][index.uint]
                        
                
                index[j] = 1
        
        for j in A[ind-1]:
            j.clear()
        
        print "It took %f seconds"%(time()-t1)
        
        
    index = BitArray(bin = "1"*n)   
        #print A[ind]
    if dest != source:
        #print A[ind][dest-source]
        if index.uint in A[ind][dest]:
            min_path = A[ind][dest][index.uint]
            last_point = dest
        else:
            print A[ind][dest]
    else:
        min_path = float('inf')
        for j in xrange(1,n):

            d = dist(points[dest],points[j])
            #print "d is",d
        
            if index.uint in A[ind][j]:
                new_path = A[ind][j][index.uint] + d
            else:
                #print A[ind][j]
                new_path = float("inf")
            
            if new_path < min_path:
                #print "Hello"
                min_path = new_path
                last_point = j
                #A[ind][j][S_index] = min_path
                x,y = zip(*[points[dest],points[j]])
        plt.plot(x,y,color = "green")
    
    path_loc = reconstruct_path(points,B,dest,last_point)
    path = []
    for loc in path_loc:
        path.append(points[loc])
    
    return path,min_path
                     

    
t1 = time()
locs = read_locations("assignment_2_5.txt")
x,y = zip(*locs)
plt.scatter(x,y)
#plt.show()
#locs = np.array(locs)
x_sorted = locs[:]
Quick_Sort(x_sorted,0)
y_sorted = locs[:]
Quick_Sort(y_sorted,1)

#A1,min_path1 = shortest_tour(x_sorted,0,0)
#print min_path1
#plt.show()

cluster_1 = [loc for loc in x_sorted if loc[0]<25000]
cluster_2 = [loc for loc in x_sorted if loc[0]>25000]


#print cluster_1


#pair,min_dist = closest_pair_brute(cluster_1,10)


_,min_path1 = shortest_tour(cluster_1,11,12)
print min_path1

_,min_path2 = shortest_tour(cluster_2,0,1)
print min_path2

print dist(cluster_1[11],cluster_2[0])+dist(cluster_1[12],cluster_2[1])+min_path1+min_path2
print dist(cluster_1[11],cluster_2[1])+dist(cluster_1[12],cluster_2[0])+min_path1+min_path2

print time()-t1
#print A


#x,y = zip(*pair)

#plt.scatter(x,y,color = "red")
plt.show()


#print find_closest_pair(locs)'''


    