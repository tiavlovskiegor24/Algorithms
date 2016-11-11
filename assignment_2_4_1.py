from bellman_ford_sp import *
from dijkstra_shortest_path import *
from floyd_warshall import *
from johnson_apsp import *
from time import time

def read_graph(filename):
    
    edges = {}
    vertices = {}
    neighbours = {}
    
    with open(filename,"r") as f:
        edge = 0
        for line in f:
            if edge < 1:
                edge += 1
                continue
            line  = line.split()
            
            #if float(line[-1]) < 0:
                #print "Graph has negative edge costs\n"
            
            edges["e" + str(edge)] = {"vertices":[int(v) for v in line[:-1]],"length":float(line[-1])}
            
            if int(line[0]) not in vertices:
                #vertices[int(line[0])] = {"out_edges":["e" + str(edge)],"in_edges":[],"label":None}
                vertices[int(line[0])] = {"edges":["e" + str(edge)],"label":None}
            else:
                #vertices[int(line[0])]["out_edges"].append("e" + str(edge))
                vertices[int(line[0])]["edges"].append("e" + str(edge))
            #print int(line[0]),vertices[int(line[0])]
            
            if int(line[1]) not in vertices:
                #vertices[int(line[1])] = {"out_edges":[],"in_edges":["e" + str(edge)],"label":None}
                vertices[int(line[1])] = {"edges":[],"label":None}
            #else:
             #   vertices[int(line[1])]["in_edges"].append("e" + str(edge))
            
            edge += 1
    
    return {"vertices":vertices,"edges":edges} 
                
def find_min(array):
    min_element = array[0]
    min_ind = 0
    for i in xrange(len(array)):
        if array[i] < min_element:
            min_element = array[i]
            min_ind = i
    return min_element,min_ind
    
         

def apsp_BF(graph):
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    min_sp = float("inf")
    count = 0
    print "Running apsp_BF..."
    for v in graph["vertices"]:
        A,_,_ = bellman_ford_push_Q(graph,v)
        if A == None:
            return None
        sp,_ = find_min(A)
        if sp < min_sp:
            min_sp = sp
        count += 1
        print count
    return min_sp

def apsp_FW(graph):
    
    A,B = floyd_warshall(graph)
    if A == None:
        return None
    
    min_sp = float("inf")
    for i in xrange(len(A)):
        sp,_ = find_min(A[i])
        if sp < min_sp:
            min_sp = sp
    return min_sp
    
def apsp_Johnson(graph):
    
    A,B = johnson_sp(graph)
    if A == None:
        return None
    
    min_sp = float("inf")
    for i in xrange(len(A)):
        sp,_ = find_min(A[i])
        if sp < min_sp:
            min_sp = sp
    return min_sp
    
    
graph_1 = read_graph("assignment_2_4_1_graph_1.txt")
graph_2 = read_graph("assignment_2_4_1_graph_2.txt")
graph_3 = read_graph("assignment_2_4_1_graph_3.txt")
#graph_large = read_graph("assignment_2_4_1_graph_large.txt")
graph_test = read_graph("apsp_test.txt")
#print graph_test["edges"]

t1= time()
A1_ = bellman_ford_push_Q(graph_3,50)
print "Push queue BF",time()-t1
#t2 = time()
#A2,B = bellman_ford_push(graph_3,11)
#print "Push BF",time()-t2

#for i in xrange(len(A1)):
 #   if A1[i] != A2[i]:
  #      print "Does not match"
   #     break

##print apsp_FW(graph_test)

#print dijkstra_shortest_path(graph_test,2)

#print apsp_Johnson(graph_test)

#min_sp_1 = apsp_FW(graph_1)
#min_sp_2 = apsp_FW(graph_2)
#min_sp = apsp_Johnson(graph_3)
#min_sp = johnson_sp(graph_large)
#min_sp = johnson_sp(graph_test)
#print min_sp

print apsp_BF(graph_3)


#print min_sp_1,min_sp_2,min_sp_3






