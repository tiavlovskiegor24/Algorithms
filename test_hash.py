def hash_func(key):
    n = 1000003
    window = len(key)/5 + 1
    params = (474145, 862538, 737395, 962738, 901392)
    
    index = 0
    for i in range(len(params)): 

        if len(key[:len(key)-window*i]) > window:
            x = int(key[:len(key)-window*i][-window:])  
            index += params[i]*x
            
            if key[:len(key)-window*i][-(window+1)] in ["-",""]:
                break
        
        else:
            x = abs(int(key[:len(key)-window*i]))
            index += params[i]*x
            break     
        
    index = index % n
    
    return index

keys = ['-73638699937', '90208942159', '83041044316', '-45502221839', '-22971339954', '2076429641', '59029929041', '-66221779290', '9493301673', '-45502221839']   
            
for key in keys:
    print (key,hash_func(key))
    