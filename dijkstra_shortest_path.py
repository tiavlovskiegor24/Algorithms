class Heap_element(object):
    
    def __init__(self,key,id):
        self.key = key
        self.id = id
        self.index = None

class Heap(object):
    
    def __init__(self,mode = "min"):
        self.array = []
        self.mode = mode
        self.indices = {}
        
    def print_array(self):
        for element in self.array:
            print (element.key,element.id)
    
    def insert(self,key,id):
        
        if self.mode == 'min':
            new_element = Heap_element(float(key),id)
            self.array.append(new_element)
        elif self.mode == 'max':
            new_element = Heap_element(-float(key),id)
            self.array.append(new_element)
            
        return self.bubble_up(len(self.array)-1) 
            
    
    def bubble_up(self,index):    
        if self.array[index].key < self.array[int(index/2)].key:
            self.swap(index,int(index/2))
            return self.bubble_up(int(index/2))
        else:
            self.indices[self.array[index].id] = index
            self.array[index].index = index
            return index
            
    def bubble_down(self,index):
        
        parent_key = self.array[index].key
        
        if index*2 < len(self.array):
            child_1_key = self.array[index*2].key
        else:
            child_1_key = float("inf")
        
        if index*2+1 < len(self.array):
            child_2_key = self.array[index*2+1].key
        else:
            child_2_key = float("inf")
            
        if child_1_key > child_2_key:
            if parent_key > child_2_key:
                self.swap(index,index*2+1)
                return self.bubble_down(index*2+1)
            else:
                self.indices[self.array[index].id] = index
                self.array[index].index = index
                return index
        else:
            if parent_key > child_1_key:
                self.swap(index,index*2)
                return self.bubble_down(index*2)
            else:
                self.indices[self.array[index].id] = index
                self.array[index].index = index
                return index
                
            
    def swap(self,index1,index2):
        s = self.array[index1]

        self.array[index1] = self.array[index2]  
        self.array[index2] = s
        
        self.indices[self.array[index1].id] = index1
        self.array[index1].index = index1
        self.indices[self.array[index2].id] = index2
        self.array[index1].index = index1
    
    def extract(self):
        if len(self.array) == 0:
            print "No more elements in the heap"
            return None
            
        if len(self.array) == 1:
            element = self.array.pop()
            del self.indices[element.id]
        else:
            element = self.array[0]
            del self.indices[element.id]
            self.array[0] = self.array.pop()
            self.bubble_down(0)
        
        if self.mode == 'min':
            return element.key,element.id
        elif self.mode == 'max':
            return -element.key,element.id
        
    def delete(self,index):
        if index > len(self.array)-1 or index < 0:
            print "Index out of range"
            return
            
        if index == len(self.array)-1:
             element = self.array.pop()
             del self.indices[element.id]
             return 
        
        element = self.array[index]
        del self.indices[element.id]
        self.array[index] = self.array.pop()
        self.bubble_up(index)
        self.bubble_down(index)

def reset_labels(graph,reset_value = "Unexplored"):
    for vertex in graph['vertices']:
        graph['vertices'][vertex]['label'] = reset_value
             
def read_graph(filename):
    
    edges = {}
    vertices = {}
    neighbours = {}
    
    with open(filename,"r") as f:
        for line in f:
            
            line  = line.split()
            vertex = line[0]
            neighbours[vertex] = line[1:]
            vertices[vertex] = {"edges":[],"label":None}
            
        f.closed
    
    edge = 1
    for vertex in neighbours:
        for neighbour in neighbours[vertex]:
            neighbour = neighbour.split(",")
            edges["e" + str(edge)] = {"vertices":[vertex,neighbour[0]],"weight":neighbour[1]}
            vertices[vertex]["edges"].append("e" + str(edge)) 
            vertices[neighbour[0]]["edges"].append("e" + str(edge))
            neighbours[neighbour[0]] = [remains for remains in neighbours[neighbour[0]] if remains[0] != vertex]
            edge += 1
    
    return {"vertices":vertices,"edges":edges}  
    
def dijkstra_shortest_path(graph,source):
    
    reset_labels(graph,"Unexplored")
    
    shortest_paths = {}
    explored_vertices = {"absorbed":{},"not_absorbed":{}}
    heap = Heap()
    
    for vertex in graph["vertices"]:
        shortest_paths[vertex] = 1000000 
    
    shortest_paths[source] = 0
    explored_vertices["absorbed"][source] = 0
    graph['vertices'][source]["label"] = "absorbed"
    
    update_heap(graph,heap,explored_vertices,source,0)
    
    while heap.array:
        
        smallest_score,abs_vertex = heap.extract()
        shortest_paths[abs_vertex] = smallest_score 
        
        explored_vertices["absorbed"][abs_vertex] = smallest_score
        del explored_vertices["not_absorbed"][abs_vertex]
        
        graph['vertices'][abs_vertex]["label"] = "absorbed"
        
        update_heap(graph,heap,explored_vertices,abs_vertex,smallest_score)

    return shortest_paths
    

def update_heap(graph,heap,explored_vertices,abs_vertex,abs_vertex_score):  
    for edge in graph['vertices'][abs_vertex]["edges"]:
        
        neighbour = [neighbour for neighbour in graph["edges"][edge]["vertices"] if neighbour != abs_vertex][0]
        score = abs_vertex_score + float(graph["edges"][edge]["weight"])
        
        if graph['vertices'][neighbour]["label"] == "absorbed":
            continue
        
        elif graph['vertices'][neighbour]["label"] == "not_absorbed":
            
            previous_score = explored_vertices["not_absorbed"][neighbour]
                
            if score < previous_score:
                heap.delete(heap.indices[neighbour])
                heap.insert(score,neighbour)
                explored_vertices["not_absorbed"][neighbour] = float(score)
        else:
            
            heap.insert(score,neighbour)
            explored_vertices["not_absorbed"][neighbour] = float(score)
            graph['vertices'][neighbour]["label"] = "not_absorbed"
                
        

graph = read_graph("assignment5.txt") 
#graph = read_graph("test5.txt")
shortest_paths = dijkstra_shortest_path(graph,"1")

sample = [7,37,59,82,99,115,133,165,188,197]

output = []
for item in sample:
    output.append(int(shortest_paths[str(item)]))
print output

if output == [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]:
    print "Algorithm works"
    

test = Heap()

test.insert(0,"0")
for key in [-1,5,100,3.5]:
    test.insert(key,str(key))
    

        