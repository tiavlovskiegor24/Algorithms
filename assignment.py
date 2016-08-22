with open("assignment.txt","r") as f:
    array = []
    for line in f:
        array.append(int(line))
    f.closed
    
from merge_sort_count_inv import merge_sort_count_inv

quick_sort(array)

print inv


