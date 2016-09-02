from collections import deque


def reset_labels(graph,reset_value = None):
    for vertex in graph['vertices']:
         graph['vertices'][vertex]['label'] = reset_value

def find_cc(graph):
    
    reset_labels(graph)
    
    n = len(graph['vertices'])
    m = len(graph['edges'])
    
    cc = {}
    
    for vertex in graph['vertices']:
        if graph['vertices'][vertex]["label"] == None:
            cc[vertex] = BFS(graph,vertex)
    
    return cc
    

def create_adj_lists(neighbours):
    edges = {}
    vertices = {}
    graph = {}
    
    for neighbour in neighbours:
        vertices[neighbour] = {"edges":[],"label":None}
    
    edge = 1
    for vertex in neighbours:
        for neighbour in neighbours[vertex]:
            edges["e" + str(edge)] = [vertex,neighbour]
            vertices[vertex]["edges"].append("e" + str(edge)) 
            vertices[neighbour]["edges"].append("e" + str(edge)) # only for the undirected graphs
            neighbours[neighbour] = [remains for remains in neighbours[neighbour] if remains != vertex]
            edge += 1
    
    graph["vertices"] = vertices
    graph["edges"] = edges    
    
    return graph
    
    

def shortes_path(graph,s,v):
    
    reset_labels(graph)
    BFS(graph,s)
    
    return abs(graph["vertices"][v]['label'] - graph["vertices"][s]['label']) 


# make sure to reset the labels of vertices to None before calling BFS
def BFS(graph,source = "1"):
    
    n = len(graph['vertices'])
    m = len(graph['edges'])
    
    found_vertices = [source]
    
    Q = deque([source])
    
    graph['vertices'][source]["label"] = 0
    
    while Q:
        v = Q.popleft()
        
        for edge in graph['vertices'][v]['edges']:
            neighbour = [vertex for vertex in graph['edges'][edge] if vertex != v][0]
            if graph['vertices'][neighbour]["label"] == None:
                found_vertices.append(neighbour)
                graph['vertices'][neighbour]["label"] = graph['vertices'][v]["label"] + 1
                Q.append(neighbour)
    return found_vertices
                
def read_vertices(filename):
    with open(filename,"r") as f:
        lines = []
        for line in f:
            lines.append(line.split())
        f.closed
        
    vertices = {}
    
    for line in lines:
          vertices[line[0]] = line[1:]
    return vertices

   
#neighbours = read_vertices("assignment3.txt")

neighbours1 = {"1":["2","7","8"],'2':['1','7','3'],'3':['2','6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3','7'],\
                '7':['1','2','6','8'],'8':['1','7']}

neighbours2 = {"1":["2","7","8"],'2':['1','7'],'3':['6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3'],\
                '7':['1','2','8'],'8':['1','7']}
                

graph = create_adj_lists(neighbours2)

BFS(graph)

print find_cc(graph)

print shortes_path(graph,"6","3")

#print graph['vertices']


                 
    
    
    
    