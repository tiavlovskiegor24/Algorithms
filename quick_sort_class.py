from random import randint

class Quick_Sort(object): 
    
    def __init__(self,list,sort_by_index = 0):
        self.sort_by_index = sort_by_index
        self.quick_sort(list)
          

    def swap(self,array,i1,i2):
        swap = array[i1]
        array[i1] = array[i2]
        array[i2] = swap

    
    def partition(self,array,l,r):
        q = l+1 # in case p == l, i.e. the pivot in the first element of array
        for j in range(l+1,r):
    
            if array[j][self.sort_by_index] < array[l][self.sort_by_index]:
                self.swap(array,q,j)
                q += 1
            
        self.swap(array,l,q-1)
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