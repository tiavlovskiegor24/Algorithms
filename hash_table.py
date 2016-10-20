from random import randint
from time import time

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
        
        if key not in [element for element in self.array[index] if element == key]:
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
        

def read_file_in_hash(filename,h_table):
    with open(filename,"r") as f:
        i = 1
        for element in f:
            if i > 10000000:
                break
            h_table.insert(element.strip("\n"))
            i += 1
            
def read_file(filename):
    with open(filename,"r") as f:
        i = 1
        elements = []
        for element in f:
            if i > 10000000:
                break
            elements.append(int(element.strip("\n")))
            i += 1
    return elements
                    

t_h_table = time()        
h_table = Hash_table()
print - t_h_table + time()

t_read = time()
elements = read_file("assignment6_1.txt")
read_file_in_hash("assignment6_1.txt",h_table)
print - t_read + time()

'''
buckets = {}
for i in range(len(h_table.array)):
    if len(h_table.array[i]) not in buckets:
         buckets[len(h_table.array[i])] = 1
    else:
        buckets[len(h_table.array[i])] += 1
    
    if len(h_table.array[i]) > 8:
        print h_table.array[i]
    
for bucket in buckets:
    print bucket,buckets[bucket] '''

from quick_sort import *
print "Sorting the array..."
quick_sort(elements)
print "Array sorted."

print elements[50000]

from two_sum_alg import *   

target_values,count = two_sum_alg2(range(-10000,10001),elements)

assert count == 427, "Answer should be 427"

targets = []
for i in range(len(target_values)):
    if target_values[i]:
        targets.append(i-10000)

target_values1,count1 = two_sum_alg(targets,h_table)

assert count1 == 427, "Answer should be 427"

if target_values == target_values1:
    print "Hurai!"
else:
    print "Oh no!"
         