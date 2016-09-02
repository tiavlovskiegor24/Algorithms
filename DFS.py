def reset_labels(graph,reset_value = None):
    for vertex in graph['vertices']:
         graph['vertices'][vertex]['label'] = reset_value
         

def create_adj_lists(neighbours,directed = False):
    edges = {}
    vertices = {}
    
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
    
    return {"vertices":vertices,"edges":edges}   
    
def DFS(graph,source = None,reset_labs = False):
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = "1"
        
    source = str(source)
    
    if graph['vertices'][source]["label"] == None:
         graph["vertices"][source]['label'] = 0
    
    found_vertices = [source]
    
    for edge in graph["vertices"][source]['edges']:
        neighbour = [vertex for vertex in graph['edges'][edge] if vertex != source][0]
        if graph["vertices"][neighbour]['label'] == None:
            graph['vertices'][neighbour]["label"] = graph['vertices'][source]["label"] + 1
            found_vertices += DFS(graph,neighbour)
            
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

neighbours = read_vertices("assignment3.txt")

neighbours1 = {"1":["2","7","8"],'2':['1','7','3'],'3':['2','6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3','7'],\
                '7':['1','2','6','8'],'8':['1','7']}

neighbours2 = {"1":["2","7","8"],'2':['1','7'],'3':['6','5','4'],\
                '4':['3','6','5'],'5':['3','4','6'],'6':['5','4','3'],\
                '7':['1','2','8'],'8':['1','7']}
                
#neighbours3 = {'1':['2','3'],'2':['4'],'3':['4'],"4":[]}
                

#graph = create_adj_lists(neighbours3.copy(),directed = True)

#print DFS(graph,8)

#print graph['vertices']


