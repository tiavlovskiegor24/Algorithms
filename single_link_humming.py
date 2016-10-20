from quick_sort_class import *
from collections import deque
from time import time

def Humm_dist(string_1,string_2,min_spacing):
    dist = 0
    for i in range(len(string_1)):
        if string_1[i] != string_2[i]:
            dist += 1
            if dist >= min_spacing:
                return False
    return True


class Union_find(object):
    
    def __init__(self,elements):
        self.n_sets = len(elements)
        self.parent = {}
        #self.sets = {}
        #self.set_range = {}
        self.set_size = {}
        self.max_set_size = 1
        for element in elements:
            #e_sum = element[1]
            #self.sets[element] = {e_sum:[element]}
            self.set_size[element] = 1
            #self.set_range[element] = [e_sum,e_sum]
            self.parent[element] = element
    
    def insert(self,elements):
        for element in elements:
            #e_sum = element[1]
            #self.sets[element] = {e_sum:[element]}
            self.set_size[element] = 1
            #self.set_range[element] = [e_sum,e_sum]
            self.parent[element] = element
            self.n_sets += 1

    def find(self,x):
        while x != self.parent[x]:
            x = self.parent[x] 
        return x
    
    def union(self,element_1,element_2):
        set1 = self.find(element_1)
        set2 = self.find(element_2)
        
        if self.set_size[set1] > self.set_size[set2]:
            leader = set1
            #self.change_leader(set2,leader)
            self.parent[set2] = leader
            self.set_size[leader] += self.set_size[set2]
            
            #del self.sets[set2]
            del self.set_size[set2]
            #del self.set_range[set2]
        else:
            leader = set2
            #self.change_leader(set1,leader)
            self.parent[set1] = leader
            self.set_size[leader] += self.set_size[set1]
            
            #del self.sets[set1]
            del self.set_size[set1]
            #del self.set_range[set1]
        
        if self.set_size[leader] > self.max_set_size:
            self.max_set_size = self.set_size[leader]
        
        self.n_sets -= 1   
        
        return leader
    
    def change_leader(self,merged_set,new_leader):
        
        for e_sum in self.sets[merged_set]:
            
            if e_sum not in self.sets[new_leader]:
                self.sets[new_leader][e_sum] = self.sets[merged_set][e_sum]
            else:
                self.sets[new_leader][e_sum] += self.sets[merged_set][e_sum]
            
            for node in self.sets[merged_set][e_sum]:
                self.leaders[node] = new_leader

def cum_digit_sum(string):
    sum = 0
    for digit in string:
        sum += int(digit)
    return sum
    
def group_by_cum_digit_sum(string,group_list):
    l = len(string)
    cum_sum = cum_digit_sum(string)
    group_list.append(cum_sum)
    if l <= 6:
        return
    group_by_cum_digit_sum(string[:l/2],group_list) 
            
    

def single_link_humming(filename):
    min_spacing = 3
    max_dist_count = 0
    max_link_count = 0
    max_link_rate = 0
    total_dist_count = 0
    with open(filename,"r") as f:
        
        vertices = {}
        for i1 in range(25):
            for i2
        count = 0
        for line in f:
            
            if count < 1:
                count += 1
                continue
            
            vertex = "".join(line.split())
            m_sum = 0
            v_sum = 0
            
            
            for digit in vertex:
                v_sum += int(digit)
            for digit in vertex[:12]:
                m_sum += int(digit)
                
            #group_list = []
            #group_by_cum_digit_sum(vertex,group_list)
            
            new_node = (vertex,v_sum)
            
            if count < 2:
                uf = Union_find([new_node])
                vertices[v_sum] = {m_sum:[new_node]}
                #vertices[v_sum] = [new_node]
                count += 1
                continue
            
            uf.insert([new_node])
            
            if v_sum not in vertices:
                vertices[v_sum] = {m_sum:[new_node]}
            else:
                if m_sum not in vertices[v_sum]:
                    vertices[v_sum][m_sum] = [new_node]
                else:
                    vertices[v_sum][m_sum].append(new_node)
                    
            #if v_sum not in vertices:
             #   vertices[v_sum] = [new_node]
            #else:
             #   vertices[v_sum].append(new_node)
            
            candidates = [node for i in range(v_sum-min_spacing+1,v_sum+min_spacing) if i in vertices for j in range(m_sum-min_spacing+1,m_sum+min_spacing) if j in vertices[i] for node in vertices[i][j]]
            #candidates = [node for i in range(v_sum-min_spacing+1,v_sum+min_spacing) if i in vertices for node in vertices[i]]
            
            #merged_set_range = uf.set_range[new_node]            
            #print "\nNew node is",new_node
            #print "candidates are",candidates
            #dist_count = 0
            link_count = 0
            max_link_count = 0
            dist_count = 0
            leader = new_node
            for candidate_node in candidates:
                #print "\nCandidate node",candidate_node
                candidate_set = uf.find(candidate_node)
                #new_node_set = uf.find(new_node)
                new_node_set = leader
                #print "Candidate set ",candidate_set
                #print "New node set ",new_node_set
                if candidate_set == new_node_set:
                    continue
                
                #if candidate_set in sets_to_merge:
                 #   continue
                dist_count += 1
                if Humm_dist(new_node[0],candidate_node[0],min_spacing):
                    link_count += 1
                    #print "Merged"
                    #sets_to_merge.append(candidate_set)
                    leader = uf.union(new_node_set,candidate_set)
                    
                    #if uf.set_range[leader][0] < merged_set_range[0]:
                     #   merged_set_range[0] = uf.set_range[leader][0]
                    
                    #if uf.set_range[leader][1] > merged_set_range[1]:
                     #   merged_set_range[1] = uf.set_range[leader][1]
                    
                    #uf.set_range[leader] = merged_set_range
               
            #if len(sets_to_merge) < 2:
                #count += 1
                #if count % 1000. == 0:
                    #print "Count is ",count
                    #print "n_sets is ",uf.n_sets
                    #print "max_set_size ",uf.max_set_size
                    #print "dist_count ",dist_count,"\n"
                #if count > 5000:
                    #break
                #continue
            
            #print "Sets to merge",sets_to_merge,"\n"     
            #leader = sets_to_merge.pop()
            #while sets_to_merge:
                    #set_2 = sets_to_merge.pop()
                
                    #leader = uf.union(leader,set_2)
            
            #uf.set_range[leader] = merged_set_range
            
            #print "Sets",uf.sets
            
            if dist_count != 0:
                link_rate = 1.0*link_count/dist_count
            else:
                link_rate = 0
                
            if dist_count > max_dist_count:
                max_dist_count = dist_count
                max_link_count = link_count  
            if link_rate > max_link_rate:
                max_link_rate = link_rate   
            
            total_dist_count += dist_count
            count += 1
            if count % 1000. == 0:
                print "Count is ",count
                print "n_sets is ",uf.n_sets
                print "max_set_size ",uf.max_set_size
                print "max_dist_count ",max_dist_count
                print "link_count for max_dist_count ",max_link_count
                print "Total dist count ",total_dist_count
                print "max_link_rate ",max_link_rate,"\n"
                
                max_dist_count = 0
            #if count > 5000:
                #break
    
    return {node:parent for node in uf.parent for parent in [uf.find(node)]},uf.n_sets 
    

sets,n = single_link_humming("assignment_2_2_2.txt")
#sets,n = single_link_humming("assignment_2_2_2_test.txt")

print n,"\n"
for set in sets:
    print set
    print sets[set],"\n"

#sets = single_link_humming("assignment_2_2_2_test.txt")
#print "Min k is",k

