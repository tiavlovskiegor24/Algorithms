from random import randint
from __future__ import division

%matplotlib inline

import matplotlib.pyplot as plt
import numpy as np


def check_strict_loc_min(matrix,i,j):
    
    for k in range(i-1,i+2):
        for l in range(j-1,j+2):
            if i == k and j == l:
                continue
            if matrix[i,j] >= matrix[k,l]:
                return False
    return True
                   
    if matrix[i,j] < matrix[i+1,j+1] and \
            matrix[i,j] < matrix[i+1,j-1] and \
            matrix[i,j] < matrix[i-1,j-1] and \
            matrix[i,j] < matrix[i-1,j+1] and \
            matrix[i,j] < matrix[i+1,j] and \
            matrix[i,j] < matrix[i-1,j] and \
            matrix[i,j] < matrix[i,j+1] and \
            matrix[i,j] < matrix[i,j-1]:
        return True
    else:
        return False


def loc_min_array(array,start_index):
    
    min_v = float("inf")
    min_ind = 0 
    n = len(array)
    
    start = start_index
    
    if array[start-1] > array[start] and array[start] < array[start+1]:
            return start
    
    for i in range(start+1,n-1):
        if array[i-1] > array[i] and array[i] < array[i+1]:
            return i  
        if array[i] < min_v:
            min_v = array[i]
            min_ind = i
    
    for i in range(start,1):
        if array[i-1] > array[i] and array[i] < array[i+1]:
            return i  
        if array[i] < min_v:
            min_v = array[i]
            min_ind = i
    
    return min_ind

    

def local_min(matrix,start = 0,end = None,start_index = "Random"):
    
    n,m = matrix.shape # n is the number of rows, m is a number of columns
    
    if start_index == "Random":
        start_index = randint(1,n-2)
    
    if end == None:
        end = matrix.shape[1]
    
    n = end - start
    
    random = True # set to true for radnom index in range(start,end) to be selected 
    
    if random:
        if n > 3:
            pivot = randint(start+1,end-2) # radnom index in range(start,end) is selected 
            #pivot = int(n/2) + start # choose this if median is to be always selected
        else:
            index = loc_min_array(matrix[:,start+1],start_index)
            
            if check_strict_loc_min(matrix,index,start+1):
                return matrix[index,start+1],start+1,index
            else: 
                return None,None,None
    
    index = loc_min_array(matrix[:,pivot],start_index)

    if matrix[index,pivot] > matrix[index,pivot-1]:
        return local_min(matrix,start,pivot+1,start_index)

    elif matrix[index,pivot] > matrix[index,pivot+1]:
        return local_min(matrix,pivot,end,start_index)
    
    else:
        if check_strict_loc_min(matrix,index,pivot):
            return matrix[index,pivot],pivot,index
        else: 
            return None,None,None
