class Edge(object):
    
    def __init__(vertices,weight = None):
        self.vertices = vertices
        self.weight = weight

class Vertex(object):
    
    def __init__(edges,label):
        self.edges = edges
        self.label = label

class Graph(object):
    
    def __init__(graph,type = "undirected"):
        self.type = type
        self.vertices = graph["vertices"]
        self.edges = graph["edges"]
    
    def sort_by_score(self):

class quick_sort(object): 
    
    def __init__(self,list,by = 0):
        self.by = by
        self.quick_sort(list)
          

    def swap(self,array,i1,i2):
        swap = array[i1]
        array[i1] = array[i2]
        array[i2] = swap

    def partition(self,array,l,r):
        q = l+1 # in case p == l, i.e. the pivot in the first element of array
        for j in range(l+1,r):
    
            if array[j][self.by] < array[l][self.by]:
                self.swap(array,q,j)
                q += 1
            
        swap(array,l,q-1)
        return q

    def quick_sort(self,array,l = 0,r = None):

        if r == None:
            r = len(array) 

        if r-l <= 1:
            return 

        p = randint(l,r-1) # select the pivot index

        # partition the array and return the index of pivot element 
        self.swap(array,p,l)
        q = self.partition(array,l,r) 

        self.quick_sort(array,l,q-1)
        self.quick_sort(array,q,r) 

