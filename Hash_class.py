from random import randint

class Hash_table(object):
    
    def __init__(self,n = 1000003):
        self.array = []
        self.n = n
        self.n_param = 4
        self.param = tuple(randint(0,self.n-1) for i in range(self.n_param))
        
        for i in range(self.n):
            self.array.append([])
     
    
    def insert(self,key):
        
        index = self.hash_func(key)
        
        #if key not in [element for element in self.array[index] if element == key]:
        if key not in self.array[index]:
            self.array[index].append(key)
            
    
    def delete(self,key):
        
        index = self.hash_func(key)
        
        self.array[index] = [element for element in self.array[index] if element != key]
        
        return key
    
    def look_up(self,key):
        
        index = self.hash_func(key)
        
        #if key in [element for element in self.array[index] if element == key]:
        if key in self.array[index]:
            return key
        else:
            return False
     
    def output_elements(self):
         
        elements = []    
        for bucket in self.array:
            for element in bucket:
                elements.append(element)
                
        return elements
            
    
    def hash_func(self,key):
        index = 0
        window = len(key)/self.n_param + 1
        
        for i in range(len(self.param)): 
 
            if len(key[:len(key)-window*i]) > window:
                x = int(key[:len(key)-window*i][-window:])
                    
                index += self.param[i]*x
                
                if key[:len(key)-window*i][-(window+1)] in ["-",""]:
                    break
            
            else:
                x = abs(int(key[:len(key)-window*i]))
                index += self.param[i]*x
                break     
            
        index = index % self.n
        
        return index