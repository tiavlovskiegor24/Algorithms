from quick_sort_class import *
from collections import deque
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
            edges["e" + str(edge)] = {"vertices":line[:-1],"weight":float(line[-1])}
            if line[0] not in vertices:
                vertices[line[0]] = {"edges":["e" + str(edge)],"label":None}
            else:
                vertices[line[0]]["edges"].append("e" + str(edge))
            
            if line[1] not in vertices:
                vertices[line[1]] = {"edges":["e" + str(edge)],"label":None}
            else:
                vertices[line[1]]["edges"].append("e" + str(edge))
            
            edge += 1
    
    return {"vertices":vertices,"edges":edges}  


class Union_find(object):
    
    def __init__(self,elements):
        self.n_sets = len(elements)
        self.leaders = {}
        self.sets = {}
        self.set_size = {}
        for element in elements:
            self.sets[element] = [element]
            self.set_size[element] = 1
            self.leaders[element] = element
        
    def find(self,element):
        return self.leaders[element]
    
    def union(self,element_1,element_2):
        set1 = self.find(element_1)
        set2 = self.find(element_2)
        
        if self.set_size[set1] > self.set_size[set2]:
            self.update_leader(set2,set1)
            self.set_size[set1] += self.set_size[set2]
            del self.sets[set2]
        else:
            self.update_leader(set1,set2)
            self.set_size[set2] += self.set_size[set1]
            del self.sets[set1]
        
        self.n_sets -= 1   
        
    
    def update_leader(self,set,new_leader):
        for node in self.sets[set]:
            self.leaders[node] = new_leader
            self.sets[new_leader].append(node)

  
def single_link_clustering(graph,k):
    vertex_list = []
    edge_list = deque([])
    for edge in graph["edges"]:
        edge_list.append((graph["edges"][edge]["weight"],edge))
        
    for vertex in graph["vertices"]:
        vertex_list.append(vertex)
    
    print "Sorting the edges"
    t1 = time()
    Quick_Sort(edge_list)
    print time()-t1,"s\n"
    
    uf = Union_find(vertex_list)
    
    print "Running the greedy algorithm"
    t1 = time()
    while uf.n_sets > k:
        min_edge = edge_list.popleft()
        vertices = graph["edges"][min_edge[1]]["vertices"]
        
        if uf.find(vertices[0]) != uf.find(vertices[1]):
            uf.union(vertices[0],vertices[1])
    
    for min_edge in edge_list:
        vertices = graph["edges"][min_edge[1]]["vertices"]
        
        if uf.find(vertices[0]) != uf.find(vertices[1]):
            max_spacing = min_edge[0]
            break
    print time()-t1,"s\n"
    print "Max spacing is",max_spacing

    return uf.sets,max_spacing
    
print "Reading the graph"   
t1 = time() 
graph = read_graph("assignment_2_2_1.txt")
print time()-t1,"s\n"
#graph = read_graph("assignment_2_2_1_test.txt")
clusters,max_spacing = single_link_clustering(graph,4)

assert max_spacing == 106.0,"For full set"