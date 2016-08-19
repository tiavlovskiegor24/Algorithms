def swap(array,i1,i2):
    swap = array[i1]
    array[i1] = array[i2]
    array[i2] = swap
    
def partition(array,p,l,r):
    q = l+1 # in case p == l, i.e. the pivot in the first element of array
    for j in range(l+1,r):
        if array[j] < array[p]:
            swap(array,q,j)
            q += 1
    swap(array,p,q-1)
    return q

def quick_sort(array,l = 0,r = None):
    
    if r == None:
        r = len(array) 
    
    if r-l <= 1:
        return 
    
    p = l # select the pivot index
    
    # partition the array and return the index of pivot element 
    q = partition(array,p,l,r) 
    
    quick_sort(array,l,q-1)
    quick_sort(array,q,r) 

array = [10,0,5]
quick_sort(array)
print array