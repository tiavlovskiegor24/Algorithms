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
    
def reverse_graph(graph):
    
    rev_edges = {}
    rev_vertices = {}
    
    for vertex in graph['vertices']:
        rev_vertices[vertex] = {"edges":[],"label":None}
    
    for edge in graph["edges"]:
        rev_edges[edge] = graph['edges'][edge][::-1]
        tail = rev_edges[edge][0]
        rev_vertices[tail]['edges'].append(edge)
    
    return {"vertices":rev_vertices,"edges":rev_edges}  
    
    
def find_scc_kosaraju(graph):
    
    reset_labels(graph)
    
    n = len(graph["vertices"])
    
    rev_graph = reverse_graph(graph)
    
    rev_graph["finishing_times"] = [None for i in range(n)]
    
    global t
    t = 0
    
    global s
    
    scc = {}
    
    for i in range(1,n+1):
        if rev_graph['vertices'][str(i)]['label'] == None:
            DFS(rev_graph,i,label = "t")
    
    graph["finishing_times"] = rev_graph["finishing_times"]
    print graph["finishing_times"]
    
    for i in range(t,0,-1):
        vertex = graph["finishing_times"][i-1]
        if graph['vertices'][vertex]['label'] == None:
            s = vertex       
            component = DFS(graph,vertex,label = "s")
            if len(component) > 1:
                scc[s] = component
            
    return scc    
            


def DFS(graph,source = None,label = None,reset_labs = False):
    
    global t
    global s
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = "1"
        
    source = str(source)
    
    found_vertices = [source]
    
    if label == "s":
        graph['vertices'][source]["label"] = s   
    else:
        graph['vertices'][source]["label"] = "Explored"
    
    for edge in graph["vertices"][source]['edges']:
        
        #neighbour = [vertex for vertex in graph['edges'][edge] if vertex != source][0]
        neighbour = graph['edges'][edge][1] # for directed graphs
        
        if graph["vertices"][neighbour]['label'] == None:
            found_vertices += DFS(graph,neighbour,label = label)
    
    t += 1
    
    if label == "t":       
        graph['vertices'][source]["label"] = t
        graph["finishing_times"][t - 1] = source
    
    return found_vertices
        
        
neighbours3 = {'1':['2','3',"6"],'2':['4',"7"],'3':['4',"8"],"4":['5'],'5':["1"],'6':['5',"8"],'7':['4'],"8":['5',"1"]} 

neighbours4 = {"1":["2","3"],"2":["4"],"3":["4"],"4":[]}
#graph = read_graph("assignment4.txt")
graph = create_adj_lists(neighbours3.copy(),directed = True)

print find_scc_kosaraju(graph)
    
    
    
    


