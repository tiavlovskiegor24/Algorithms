from bellman_ford_sp import *
from dijkstra_shortest_path import *

def find_min(array):
    min_element = array[0]
    min_ind = 0
    for i in xrange(len(array)):
        if array[i] < min_element:
            min_element = array[i]
            min_ind = i
    return min_element,min_ind


def johnson_sp(graph):
    print "\nRunning johnson sp..."
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    A = []
    B = []
    
    graph["vertices"][n+1] = {"edges":[],"label":None}
    for v in xrange(n):
        graph["vertices"][n+1]["edges"].append("to_"+str(v+1))
        #graph["vertices"][v+1]["in_edges"].append("to_"+str(v+1))
        graph["edges"]["to_"+str(v+1)] = {"vertices":[n+1,v+1],"length":float(0)}
    
    #print graph["edges"]
    
    print "\n\tRunning Bellman_Ford..."
    a,b,_ = bellman_ford_push_Q(graph,n+1)
    #print a
    
    for i in xrange(len(a)):
        graph["vertices"][i+1]["p"] = a[i]
    
    min_sp = float("inf")
    for edge in graph["edges"]:
        length = graph["edges"][edge]["length"]
        vertices = graph["edges"][edge]["vertices"]
        graph["edges"][edge]["length"] = length \
            + graph["vertices"][vertices[0]]["p"] \
            - graph["vertices"][vertices[1]]["p"]
        
        #sp =  - graph["vertices"][vertices[0]]["p"] \
         #           + graph["vertices"][vertices[1]]["p"]
    
        #if sp < min_sp:
         #   min_sp = sp
    
    print "\n\tRunning Dijkstra's..."
    
    # for returning shortest path among APSP
    min_sp = float("inf")
    for i in xrange(n):
        #print i
        sp_i = dijkstra_shortest_path(graph,i+1)
        
        for j in xrange(n):
            sp_i[j] = sp_i[j] - graph["vertices"][i+1]["p"] \
                + graph["vertices"][j+1]["p"]
        
        sp,sp_ind = find_min(sp_i)
        if sp < min_sp:
            min_sp = sp
            print "\n\t\tPath %s->%s has min length %s."%(i+1,sp_ind+1,min_sp)
    return min_sp
  
    '''
    # for returning APSP
    for i in xrange(n):
        print i+1
        A.append(dijkstra_shortest_path(graph,i+1))
    
    for i in xrange(n):
        for j in xrange(n):
            A[i][j] = A[i][j] - graph["vertices"][i+1]["p"] \
                        + graph["vertices"][j+1]["p"]
    
    return A,B'''