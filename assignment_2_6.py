import sys
sys.setrecursionlimit(5000)
from time import time

def reset_labels(graph,reset_value = "Unexplored"):
    for vertex in graph['vertices']:
        graph['vertices'][vertex]['label'] = reset_value
    
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
    
    rev_graph["finishing_times"] = [None for i in xrange(n)]
    
    global t
    t = 0
    
    global s
    
    global depth
    depth = 0
    
    scc = []
    
    time_first_DFS = time()
    print "Running the first DFS...\n"
    
    for vertex in graph["vertices"]:
        
        if rev_graph['vertices'][vertex]['label'] == "Unexplored":
            
            if method == "recursion":
                DFS(rev_graph,vertex,label = "t")
            elif method == "stack":
                DFS_stack(rev_graph,vertex,label = "t")
                
    print "First DFS is finished in",round(time()-time_first_DFS,3),"seconds.\n"
    
    graph["finishing_times"] = rev_graph["finishing_times"][:]
    
    del rev_graph
    
    time_second_DFS = time()
    print "Running the second DFS..."
    
    #for i in xrange(t,0,-1):
    for vertex in graph["finishing_times"][::-1]:
        #vertex = graph["finishing_times"][i-1]
        if graph['vertices'][vertex]['label'] == "Unexplored":
            s = vertex
            
            if method == 'recursion':       
                component = DFS(graph,s,label = "s")
            elif method == 'stack':
                component = DFS_stack(graph,s,label = "s")
            
            if len(component) > 0:
                scc.append({"vertices":component,"leader":s,"size":len(component)})
    
    print "Second DFS is finished in",round(time()-time_second_DFS,3),"seconds.\n"
            
    return scc[::-1]   
            

def DFS_stack(graph,source = None,label = None,reset_labs = False):
    
    global t
    global s
    
    if reset_labs:
        reset_labels(graph)
    
    if source == None:
        source = 1
    
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
        source = 1
    
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
        next(f)
        for line in f:
            
            edge1  = [int(literal) for literal in line.split()]
            edge2 = edge1[::-1]
            edge1[0] = -edge1[0]
            edge2[0] = -edge2[0]
            #print line
            edges["e" + str(edge)] = edge1
            
            if edge1[0] not in vertices:
                vertices[edge1[0]] = {"edges":[],'label':"Unexplored"}  
            vertices[edge1[0]]['edges'].append("e" + str(edge))
            
            if edge1[1] not in vertices:
                vertices[edge1[1]] = {"edges":[],'label':"Unexplored"}
            
            edge += 1
            
            edges["e" + str(edge)] = edge2
            if edge2[0] not in vertices:
                vertices[edge2[0]] = {"edges":[],'label':"Unexplored"}  
            vertices[edge2[0]]['edges'].append("e" + str(edge))
            
            if edge2[1] not in vertices:
                vertices[edge2[1]] = {"edges":[],'label':"Unexplored"}
            
            edge += 1
    
    print "Graph file is read in ",round(time()-time_reading_graph,3),"seconds.\n"
    
    return {"vertices":vertices,"edges":edges}

def check_sat(graph,scc):
    sat_table = {}
    
    for i in xrange(len(scc)):
        leader = scc[i]["leader"]
        if leader not in sat_table:
            sat_table[leader] = False
            
        for vertex in scc[i]["vertices"]:
            opp_leader = graph["vertices"][-vertex]["leader"]
            if opp_leader not in sat_table:
                sat_table[opp_leader] = not sat_table[leader]
            else:
                if sat_table[opp_leader] == sat_table[leader]:
                    print "Problem is Unsatisfiable\n"
                    return
    print "Problem is Satisfiable\n"
 
graph = read_graph("2sat_test.txt") 
scc = find_scc_kosaraju(graph,method = 'stack')
check_sat(graph,scc)
        
'''for i in xrange(1,7):
    graph = read_graph("2sat"+str(i)+".txt") 
    scc = find_scc_kosaraju(graph,method = 'stack')
    print "Problem ",i
    check_sat(graph,scc)'''