class Union_find(object):
    
    def __init__(self,elements = []):
        self.n_sets = len(elements)
        self.parent = {}
        self.set_size = {}
        self.rank = {}
        self.max_set_size = 0
        for element in elements:
            self.parent[element] = element
            self.set_size[self.find(element)] = 1
            self.rank[self.find(element)] = 0
            self.max_set_size = 1
    
    def insert(self,elements):
        for element in elements:
            self.parent[element] = element
            self.set_size[self.find(element)] = 1
            self.rank[self.find(element)] = 0
            self.n_sets += 1

    def find_old(self,x):
        # find without pass compression
        while x != self.parent[x]:
            x = self.parent[x] 
        return x
    
    def find(self,x):
        # find with path compression
        parent = self.parent[x]
        
        if parent == x:
            return parent
        
        root = self.find(parent)
        self.parent[x] = root
        
        return root
    
    def union(self,element_1,element_2):
        
        set1 = self.find(element_1)
        set2 = self.find(element_2)
        
        if self.rank[set1] > self.rank[set2]:
            leader = set1
            self.parent[set2] = leader
            
        elif self.rank[set1] < self.rank[set2]:
            leader = set2
            self.parent[set1] = leader
        
        elif self.rank[set1] == self.rank[set2]:
            leader = set2
            self.parent[set1] = leader
            self.rank[leader] += 1
            
        '''
        if self.set_size[self.find(leader)] > self.max_set_size:
            self.max_set_size = self.set_size[self.find(leader)]
        
        self.n_sets -= 1
        
        
        if self.set_size[set1] > self.set_size[set2]:
            leader = set1
            self.parent[set2] = leader
            self.set_size[self.find(leader)] += self.set_size[set2]
            
            del self.set_size[set2]
            
        else:
            leader = set2
            self.parent[set1] = leader
            self.set_size[self.find(leader)] += self.set_size[set1]
            
            del self.set_size[set1]
        
        if self.set_size[self.find(leader)] > self.max_set_size:
            self.max_set_size = self.set_size[self.find(leader)]
        '''
            
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