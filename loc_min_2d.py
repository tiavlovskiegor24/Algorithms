def print_neighbours(matrix,(i,j)):
    print matrix[i-1:i+2,j-1:j+2]

def global_min(matrix,rows = None,cols = None,include_margins = True):
    
    m,n = matrix.shape
    
    if rows == None:
        rows = (1,int(m/2),m-2)
        
    if cols == None:
        cols = (1,int(n/2),n-2)
    
    rows_range = (rows[0],rows[-1]+1)
    cols_range = (cols[0],cols[-1]+1)
    
    if not include_margins:
        rows = rows[1:-1]
        cols = cols[1:-1]
    
    min_v = float("inf")
    min_ind = () 
    
    for i in rows:
        for j in range(cols_range[0],cols_range[1]):
            #plt.scatter(x[j],y[i])
            if matrix[i,j] < min_v:
                min_v = matrix[i,j]
                min_ind = (i,j)
            
    for j in cols:
        for i in range(rows_range[0],rows_range[1]):
            #plt.scatter(x[j],y[i])
            if matrix[i,j] < min_v:
                min_v = matrix[i,j]
                min_ind = (i,j)
   
    return min_ind

def check_smaller_neighbours(matrix,rows,cols,(min_i,min_j)):
    
    smallest_neighbour = float("inf")
    smallest_neighbour_ind = ()
    
    for i in range(min_i-1,min_i+2):
        if i > rows[-1] and i < rows[0]:
            continue
        for j in range(min_j-1,min_j+2):
            if j > cols[-1] and j < cols[0]:
                continue
            if matrix[i,j] < matrix[min_i,min_j]:
                if matrix[i,j] < smallest_neighbour:
                    smallest_neighbour = matrix[i,j]
                    smallest_neighbour_ind = (i,j)
    
    if smallest_neighbour < float("inf"):
        return smallest_neighbour_ind
    else:
        return False
    
global memory
memory = {}
memory["frame_mins"] = []

def local_min_rec(matrix,rows = None,cols = None):
    
    global memory
    
    m,n = matrix.shape # n is the number of rows, m is a number of columns
    
    if rows == None:
        include_margins = True
        rows = (1,m-2)
    else:
        include_margins = True
        
        
    if cols == None:
        cols = (1,n-2)
    
    memory.append((rows[1]-rows[0]+1,cols[1]-cols[0]+1))
    
    rows_range = rows[1]-rows[0]+1
    rows_margin = int(1./3*rows_range)
    
    if rows_range > 5:
        mid_row = randint(rows[0]+rows_margin,rows[1]-rows_margin)
    elif rows_range == 5:
        mid_row = rows[0]+2
    else:
        min_ind = global_min(matrix,range(rows[0],rows[1]+1),range(cols[0],cols[1]+1),True)
        found = check_smaller_neighbours(matrix,rows,cols,min_ind)
    
        if not found:
            return matrix[min_ind],min_ind
        else: 
            print memory
            plt.scatter(x[min_ind[1]],y[min_ind[0]],color = "black")
            return None,(None,None)
    
    cols_range = cols[1] - cols[0] + 1
    cols_margin = int(1./3*cols_range)
    
    if cols_range > 5:
        mid_col = randint(cols[0]+cols_margin,cols[1]-cols_margin)
    elif cols_range == 5:
        mid_col = cols[0]+2
    else:
        min_ind = global_min(matrix,range(rows[0],rows[1]+1),range(cols[0],cols[1]+1),True)
        
        found = check_smaller_neighbours(matrix,rows,cols,min_ind)
    
        if not found:
            return matrix[min_ind],min_ind
        else:
            print memory
            plt.scatter(x[min_ind[1]],y[min_ind[0]],color = "black")
            return None,(None,None)
    
    #mid_row = int((rows[0] + rows[1])/2)
    #mid_col = int((cols[0] + cols[1])/2)
    
    
    frame_rows = (rows[0],mid_row,rows[1])
    frame_cols = (cols[0],mid_col,cols[1])
        
    frame_min = global_min(matrix,frame_rows,frame_cols,include_margins)
    #print frame_min_i,frame_min_j
    
    #plt.scatter(x[frame_min_j],y[frame_min_i],color = "black")
    
    s_neighbour = check_smaller_neighbours(matrix,rows,cols,frame_min)
    
    if not s_neighbour:
        
        return matrix[frame_min],frame_min
    
    else:
        if s_neighbour[0] < mid_row:
            if s_neighbour[1] < mid_col:
                return local_min_rec(matrix,(rows[0],mid_row),(cols[0],mid_col))
            elif s_neighbour[1] > mid_col:
                return local_min_rec(matrix,(rows[0],mid_row),(mid_col,cols[-1]))
            else:
                print "Surprise"
                return None,(None,None)
        elif s_neighbour[0] > mid_row:      
            if s_neighbour[1] < mid_col:
                return local_min_rec(matrix,(mid_row,rows[-1]),(cols[0],mid_col))
            elif s_neighbour[1] > mid_col:
                return local_min_rec(matrix,(mid_row,rows[-1]),(mid_col,cols[-1]))
            else:
                print "Surprise"
                return None,(None,None)
        else:
            print "Surprise"
            return None,(None,None)