from time import time

def mutate(node,n_m):
    n = len(node)
    mutants = []
    if n_m == 1:
        for i in range(n):
            digit = node[i]
            mutation = [d for d in "01" if d != digit][0]
            mutant = node[:i]+mutation+node[i+1:]
            mutants.append(mutant) 
            print i,mutant
    
    if n_m == 2:
        locs = [(i,j) for i in range(n) for j in range(i+1,n)]
        for loc in locs:
            mutant = node
            for i in loc:
                digit = node[i]
                mutation = [d for d in "01" if d != digit][0]
                mutant = mutant[:i]+mutation+mutant[i+1:]
            print loc,mutant
            mutants.append(mutant) 
            
    return mutants 
    
def mutate_rec(node,n_mutations,start = 0,mutants = []):
    n = len(node)
    if n_mutations == 1:
        for i in range(start,n-n_mutations+1):
            digit = node[i]
            mutation = [d for d in "01" if d != digit][0]
            mutant = node[:i]+mutation+node[i+1:]
            mutants.append(mutant) 
            #print i,mutant,len(mutants)
        return mutants
    
    for i in range(start,n-n_mutations+1):
        digit = node[i]
        mutation = [d for d in "01" if d != digit][0]
        mutant = node[:i]+mutation+node[i+1:]
        mutate_rec(mutant,n_mutations-1,i+1,mutants)
        
    return mutants
    
def index_gen(n_mutations,start,finish):
    
    if n_mutations == 0:
        yield "Total_End"
        return
    
    elif n_mutations > 1:
        i = start
        while i < finish-n_mutations+1:
        #for i in range(start,finish-n_mutations+1):
            yield i
            
            for j in index_gen(n_mutations-1,i+1,finish):
                
                if j == "Total_End":
                    
                    if i == finish-n_mutations:
                        yield "Total_End"
                        return
                    
                    yield "End"
                    break
                
                elif j == "End":
                    yield "End"
                    yield i
                    continue
                
                else:
                    yield j
            i += 1
            
    else:
        i = start
        while i < finish:
        #for i in range(start,finish):
            yield i
            
            if i == finish - 1:
                yield "Total_End"
                return
            
            yield "End"
            i += 1

def mutate_gen(node,n_mutations,start = 0):
        n = len(node)
        locs = index_gen(n_mutations,start,n)  
        while True:
            mutant = node
            for j in locs:
                if j == "Total_End":
                    yield mutant
                    return
                if j == "End":
                    break
                #print j
                digit = mutant[j]
                mutation = [d for d in "01" if d != digit][0]
                mutant = mutant[:j] + mutation + mutant[j+1:]
            yield mutant

n_mutations = 1    
t1 = time()    
mutants = mutate_gen("0101001110100",n_mutations)
#t2 = time()
mutants2 = mutate_rec("0101001110100",n_mutations,0,[])
#print "List ",time()-t2

#ind = index_gen(2,0,5)
i = 0

t1 = time()  
for mutant in mutants:
    #print mutant,mutants2[i]
    
    if mutant not in mutants2:
       print i,mutant,"\n"
    i += 1    
print "Generator ",time()-t1
print i

t2 = time()
for mutant in mutants2:
    pass
    #print mutant,"\n"
print "List ",time()-t2

print len(mutants2)

