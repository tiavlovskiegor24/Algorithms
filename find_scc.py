import sys
sys.setrecursionlimit(5000)
from time import time

def reset_labels(graph,reset_value = "Unexplored"):
    for vertex in graph['vertices']:
        graph['vertices'][vertex]['label'] = reset_value
         

def create_adj_lists(neighbours,directed = False):
    edges = {}
    vertices = {}
    
    for neighbour in neighbours:
        vertices[neighbour] = {"edges":[],"label": "Unexplored"}
    
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
        rev_vertices[vertex] = {"edges":[],"label": "Unexplored"}
    
    for edge in graph["edges"]:
        rev_edges[edge] = graph['edges'][edge][::-1]
        tail = rev_edges[edge][0]
        rev_vertices[tail]['edges'].append(edge)
    
    return {"vertices":rev_vertices,"edges":rev_edges}  
    
    
def find_scc_kosaraju(graph, method = "recursion"):
    
    print "Running kosaraju algorithm using",method,"method.\n"
    #reset_labels(graph)
    
    n = len(graph["vertices"])
    
    time_create_reverse = time()
    print "Creating the reverse graph..."
    rev_graph = reverse_graph(graph)
    print "Reversed graph created in",round(time()-time_create_reverse,3), "seconds.\n"
    
    rev_graph["finishing_times"] = [None for i in range(n)]
    
    global t
    t = 0
    
    global s
    
    global depth
    depth = 0
    
    scc = {}
    
    time_first_DFS = time()
    print "Running the first DFS...\n"
    
    for i in range(n,0,-1):
        
        if rev_graph['vertices'][str(i)]['label'] == "Unexplored":
            
            if method == "recursion":
                DFS(rev_graph,i,label = "t")
            elif method == "stack":
                DFS_stack(rev_graph,i,label = "t")
                
    print "First DFS is finished in",round(time()-time_first_DFS,3),"seconds.\n"
    
    graph["finishing_times"] = rev_graph["finishing_times"]
    
    time_second_DFS = time()
    print "Running the second DFS..."
    
    for i in range(t,0,-1):
        vertex = graph["finishing_times"][i-1]
        if graph['vertices'][vertex]['label'] == "Unexplored":
            s = vertex
            
            if method == 'recursion':       
                component = DFS(graph,vertex,label = "s")
            elif method == 'stack':
                component = DFS_stack(graph,vertex,label = "s")
            
            if len(component) > 0:
                scc[s] = {"vertices":component,"size":len(component)}
    
    print "Second DFS is finished in",round(time()-time_second_DFS,3),"seconds.\n"
            
    return scc    
            

def DFS_stack(graph,source = None,label = None,reset_labs = False):
    
    global t
    global s
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = "1"
        
    source = str(source)
    
    found_vertices = []
    
    S = [source]
    
    if label == "s":
        graph['vertices'][source]["leader"] = s   

    #graph['vertices'][source]["label"] = "Found"
    
    while S:
        v = S[-1]
        
        if graph['vertices'][v]['label'] == "Unexplored":
            
            for edge in graph['vertices'][v]['edges']:
                #neighbour = [vertex for vertex in graph['edges'][edge] if vertex != v][0]
                neighbour = graph['edges'][edge][1] # for directed graphs
                
                if graph['vertices'][neighbour]["label"] == "Unexplored":
                    S.append(neighbour)
                    #graph['vertices'][neighbour]["label"] = "Found"
                    
                    if label == "s":
                        graph['vertices'][neighbour]["leader"] = s
                    
            graph['vertices'][v]['label'] = "Explored"

        if S[-1] == v:
            
            if graph['vertices'][v]['label'] == "Explored":   
                
                if label == "t":
                    t += 1    
                    graph['vertices'][v]["finishing_time"] = t
                    graph["finishing_times"][t - 1] = v
                
                found_vertices.append(v)
                graph['vertices'][v]['label'] = "Finished"
            
            S.pop()
    
    return found_vertices
    

def DFS(graph,source = None,label = None,reset_labs = False):
    
    global t
    global s
    global depth
    depth += 1
    print "Depth = ",depth
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = "1"
        
    source = str(source)
    
    found_vertices = [source]
    
    if label == "s":
        graph['vertices'][source]["leader"] = s   
    
    graph['vertices'][source]["label"] = "Explored"
    
    for edge in graph["vertices"][source]['edges']:
        
        #neighbour = [vertex for vertex in graph['edges'][edge] if vertex != source][0]
        neighbour = graph['edges'][edge][1] # for directed graphs
        
        if graph["vertices"][neighbour]['label'] == "Unexplored":
            found_vertices += DFS(graph,neighbour,label = label)
    
    t += 1
    
    if label == "t":       
        graph['vertices'][source]["label"] = t
        graph["finishing_times"][t - 1] = source
    
    depth -= 1
    return found_vertices
        

def read_graph(filename):
    print "Reading the graph file\n"
    time_reading_graph = time()
    edges = {}
    vertices = {}
    
    with open(filename,"r") as f:
        edge = 1
        for line in f:
            
            line  = line.split()
            edges["e" + str(edge)] = line
            
            if not (line[0] in vertices):
                vertices[line[0]] = {"edges":[],'label':"Unexplored"}    
            vertices[line[0]]['edges'].append("e" + str(edge))
            
            if not (line[1] in vertices):
                vertices[line[1]] = {"edges":[],'label':"Unexplored"}
            
            edge += 1
        f.closed
    
    print "Graph file is read in ",round(time()-time_reading_graph,3),"seconds.\n"
    
    return {"vertices":vertices,"edges":edges}


neighbours3 = {'1':['2','3',"6"],'2':['4',"7"],'3':['4',"8"],"4":['5'],'5':['1'],'6':['5',"8"],'7':['4'],"8":['5',"1"]} 

neighbours4 = {"1":["2","3"],"2":["4"],"3":["4"],"4":[]}
#graph = read_graph("assignment4.txt")

#graph = create_adj_lists(neighbours3.copy(),directed = True)

#print find_scc_kosaraju(graph)


#graph = read_graph("assignment4.txt") 
# correct answer is [434821, 968, 459, 313, 211] 
graph = read_graph("scc_test.txt") 

scc = find_scc_kosaraju(graph,method = 'stack')


scc_sizes = []
for component in scc:
    scc_sizes.append(scc[component]["size"])
print sorted(scc_sizes)[::-1][0:5]
    
    
    


