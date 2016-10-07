import heap as Heap

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


def reset_labels(graph,reset_value = "Unexplored"):
    for vertex in graph['vertices']:
        graph['vertices'][vertex]['label'] = reset_value
   
def prim_MST(graph,source = None):
    
    if source == None:
        source = "1"
        
    for vertex in graph["vertices"]:
        graph["vertices"][vertex]["label"] = "Unexplored"
    
    graph["MST"] = {"edges":[],"cost":0}
    graph["explored_vertices"] = {"spanned":{source:0},"not_spanned":{}}
    heap = Heap.Heap()
         
    graph['vertices'][source]["label"] = "spanned"
    
    update_heap(graph,heap,source)
    
    while heap.array:
        
        smallest_weight,(spanned_vertex,min_edge) = heap.extract()
        graph["MST"]["edges"].append(min_edge)
        graph["MST"]["cost"] += smallest_weight
        
        graph["explored_vertices"]["spanned"][spanned_vertex] = (smallest_weight,min_edge)
        
        del graph["explored_vertices"]["not_spanned"][spanned_vertex]
        
        graph['vertices'][spanned_vertex]["label"] = "spanned"
        
        update_heap(graph,heap,spanned_vertex)

    return graph["MST"]
    

def update_heap(graph,heap,spanned_vertex):  
    for edge in graph['vertices'][spanned_vertex]["edges"]:
        
        neighbour = [neighbour for neighbour in graph["edges"][edge]["vertices"] if neighbour != spanned_vertex][0]
        weight = graph["edges"][edge]["weight"]
        
        if graph['vertices'][neighbour]["label"] == "spanned":
            continue
        
        elif graph['vertices'][neighbour]["label"] == "not_spanned":
            
            current_weight,current_edge = graph["explored_vertices"]["not_spanned"][neighbour]
                
            if weight < current_weight:
                heap.delete(heap.indices[(neighbour,current_edge)])
                heap.insert(weight,(neighbour,edge))
                graph["explored_vertices"]["not_spanned"][neighbour] = (weight,edge)
        else:
            heap.insert(weight,(neighbour,edge))
            if (neighbour,edge) == ('132', 'e1264'):
                print "('132', 'e1264') inserted"
            graph["explored_vertices"]["not_spanned"][neighbour] = (weight,edge)
            graph['vertices'][neighbour]["label"] = "not_spanned"
                
        


graph = read_graph("assignment_2_1_3.txt")
MST = prim_MST(graph)
assert MST["cost"] == -3612829.0, "Cost is not equal to -3612829.0"
        