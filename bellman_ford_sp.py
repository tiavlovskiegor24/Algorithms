from collections import deque
from bitarray import bitarray

def bellman_ford_push(graph,source):
    #print "\nRunning bellman_ford...\n"
    
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    A = [[],[]]
    B = []
    
    for _ in xrange(n):
        A[0].append(float("inf"))
        A[1].append(float("inf"))
        B.append(None)
    
    #print "A has length",len(A)
    
    A[0][source-1] = 0.
    A[1][source-1] = 0.
    #print "Source is :",source-1
    
    #A_i = A[:]
    for i in xrange(0,n-1):
        ind = i % 2
        #print "\ni is ",i,"\n"
        changed = False
        for v in graph["vertices"]:
            if A[ind][v-1] < A[ind-1][v-1]:
                changed = True
                A[ind-1][v-1] = A[ind][v-1]
            #print "v is:",v-1
            for edge in graph["vertices"][v]["edges"]:
                w = graph["edges"][edge]["vertices"][1]
                #print "w is:",w-1
                length = graph["edges"][edge]["length"]
                if A[ind][v-1] + length < A[ind][w-1]:
                    if A[ind][v-1] + length < A[ind-1][w-1]:
                        changed = True
                        A[ind-1][w-1] = A[ind][v-1] + length
                        B[w-1] = v
                        #print ind-1,A[ind-1]
                    else:
                        continue
        if not changed:
            print "Preliminary halt"
            print i,"\n"
            break
        #A = A_i[:]
    
    # checking for negative cost cycles
    for v in graph["vertices"]:
        if A[ind-1][v-1] < A[ind][v-1]:
            print "Negative cycle detected."
            return None,None
        for edge in graph["vertices"][v]["edges"]:
            w = graph["edges"][edge]["vertices"][1]
            length = graph["edges"][edge]["length"]
            if A[ind][v-1] + length < A[ind][w-1]:
                print "Negative cycle detected."
                return None,None
            #A[v-1] = min_path 
            
    return A[ind-1],B
    
    
def bellman_ford_push_Q(graph,source):
    #print "\nRunning bellman_ford...\n"
    
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    A = [] # shortest distance values
    B = [] # penultimate vertex on shortest path
    C = [] # number of edges in shortest path
    
    update_Q = deque([(source,0)])
    in_Q = bitarray(n)
    
    for _ in xrange(n):
        A.append(float("inf"))
        B.append(None)
        C.append(None)
        #in_Q.append(False)
    
    #print "A has length",len(A)
    
    A[source-1] = 0.
    B[source-1] = source-1
    C[source-1] = 0
    in_Q[source-1] = True
    
    #print "Source is :",source-1
    
    count = 0
    max_Q_len = 0
    while update_Q:
        count += 1
        
        v,l = update_Q.popleft()
        
        in_Q[v-1] = False
        
        level = C[v-1]
        
        for edge in graph["vertices"][v]["edges"]:
            w = graph["edges"][edge]["vertices"][1]
            #print "w is:",w-1
            length = graph["edges"][edge]["length"]
            
            if A[v-1] + length < A[w-1]:
                A[w-1] = A[v-1] + length
                B[w-1] = v
                
                '''if C[v-1] + 1 > C[w-1]:
                    C[w-1] = C[v-1] + 1
                    #if not in_Q[w-1]:
                    update_Q.append((w,C[w-1]))
                        #in_Q[w-1] = True'''
                
                C[w-1] = C[v-1] + 1
                if C[w-1] > n-1:
                    print "Negative cycle detected."
                    print level
                    print max_Q_len
                    print count
                    return None,None,None
                
                if not in_Q[w-1]:
                    update_Q.append((w,C[w-1]))
                    in_Q[w-1] = True
        
        if len(update_Q) > max_Q_len:
            max_Q_len = len(update_Q)
    
    print level
    print max_Q_len
    print count
    return A,B,C


def bellman_ford_pull(graph,source):
    #print "\nRunning bellman_ford...\n"
    
    n = len(graph["vertices"])
    m = len(graph["edges"])
    
    A = [[],[]]
    B = []
    
    for _ in xrange(n):
        A[0].append(float("inf"))
        A[1].append(float("inf"))
        B.append(None)
    
    #print "A has length",len(A)
    
    A[0][source-1] = 0.
    
    #A_i = A[:]
    for i in xrange(1,n):
        ind = i % 2
        print i
        changed = False
        for v in graph["vertices"]:
            min_path = A[ind-1][v-1]
            for edge in graph["vertices"][v]["in_edges"]:
                w = graph["edges"][edge]["vertices"][0]
                length = graph["edges"][edge]["length"]
                #print w - 1
                if A[ind-1][w-1] + length < min_path:
                    changed = True
                    min_path = A[ind-1][w-1] + length
                    B[v-1] = w
                A[ind][v-1] = min_path
        if not changed:
            break
        #A = A_i[:]
    
    # checking for negative cost cycles
    for v in graph["vertices"]:
        min_path = A[ind][v-1]
        for edge in graph["vertices"][v]["in_edges"]:
            w = graph["edges"][edge]["vertices"][0]
            length = graph["edges"][edge]["length"]
            if A[ind][w-1] + length < min_path:
                print "Negative cycle detected."
                return None,None
            #A[v-1] = min_path 
    
    return A[ind],B





