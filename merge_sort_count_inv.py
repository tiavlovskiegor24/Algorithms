def merge_sort_count_inv(array):
    n = len(array)
    
    if n == 1 or n == 0:
        return array,0
        
    
    B,left_inv = merge_sort_count_inv(array[0:n-n/2])
    C,right_inv = merge_sort_count_inv(array[n-n/2:n])
    
    i = 0
    j = 0
    split_inv = 0
    
    for k in range(0,n):
        if i < len(B) and j < len(C):
            if B[i]<=C[j]:
                array[k] = B[i]
                i += 1
            else:
                array[k] = C[j]
                split_inv += len(B)-i
                j += 1
        elif j < len(C):
            array[k] = C[j]
            j += 1
        elif i < len(B):
            array[k] = B[i]
            i += 1
            
    return array,(split_inv + left_inv + right_inv)
