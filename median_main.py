from heap import *

upper = Heap("min")
lower = Heap("max")

def read_file(filename):
    with open(filename,"r") as f:
        s = 0
        medians = []
        for element in f:
            
            element = float(element)
            
            if not lower.array:
                lower.insert((element,element))
                s += element
                medians.append(element)
                continue
                
            if element <= lower.array[0].value:
                lower.insert((element,element))
            else:
                upper.insert((element,element))            
                
            if len(lower.array)-len(upper.array) > 1:
                upper.insert(lower.extract())
            
            if len(upper.array)-len(lower.array) > 0:
                lower.insert(upper.extract())
                
            s += lower.array[0].value
            medians.append(lower.array[0].value)
    
    return s, medians
    
s,medians = read_file("assignment6_2.txt")

print s % 10000
                