# huffman codes class
from quick_sort_class import *
import numpy as np
from operator import itemgetter

class binary_node(object):
    def __init__(self,id,(key,value) = None,left=None,right=None):
        self.leaves = [left,right]
        self.id = id
        self.key = key
        self.value = value
        self.code = None

    def __getitem__(self,item):
        return self.leaves[item]

    def __repr__(self):
        return self.code

    
class huffman_codes(object):
    def __init__(self,symbols,freqs):
        freqs = [-freq for freq in freqs]
        pairs = zip(freqs,symbols)
        Quick_Sort(pairs)
        #pairs.sort(key=itemgetter(0))
        # create a stack of symbols in descending order of frequencies
        nodes = [binary_node(str(id),pair) for id,pair in enumerate(pairs)]

        #look up table for parent nodes
        self.parents = {}
        for node in nodes:
            self.parents[node.value] = node
        
        for i in range(len(nodes)-1):
            s1 = nodes.pop()
            s2 = nodes[-1]

            s12_key = s1.key + s2.key
            s12_id = s1.id +"_"+ s2.id

            s1.code = "0"
            s2.code = "1"

            s12 = binary_node(s12_id,(s12_key,None),s1,s2)

            self.parents[s1] = s12
            self.parents[s2] = s12

            nodes[-1] = s12
            
            for idx in range(1,len(nodes)):
            
                if nodes[-idx].key < nodes[-idx-1].key:
                    s = nodes[-idx]
                    nodes[-idx] = nodes[-idx-1]
                    nodes[-idx-1] = s
                    idx -= 1
                else:
                    break
                
        self.decoder = nodes.pop()
        self.parents[self.decoder] = self.decoder

    def decode(self,code):
        out = ""
        symbol = self.decoder
        for d in code:
            symbol = symbol[int(d)]
            if symbol[0] is None:
                #print code,":",symbol.value
                out += symbol.value
                symbol = self.decoder
        if symbol is not self.decoder:
            print "Incomplete code"
        return out

    def encode(self,message):
        out = "" # change to bits later
        for c in message:
            if c not in self.parents:
                print "Character not in the code list"
                return 
            code = ""
            while True:
                c = self.parents[c]
                if c is not self.decoder:
                    code =  c.code + code
                else:
                    break
            out += code
        print "Message length is:%d characters"%len(message)
        print "Code length is: %d bits"%len(out)
        return out
            

freqs = np.array([17,2,11,15,3])
alph = ["x","a","b","c","d"]
hf = huffman_codes(alph,freqs)
H = np.dot((freqs*1./freqs.max()),np.log2((freqs*1./freqs.max())**-1))
H0 = np.log2(len(alph))
'''
hf.decode("00") 
hf.decode("01")
hf.decode("1")
hf.decode("000")
hf.decode("0011")
'''
m = "adcxxxxxxxxabxxxxxxxxxxxxxxxdaxxxxxbxxxxxxxxxxxxdaxxxdxxabxx"
print m
print H,H0*len(m),H*len(m)
print hf.encode(m)
print hf.decode(hf.encode(m))
#print hf.decode("000101101000111000100110001110010001011101001011001111000101011110000")
#print hf.decode("00110")
print hf.encode("x")        
