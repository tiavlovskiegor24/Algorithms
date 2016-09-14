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


def read_graph(filename):
    
    edges = {}
    vertices = {}
    
    with open(filename,"r") as f:
        edge = 1
        for line in f:
            
            line  = line.split()
            edges["e" + str(edge)] = line
            
            if not (line[0] in vertices):
                vertices[line[0]] = []    
            vertices[line[0]].append(line[1])
            
            if not (line[1] in vertices):
                vertices[line[1]] = []
            
            edge += 1
        f.closed
    
    return {"vertices":vertices,"edges":edges}
#graph = read_graph("assignment4.txt")    


neighbours3 = {'1':['2','3',"6"],'2':['4',"7"],'3':['4',"8"],"4":['5'],'5':[],'6':['5',"8"],'7':['4'],"8":['5']} 

graph = create_adj_lists(neighbours3.copy(),directed = True)

print graph["vertices"]['1']

