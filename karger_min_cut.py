from random import *
    
def create_adj_lists(neighbours):
    edges = {}
    vertices = {}
    
    for neighbour in neighbours:
        vertices[neighbour] = []
    
    edge = 1
    for vertex in neighbours:
        for neighbour in neighbours[vertex]:
            edges["e" + str(edge)] = [vertex,neighbour]
            vertices[vertex].append("e" + str(edge)) 
            vertices[neighbour].append("e" + str(edge))
            neighbours[neighbour] = [remains for remains in neighbours[neighbour] if remains != vertex]
            edge += 1    
    
    return vertices,edges

def test_create_adj_lists():
    neighbours = {"1":["2","7","8"],'2':['1','7','3'],'3':['2','6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3','7'],\
                '7':['1','2','6','8'],'8':['1','7']}
    
    vertices,edges = create_adj_lists(neighbours)
    
    assert len(edges) == 13 and len(vertices) == 8
test_create_adj_lists()

def karger_min_cut(vertices,edges):
    
    m = len(edges)
    n = len(vertices)
    
    for i in range(1,n-1):
        seed()
        selected_edge = choice(edges.keys())
        fused_vertex = ""
        fused_vertex = "-".join([vertex for vertex in edges[selected_edge]])
        vertices[fused_vertex] = []
        
        for merged_vertex in edges[selected_edge]:
            vertices[fused_vertex] += [edge for edge in vertices[merged_vertex] if edge != selected_edge] # and not (edge in vertices[fused_vertex])]
            for edge in vertices[merged_vertex]:
                if (edge != selected_edge):
                    edges[edge] = [vertex for vertex in edges[edge] if vertex != merged_vertex and vertex != fused_vertex]
                
                    if len(edges[edge]) > 0:
                        edges[edge].append(fused_vertex) 
                    else:
                        del edges[edge]                 
    
            del vertices[merged_vertex]
            
        vertices[fused_vertex] = [edge for edge in vertices[fused_vertex] if edge in edges] 
            
        del edges[selected_edge]
        
    
    return len(edges),vertices,edges

def test_karger_min_cut():
    neighbours = {"1":["2","7","8"],'2':['1','7','3'],'3':['2','6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3','7'],\
                '7':['1','2','6','8'],'8':['1','7']}
    
    min_cut = karger_min_cut(neighbours)
    assert min_cut == 2
#test_karger_min_cut()


neighbours = {"1":["2","7","8"],'2':['1','7','3'],'3':['2','6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3','7'],\
                '7':['1','2','6','8'],'8':['1','7']}

best_min_cut = float("inf")
best_min_cut_vertices = None

vertices,edges = create_adj_lists(neighbours)

print "Number of vertices:",len(vertices)
print "Number of edges",len(edges)
print
                 
for i in range(len(vertices)):
    min_cut,min_cut_vertices,min_cut_edges = karger_min_cut(vertices.copy(),edges.copy())
    if min_cut < best_min_cut:
        best_min_cut = min_cut
        best_min_cut_vertices = min_cut_vertices

print best_min_cut
print
print best_min_cut_vertices
print

    
        
 



