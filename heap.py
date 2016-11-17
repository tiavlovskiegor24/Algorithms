class Heap_element(object):
    
    def __init__(self,(key,value)):
        self.key = key
        self.value = value
        self.index = None

class Heap(object):
    
    def __init__(self,mode = "min"):
        if mode == "min":
            #self.array = [Heap_element((-float("inf"),None))]
            self.array = []
        elif mode == "max":
            #self.array = [Heap_element((float("inf"),None))]
            self.array = []
        else:
            print "Mode has to be either 'min' or 'max'.\n"
            return
        self.mode = mode
        self.indices = {}
        
    def print_array(self):
        for element in self.array:
            print (element.key,element.value)
    
    def heapify(self,array):
        n = len(array)
        if n == 0:
            print "\nEmpty list passed"
            return
        
        if self.mode == 'min':
            for i in xrange(n):
                key,value = array[i]
                new_element = Heap_element((float(key),value))
                self.array.append(new_element)
        elif self.mode == 'max':
            for i in xrange(n):
                key,value = array[i]
                new_element = Heap_element((-float(key),value))
                self.array.append(new_element)
        
        last_index = n-1
        
        if last_index == 0:
            return       
        elif last_index % 2 == 0:
            parent = int((last_index-2)/2)
        else:
            parent = int((last_index-1)/2)

        for i in xrange(parent,-1,-1):
            self.bubble_down(i)
    
    def insert(self,key,value):
        
        if self.mode == 'min':
            new_element = Heap_element((float(key),value))
            self.array.append(new_element)
        elif self.mode == 'max':
            new_element = Heap_element((-float(key),value))
            self.array.append(new_element)
            
        return self.bubble_up(len(self.array)-1) 
            
    def bubble_up(self,index): 
        
        if index == 0:
            parent = index
        elif index % 2 == 0:
            parent = int((index-2)/2)
        else:
            parent = int((index-1)/2)
            
        #print "Bubble up",index,parent
        #if self.array[index].key < self.array[int(index/2)].key:
        if self.array[index].key < self.array[parent].key:    
            self.swap(index,parent)
            return self.bubble_up(parent)
        else:
            self.indices[self.array[index].value] = index
            self.array[index].index = index
            return index
            
    def bubble_down(self,index):
        
        parent_key = self.array[index].key
        
        if index*2+1 < len(self.array):
            child_1_key = self.array[index*2+1].key
        else:
            child_1_key = float("inf")
        
        if index*2+2 < len(self.array):
            child_2_key = self.array[index*2+2].key
        else:
            child_2_key = float("inf")
            
        if child_1_key > child_2_key:
            if parent_key > child_2_key:
                self.swap(index,index*2+2)
                return self.bubble_down(index*2+2)
            else:
                self.indices[self.array[index].value] = index
                self.array[index].index = index
                return index
        else:
            if parent_key > child_1_key:
                self.swap(index,index*2+1)
                return self.bubble_down(index*2+1)
            else:
                self.indices[self.array[index].value] = index
                self.array[index].index = index
                return index
                
            
    def swap(self,index1,index2):
        s = self.array[index1]

        self.array[index1] = self.array[index2]  
        self.array[index2] = s
        
        self.indices[self.array[index1].value] = index1
        self.array[index1].index = index1
        self.indices[self.array[index2].value] = index2
        self.array[index1].index = index1
    
    def extract(self):
        if len(self.array) == 0:
            print "No more elements in the heap"
            return None
            
        if len(self.array) == 1:
            element = self.array.pop()
            del self.indices[element.value]
        else:
            element = self.array[0]
            del self.indices[element.value]
            self.array[0] = self.array.pop()
            self.bubble_down(0)
        
        if self.mode == 'min':
            return (element.key,element.value)
        elif self.mode == 'max':
            return (-element.key,element.value)
        
    def delete(self,index):
        if index > len(self.array)-1 or index < 0:
            print "Index out of range"
            return
            
        if index == len(self.array)-1:
             element = self.array.pop()
             del self.indices[element.value]
             return 
        
        element = self.array[index]
        del self.indices[element.value]
        self.array[index] = self.array.pop()
        self.bubble_up(index)
        self.bubble_down(index)
        
    def change_key(self,index,new_key):
        if index > len(self.array)-1 or index < 0:
            print "Index out of range"
            return
            
        if index == len(self.array)-1:
             old_element = self.array.pop()
             
             if self.mode == 'min':
                 new_element = Heap_element((float(new_key),old_element.value))
                 self.array.append(new_element)
             elif self.mode == 'max':
                 new_element = Heap_element((-float(new_key),old_element.value))
                 self.array.append(new_element)
                 
             return 
        
        old_element = self.array[index]
        
        if self.mode == 'min':
            new_element = Heap_element((float(new_key),old_element.value))
            self.array[index] = new_element
        elif self.mode == 'max':
            new_element = Heap_element((-float(new_key),old_element.value))
            self.array[index] = new_element
        
        self.bubble_up(index)
        self.bubble_down(index)


def test_heapify():
    import numpy as np
    array = np.random.randint(0,10,200)
    array_for_heap = zip(array,np.zeros_like(array))
    #print array_for_heap
    h = Heap()
    #for i in array:
     #   h.insert(i,i)
    h.heapify(array_for_heap)
    
    for i in xrange(len(array)):
        key,v = h.extract()
        assert key == np.sort(array)[i]
        #print key,np.sort(array)[i]
        if key != np.sort(array)[i]:
            print "Oops"
    
test_heapify() 
