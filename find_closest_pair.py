import numpy as np

def swap(array,i1,i2):

    swap = [point for point in array[i1]]
    array[i1] = array[i2]
    array[i2] = swap

def test_swap():   
    points = [[0,5.5],[-1,20.6],[-5,100],[-60,35],[-1,20],[0,7],[10,10]]
    points = np.array(points)
    
    swap(points,0,1)
    swap(points,2,4)
    
    expected = np.array([[-1,20.6],[0,5.5],[-1,20],[-60,35],[-5,100],[0,7],[10,10]])
    assert (points == expected).all(), "swap is not working"
test_swap()     
  
def partition(array,p,l,r,dim = 0):
    split_index = l+1 # in case p == l, i.e. the pivot in the first element of array
    for j in range(l+1,r):
        if array[j,dim] < array[p,dim]:
            swap(array,split_index,j)
            split_index += 1
    swap(array,p,split_index-1)
    
    return split_index

def test_pivot_ends_up_where_we_expect():
    points = np.array([[5],[4],[1],[6]])
    
    split_index_returned = partition(points,0,0,len(points))
    assert split_index_returned == 3, split_index_returned
test_pivot_ends_up_where_we_expect()
    
    
def test_partition():
    points = [[0,5.5],[-1,20.6],[-5,100],[-60,35],[-1,20],[0,7],[10,10]]
    points = np.array(points)

    partition(points,0,0,len(points))
    expected = np.array([[-1,20],[-1,20.6],[-5,100],[-60,35],[0,5.5],[0,7],[10,10]])

    assert (points == expected).all(), "partition is not working"
test_partition()


def quick_sort_points(points,l = 0,r = None,dim = 0):
    
    if r == None:
        r = len(points) 

    if r-l <= 1:
        return 
    pivot = l # select the pivot index
    
    # partition the array and return the split index
    q = partition(points,pivot,l,r,dim)
    
    quick_sort_points(points,l,q-1,dim)
    quick_sort_points(points,q,r,dim) 
    
def test_quick_sort_points():
    points = [[0,5.5],[-1,20.6],[-5,100],[-60,35],[-1,20],[0,7],[10,10]]
    points = np.array(points)

    quick_sort_points(points,l = 0,r = len(points))
    
    expected = np.array([[-60,35],[-5,100],[-1,20],[-1,20.6],[0,5.5],[0,7],[10,10]])
    
    assert (points == expected).all()
test_quick_sort_points()
    


def split_points(x_sorted,y_sorted):
    
    n = len(y_sorted)
    
    split_index = n/2
    while (x_sorted[split_index,0] == x_sorted[split_index+1,0] and split_index < n - 2):
        split_index += 1
    
    q_x = x_sorted[0:split_index + 1]
    r_x = x_sorted[split_index + 1:n]
    
    q_y = np.zeros(q_x.shape)
    r_y = np.zeros(r_x.shape)
    
    q = 0
    r = 0
    for i in range(0,n):
        if y_sorted[i,0] <= q_x[-1,0] and q < len(q_x):
            q_y[q] = y_sorted[i]
            q += 1
        else:
            r_y[r] = y_sorted[i]
            r += 1
    
    return q_x,q_y,r_x,r_y
    
def test_split_points():
    x_sorted = np.array([[-60,35],[-5,100],[-1,20],[-1,20.6],[0,5.5],[0,7],[10,10]])
    y_sorted = np.array([[0,5.5],[0,7],[10,10],[-1,20],[-1,20.6],[-60,35],[-5,100]])
    
    q_x,q_y,r_x,r_y = split_points(x_sorted,y_sorted)
    assert (q_x == np.array([[-60,35],[-5,100],[-1,20],[-1,20.6]])).all()
    assert (r_x == np.array([[0,5.5],[0,7],[10,10]])).all()
    assert (q_y == np.array([[-1,20],[-1,20.6],[-60,35],[-5,100]])).all(),q_y
    assert (r_y == np.array([[0,5.5],[0,7],[10,10]])).all(),r_y
test_split_points()

  
def dist(point1,point2):
    
    dist = 0
    dim = 2
    
    for i in range(0,dim):
        dist += (point1[i]-point2[i])**2
        
    dist = np.sqrt(dist)
    return dist
    
def closest_pair_brute(points):
    
    n = len(points)
    if n < 2:
        return None,float("inf")
    
    closest_pair = [points[0],points[1]]
    min_dist = dist(points[0],points[1])
    
    for i in range(n):
        for j in range(i+1,n): 
            if dist(points[i],points[j]) < min_dist:
                closest_pair = [points[i],points[j]]
                min_dist = dist(points[i],points[j])
    
    return closest_pair,min_dist

def find_closest_split_pair(x_sorted,y_sorted,delta):
    
    n = len(y_sorted)
    
    filter_point = [point for point in y_sorted \
        if point[0] > x_sorted[-1,0] - delta and point[0] < x_sorted[-1,0] + delta]
    
    if len(filter_point) < 2:
        return None, float("inf")
        
    closest_split_pair = [filter_point[0],filter_point[1]]
    min_dist = dist(filter_point[0],filter_point[1])
    
    if len(filter_point) < 9:
        return closest_pair_brute(filter_point)
        
    for i in range(0,len(filter_point)-8):
        for j in range(1,7):
            if dist(filter_point[i],filter_point[j]) < min_dist:
                closest_split_pair = [filter_point[i],filter_point[j]]
                min_dist = dist(filter_point[i],filter_point[j])
    
    return closest_split_pair,min_dist

def find_closest_pair(points,points_sorted = []):
    
    if type(points) != type(np.array([0])):
        print "Input is not numpy array"
        return 
        
    n = len(points)
    
    if n <= 1:
        print "Only one or no points. There are no distances to calculate"
        return None, float("inf")
    
    points = np.array(points)
    points_sorted = np.array(points_sorted)

    if n <= 3:
        return closest_pair_brute(points)
    
    if not points_sorted.size:
        x_sorted = [point for point in points]
        x_sorted = np.array(x_sorted)
        quick_sort_points(x_sorted,0)
        
        y_sorted = [point for point in points]
        y_sorted = np.array(y_sorted)
        quick_sort_points(y_sorted,1)
    else:
        x_sorted = points
        y_sorted = points_sorted
    
    q_x,q_y,r_x,r_y = split_points(x_sorted,y_sorted)
    
    closest_left_pair,min_left_dist = find_closest_pair(q_x,q_y)
    closest_right_pair,min_right_dist = find_closest_pair(r_x,r_y)
    

    if min_left_dist > min_right_dist:
        closest_pair = closest_right_pair
        min_dist = min_right_dist
    elif min_left_dist < min_right_dist:
        closest_pair = closest_left_pair
        min_dist = min_left_dist
    else:
        closest_pair = closest_right_pair
        min_dist = min_right_dist   
        
    closest_split_pair,min_split_dist = find_closest_split_pair(x_sorted,y_sorted,min_dist)
    
    if min_split_dist < min_dist and min_split_dist != None:
        closest_pair = closest_split_pair
        min_dist = min_split_dist
        print "Split pair is chosen"
    
    return closest_pair,min_dist
   
points = [[0,5.5],[-1,20.6],[-5,100],[-60,35],[-1,15],[0,70.1],[10,10],[0,0],[-10,15]]
#points = [[0,0],[1,1],[1,1.5],[1,1.3]]
#point = []
points = np.array(points)
print type(points)

print find_closest_pair(points)
print closest_pair_brute(points)



    