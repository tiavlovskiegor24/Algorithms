def median(points):
    for point1 in points:
        for point2 in points:
            for point3 in points:
                if points[point1] < points[point2] and points[point2] < points[point3]:
                    return point2


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

def quick_sort(array,l = 0,r = None):
    global comparisons
    
    if r == None:
        r = len(array) 
    
    if r-l <= 1:
        return 
    
    #p = l # case 1
    #p = r-1 # case 2
    # case 3
    if r-l >= 3:
        p = median({l:array[l],(r-1)-(r-l)/2:array[(r-1)-(r-l)/2],r-1:array[r-1]})
    else:
        p = l
    # partition the array and return the index of pivot element 
    swap(array,p,l)
    q = partition(array,l,r)
    comparisons += r-l-1
    
    quick_sort(array,l,q-1)
    quick_sort(array,q,r) 


with open("assignment2.txt","r") as f:
    array = []
    for line in f:
        array.append(int(line))
    f.closed

comparisons = 0

quick_sort(array)

print comparisons
