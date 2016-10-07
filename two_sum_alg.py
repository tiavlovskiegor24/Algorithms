def two_sum_alg(targets,h_table):
    total_count = 0
    target_values = []
    
    for i in range(-10000,10001):
        target_values.append(False)
    
    print "\nRunning two_sum_algorithm\n"
    for t in targets:       
        
        elements = h_table.output_elements()
        
        while elements:
            
            x = elements.pop()
            y = h_table.look_up(str(t-int(x)))
            if y:
                index = t+10000
                try:
                    target_values[index] = True
                except:
                    print index
                total_count += 1
                break
                
        
        print "Sum %s is %s \n" %(t,target_values[index])
    
    print "Total count is ",total_count,"\n"
    
    return target_values,total_count
    
def two_sum_alg2(targets,elements):
    total_count = 0
    target_values = []
    
    for i in targets:
        target_values.append(False)
    
    lower_pointer = 0
    upper_pointer = len(elements)-1
    
    print "\nRunning two_sum_algorithm\n"
    
    while lower_pointer != upper_pointer:
        sum = int(elements[lower_pointer]) + int(elements[upper_pointer])
        if sum < targets[0]:
            lower_pointer += 1
        elif sum > targets[-1]:
            upper_pointer -= 1
        else:
            index = sum+10000
            if not target_values[index]:
                target_values[index] = True
                total_count += 1
                print "Sum %s is %s \n" %(sum,target_values[index])
            lower_pointer += 1
                
    
    print "Total count is ",total_count,"\n"
    
    return target_values,total_count
    
