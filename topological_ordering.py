def reset_labels(graph,reset_value = None):
    for vertex in graph['vertices']:
         graph['vertices'][vertex]['label'] = reset_value
         

def create_adj_lists(neighbours,directed = False):
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
            if not directed: # only for the undirected graphs
                vertices[neighbour]["edges"].append("e" + str(edge)) 
                neighbours[neighbour] = [remains for remains in neighbours[neighbour] if remains != vertex]
            edge += 1
    
    graph["vertices"] = vertices
    graph["edges"] = edges    
    
    return graph  


def topological_ordering(graph):
    
    reset_labels(graph)
    
    n = len(graph['vertices'])
    graph["topological_ordering"] = [0 for i in range(n)]
    
    global current_label
    
    current_label = n
    
    for vertex in graph['vertices']:
        if graph['vertices'][vertex]["label"] == None:
             DFS(graph,vertex)
    
    return graph["topological_ordering"]

    
def DFS(graph,source = None,reset_labs = False):
    
    global current_label
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = "1"
        
    source = str(source)
    
    found_vertices = [source]
    graph['vertices'][source]["label"] = "Explored"
    
    for edge in graph["vertices"][source]['edges']:
        
        #neighbour = [vertex for vertex in graph['edges'][edge] if vertex != source][0]
        neighbour = graph['edges'][edge][1]
        
        if graph["vertices"][neighbour]['label'] == None:
            found_vertices += DFS(graph,neighbour)
            
    graph['vertices'][source]["label"] = current_label
    graph["topological_ordering"][current_label - 1] = source
    
    current_label -= 1
    
    return found_vertices
    
neighbours3 = {'1':['2','3',"6"],'2':['4',"7"],'3':['4',"8"],"4":['5'],'5':[],'6':['5',"8"],'7':['4'],"8":['5']}
                

graph = create_adj_lists(neighbours3.copy(),directed = True)

topological_ordering(graph)

print graph['vertices']
print graph["topological_ordering"]
