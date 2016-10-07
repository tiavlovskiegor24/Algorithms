from random import randint

def swap(array,i1,i2):
    swap = array[i1]
    array[i1] = array[i2]
    array[i2] = swap
    
def partition(array,l,r):
    q = l+1 # in case p == l, i.e. the pivot in the first element of array
    for j in range(l+1,r):
        
        if array[j]["score"] < array[l]["score"]:
            swap(array,q,j)
            q += 1
        elif array[j]["score"] == array[l]["score"]:
            if array[j]["weight"] < array[l]["weight"]:
                swap(array,q,j)
                q += 1
                
    swap(array,l,q-1)
    return q


def quick_sort(array,l = 0,r = None):
    
    if r == None:
        r = len(array) 
    
    if r-l <= 1:
        return 
    
    p = randint(l,r-1) # select the pivot index
    
    # partition the array and return the index of pivot element 
    swap(array,p,l)
    q = partition(array,l,r) 
    
    quick_sort(array,l,q-1)
    quick_sort(array,q,r) 

def read_jobs(filename):
    job_list = []
    with open(filename,"r") as f:
        i = 0
        for line in f:
            if i < 1:
                i += 1
                continue
            line  = line.split()
            job_list.append({"id":"j_"+str(i),"weight":float(line[0]),"length":float(line[1]),"score":None,"comletion_time":None})
            i += 1
                    
    return job_list

def schedule(job_list):
    
    for job in job_list:
        job["score"] = job["weight"]/job["length"]
        
    quick_sort(job_list)
    
    return job_list[::-1]
    
#job_list = read_jobs("assignment_2_1_1.txt")
job_list = read_jobs("assignment_2_1_1_test.txt")

job_list = schedule(job_list)

completion_time = 0
weighted_completion_sum = 0
for job in job_list:
    
    completion_time += job["length"]
    weighted_completion_sum += completion_time*job["weight"]
    
    job["comletion_time"] = completion_time

print weighted_completion_sum
  
#assert weighted_completion_sum == 69119377652.0, "Does not match with w-l score"
#assert weighted_completion_sum == 67311454237.0, "Does not match with w/l score"
    



    

    