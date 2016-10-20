from Hash_class import *
from union_find_class import *
from quick_sort_class import *
from collections import deque
from time import time
    
 
def read_file(filename,hash_table,uf):
    with open(filename,"r") as f:
        
        nodes = []
        count = 0
        for line in f:
            
            if count < 1:
                count += 1
                continue
            
            node = "".join(line.split())
            node_dec = str(int(node,2))
            
            if hash_table.look_up(node_dec):
                continue
            
            hash_table.insert(node_dec)
            uf.insert([node_dec])
            
            nodes.append(node)
            
            count += 1
    return nodes
                
    
def mutate(node,n_m):
    n = len(node)
    mutants = []
    if n_m == 1:
        for i in range(n):
            digit = node[i]
            mutation = [d for d in "01" if d != digit][0]
            mutant = node[:i]+mutation+node[i+1:]
            mutants.append(mutant) 
    
    if n_m == 2:
        locs = [(i,j) for i in range(n) for j in range(i+1,n)]
        for loc in locs:
            mutant = node
            for i in loc:
                digit = node[i]
                mutation = [d for d in "01" if d != digit][0]
                mutant = mutant[:i]+mutation+mutant[i+1:]
            mutants.append(mutant) 
            
    return mutants   
    
def index_gen(n_mutations,start,finish):
    
    for i in range(start,finish):
        if n_mutations > 1:
            for j in index_gen(n_mutations-1,i+1,finish):
                yield i
                yield j
        else:
            yield i

def mutate_gen(node,n_mutations,start = 0):
        n = len(node)
        
        locs = index_gen(n_mutations,start,n)  
        while True:
            mutant = node
            for i in range(n_mutations):
                digit = node[locs.next()]
                mutation = [d for d in "01" if d != digit][0]
                mutant = node[:i]+mutation+node[i+1:]
            yield mutant


def mutate_rec(node,n_mutations,start = 0,mutants = []):
    n = len(node)
    if n_mutations == 1:
        for i in range(start,n-n_mutations+1):
            digit = node[i]
            mutation = [d for d in "01" if d != digit][0]
            mutant = node[:i]+mutation+node[i+1:]
            mutants.append(mutant) 
        return mutants
    
    for i in range(start,n-n_mutations+1):
        digit = node[i]
        mutation = [d for d in "01" if d != digit][0]
        mutant = node[:i]+mutation+node[i+1:]
        mutate_rec(mutant,n_mutations-1,i+1,mutants)
        
    return mutants 

def single_link_humming(nodes,uf):
    count = 0
    while nodes:
        node = nodes.pop()
        node_dec = str(int(node,2))
        
        mutants = mutate_rec(node,1,0,[]) + mutate_rec(node,2,0,[])
        
        leader = node_dec
        for mutant in mutants:
            mutant_dec = str(int(mutant,2))
            if ht.look_up(mutant_dec):
                if uf.find(leader) != uf.find(mutant_dec):
                    leader = uf.union(leader,mutant_dec)
        count += 1
        if count % 1000 == 0:
            print "\nCount is ",count
            print "n_sets is ",uf.n_sets

        
def single_link_humming_gen(filename,uf):
    
    with open(filename,"r") as f:
        
        nodes = {}
        count = 0
        
        for line in f:
            
            if count < 1:
                count += 1
                continue
            
            node = "".join(line.split())
            node_dec = str(int(node,2))
            
            if node_dec not in nodes:
                nodes[node_dec] = node
                uf.insert([node_dec])
            
            count += 1
    
    print uf.n_sets
    count = 0
    
    for node_dec in nodes:
        node = nodes[node_dec]
        
        leader = node_dec
        
        mutants = mutate_gen(node,1)
    
        for mutant in mutants:
            mutant_dec = str(int(mutant,2))
            if ht.look_up(mutant_dec):
                if uf.find(leader) != uf.find(mutant_dec):
                    leader = uf.union(leader,mutant_dec)
                    
        mutants = mutate_gen(node,2)
        for mutant in mutants:
            mutant_dec = str(int(mutant,2))
            if ht.look_up(mutant_dec):
                if uf.find(leader) != uf.find(mutant_dec):
                    leader = uf.union(leader,mutant_dec)
        
        count += 1
        if count % 1000 == 0:
            print "\nCount is ",count
            print "n_sets is ",uf.n_sets  
        

def single_link_humming_1(filename,uf):
    
    with open(filename,"r") as f:
        
        nodes = {}
        count = 0
        
        for line in f:
            
            if count < 1:
                count += 1
                continue
            
            node = "".join(line.split())
            node_dec = str(int(node,2))
            
            if node_dec not in nodes:
                nodes[node_dec] = node
                uf.insert([node_dec])
            
            count += 1
    
    print uf.n_sets
    count = 0
    
    for node_dec in nodes:
        node = nodes[node_dec]
        
        mutants = mutate_rec(node,1,0,[]) + mutate_rec(node,2,0,[])
        
        leader = node_dec
        for mutant in mutants:
            mutant_dec = str(int(mutant,2))
            if mutant_dec in nodes:
                if uf.find(leader) != uf.find(mutant_dec):
                    leader = uf.union(leader,mutant_dec)
        count += 1
        if count % 1000 == 0:
            print "\nCount is ",count
            print "n_sets is ",uf.n_sets                
    
    

ht = Hash_table(200001)
uf = Union_find()

#nodes = read_file("assignment_2_2_2.txt",ht,uf)
#nodes = read_file("assignment_2_2_2_test.txt",ht)


#single_link_humming(nodes,ht,uf)
single_link_humming_gen("assignment_2_2_2.txt",uf)

#print uf.parent
print "Number of clusters is",uf.n_sets

