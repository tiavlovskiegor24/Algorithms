from random import randint

def swap(array,i1,i2):
    swap = array[i1]
    array[i1] = array[i2]
    array[i2] = swap
    
def partition(array,l,r):
    q = l+1 # in case p == l, i.e. the pivot in the first element of array
    for j in range(l+1,r):
        if array[j] < array[l]:
            swap(array,q,j)
            q += 1
    swap(array,l,q-1)
    return q

# find the ith statistic of the array, medium as default
def r_select(array,x_i = None,l = 0,r = None):
    
    if x_i == None:
        x_i = len(array)/2       
    
    if r == None:
        r = len(array) 
    
    if r-l < 1:
        return None 
    
    p = randint(l,r-1) # select the pivot index randomly
    
    # partition the array and return the index of pivot element 
    swap(array,p,l)
    q = partition(array,l,r) 
    
    if q-1 == x_i-1:
        return array[q-1]
    elif q-1 > x_i-1:
        return r_select(array,x_i,l,q-1)
    elif q-1 < x_i-1:
        return r_select(array,x_i,q,r)
    else:
        return None 
    

array = [10,0,5,4,0.1,-7,0,-5,5,9,-20,100]
print array
for i in range(len(array)):
    print r_select([element for element in array],i+1)
print "Median is:", r_select([element for element in array])