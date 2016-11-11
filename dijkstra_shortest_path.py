from heap import *

def reset_labels(graph,reset_value = "Unexplored"):
    for vertex in graph['vertices']:
        graph['vertices'][vertex]['label'] = reset_value

def dijkstra_shortest_path(graph,source):
    #print "\nRunning dijkstra sp...\n"
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    #reset_labels(graph,"Unexplored")
    
    shortest_paths = []
    for i in xrange(n):
        shortest_paths.append(float("inf"))
    
    explored_vertices = {"absorbed":{},"not_absorbed":{}}
    heap = Heap() 
    
    shortest_paths[source-1] = 0
    explored_vertices["absorbed"][source] = 0
    graph['vertices'][source]["label"] = "absorbed"
    
    update_heap(graph,heap,explored_vertices,source,0)
    
    while heap.array:
        
        smallest_score,abs_vertex = heap.extract()
        #print smallest_score,abs_vertex-1
        shortest_paths[abs_vertex-1] = smallest_score 
        
        explored_vertices["absorbed"][abs_vertex] = smallest_score
        del explored_vertices["not_absorbed"][abs_vertex]
        
        graph['vertices'][abs_vertex]["label"] = "absorbed"
        
        update_heap(graph,heap,explored_vertices,abs_vertex,smallest_score)

    return shortest_paths
    

def update_heap(graph,heap,explored_vertices,abs_vertex,abs_vertex_score):  
    for edge in graph['vertices'][abs_vertex]["edges"]:
        
        neighbour = [neighbour for neighbour in graph["edges"][edge]["vertices"] if neighbour != abs_vertex][0]
        score = abs_vertex_score + graph["edges"][edge]["length"]
        
        #if graph['vertices'][neighbour]["label"] == "absorbed":
         #   continue
        if neighbour in explored_vertices["absorbed"]:
            continue
        
        #elif graph['vertices'][neighbour]["label"] == "not_absorbed":
        elif neighbour in explored_vertices["not_absorbed"]:
            
            previous_score = explored_vertices["not_absorbed"][neighbour]
                
            if score < previous_score:
                heap.delete(heap.indices[neighbour])
                heap.insert(score,neighbour)
                explored_vertices["not_absorbed"][neighbour] = float(score)
        else:
            
            heap.insert(score,neighbour)
            explored_vertices["not_absorbed"][neighbour] = score
            graph['vertices'][neighbour]["label"] = "not_absorbed"
            