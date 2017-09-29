from message_passing import *
from collections import namedtuple,OrderedDict
from factor_graph import *
from operator import itemgetter


def binary_sym_channel(flip_prob,valid_variable_tuples = None):
    '''factory creates likelihood function for received and transmitted bits'''
    
    valid_variables_set = set([tuple(sorted(var_tuple)) for var_tuple in valid_variable_tuples])
    
    def likelihood_func(variables_dict):
        assert tuple(sorted(variables_dict.keys())) in valid_variables_set
        #assert reduce(lambda cum,x: )
        received_bits = variables_dict["r"]
        #state = bin(variables_dict["s"]).split("b")[-1]
        transmitted_bits = variables_dict["t"] 
        assert len(received_bits) == len(transmitted_bits)
        cum_prob = 1
        for r,t in zip(received_bits,transmitted_bits):
            
            cum_prob *= (1-flip_prob if int(r) == int(t) else flip_prob)

        return cum_prob
    
    return likelihood_func

def binary_dot_prod(x1,x2):
    
    i = 0
    while (x1 >> i+1) > 0 or (x2 >> i+1) > 0:
        i += 1

    r1 = x1
    r2 = x2
    cum = []
    for j in reversed(range(i+1)):
        b = (r1 >> j)*(r2 >> j)
        cum.append(b)
        r1 = r1 - ((r1 >> j) << j)
        r2 = r2 - ((r2 >> j) << j)

    return sum(cum) % 2

def likelihood_func(vars_dict):
    valid_vars = set(["r1,r2","c1","c2"])
    assert all(var in var_dict for var in valid_vars)
    assert all(var in valid_vars for var in vars_dict)

def filter_width(f):
    i = 0
    while f >> i > 0:
        i+=1

    return i
    

class Convolutional_Code(Graph):

    def __init__(self,n_steps,filters,flip_prob,*args,**kwargs):

        super(Convolutional_Code,self).__init__(type_="Convolutional_Code",*args,**kwargs)

        #assert reduce(lambda cum,x:cum and len(bin(x).split("b")[-1] == self.filter_width),filters)
        self.n_steps = n_steps
        
        self.filters = filters
        self.n_filters = len(self.filters)
        self.filter_width = max([filter_width(f) for f in filters])
        
        self.state_range = int("1"*(self.filter_width-1),2)+1

        self.transition_func,self.transitions_dict = self.create_transition_func(self.state_range)
        self.encoding_func = self.create_encoding_func(self.filters)
        
        self.flip_prob = flip_prob

        self.create_graph()


        
    def create_graph(self):

        encoder_state = Recurrent_Variable(name = "e",
                                           n_steps = self.n_steps,
                                           transition_func = self.transition_func,
                                           #binary_equality_constraint([("n","p")]),
                                           domain = range(self.state_range),
                                           connections = ["encoding"],
                                           observed_steps = None,
                                              
        )
        self.add_node(encoder_state,category = "Encoder_state")

        encoding_factor = Factor(name="encoding",
                                 factor_func = self.encoding_func,
                                 connections = ["e","t"])

        self.add_node(encoding_factor,category = "Encoding_factor")

        bits_domain = [tuple(("0"*self.n_filters+bin(i)[2:])[-self.n_filters:])
                       for i in range(2**self.n_filters)]
        
        transmitted_bits = Variable(name = "t",
                                    connections = ["likelihood","encoding"],
                                    domain = bits_domain,
        )
        
        self.add_node(transmitted_bits,category = "Transmitted_bits")


        likelihood_factor = Factor(name = "likelihood",
                                   factor_func = binary_sym_channel(self.flip_prob,[("t","r")]),
                                   connections = ["t","r"],
        )
        self.add_node(likelihood_factor,category = "Likelihood_factor")
        
        received_bits = Observed_Recurrent_Variable(name = "r",
                                                    connections = ["likelihood"],
                                                    domain = bits_domain)

        self.add_node(received_bits,category = "Received_bits")

        
    def encode(self,source_bits):

        state = "0"*(self.filter_width-1)
        for b in source_bits:
            print state,b
            yield tuple(str(binary_dot_prod(f,int(state+str(b),2))) for f in self.filters),int(state,2)
            state = state[1:]+str(b)

    def decode(self,received_bits,**kwargs):

        self.nodes["Received_bits"]["r"].set_as_observed(received_bits)
        self.nodes["Encoder_state"]["e"].set_as_observed([0]+[None]*(self.n_steps-1))

        self.run(init_node_type = "Received_bits",**kwargs)
        node = self.nodes["Encoder_state"]["e"]
        for i in range(node.n_steps):
            node.go_to_step(i)
            #print "\n\nStep {}".format(i)
            #print max([(s,node.compute(s)) for s in range(self.state_range)],key=itemgetter(1))
            #
            #print node.received
            #node.unpack_messages()
            #print [(s,node.compute(s)) for s in range(self.state_range)]
            yield max([(s,node.compute(s)) for s in range(self.state_range)],key=itemgetter(1))[0]
            
            #print i,(1,node.compute(1)),(0,node.compute(0)),node.compute(1)/node.compute(0)
    
    @staticmethod
    def create_encoding_func(filters):
        '''function creates an encoding function using the list of convolution filters'''
        def encoding_func(vars_dict):
            assert set(vars_dict.keys()) == set(["e","t"]),vars_dict
            s = vars_dict["e"]
            s1 = (s << 1)
            s2 = s1 + 1
            t = vars_dict["t"]
            assert len(t) == len(filters)
            for t,f in zip(t,filters):
                if int(t) not in [binary_dot_prod(f,s1),binary_dot_prod(f,s2)]:
                    return 0.
            return 1.

        return encoding_func
        
    @staticmethod
    def create_transition_func(state_range):
        '''function create a state transition function'''
        transitions = {}
        i = 0
        while (state_range >> i+1)> 0:
            i+=1
            
        for s in range(state_range):
            #print
            #print bin(s)
            #i = 0
            #while s >> i+1 > 0:
             #   i += 1

            #print bin((s >> i) << i)
            r = s << 1
            r = r-((r >> i) << i)
            #r =  (s - ((s>>i) << i)) << 1
            #r = 
            #print bin(r)
            assert r+1 < state_range,r
            transitions[(s,r)] = 0
            transitions[(s,r+1)] = 1
            
        def transition_func(var_dict):
            assert set(var_dict.keys()) == set(["p","n"]),var_dict

            source_bit = transitions.get((var_dict["p"],var_dict["n"]))
            if source_bit is None:
                return 0
            else:
                return 1

        return transition_func,transitions



if __name__=="__main__":

    source_bits = [1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,0]
    conv_code = Convolutional_Code(n_steps = len(source_bits),flip_prob = 0.1,filters = [7,6,5])
    coded_bits,state_seq = zip(*list(conv_code.encode(source_bits)))
    print coded_bits

    received_bits = list(coded_bits)#[('1', '0'), ('0', '1'), ('0', '1'), ('1', '1'), ('0', '1')]
    received_bits[2] = ("1","0","1")
    received_bits[-3] = ("1","1","1")
    #received_bits[-12] = ("0","1","1")
    print received_bits

    print
    for i,(t,r) in enumerate(zip(coded_bits,received_bits)):
        if t != r:
            print i,t,r

    decoded_state_seq = list(conv_code.decode(received_bits,message_type = "max_mult",verbose = False))
    print
    for t,p in zip(state_seq,decoded_state_seq):
        print t,p,
        if t!=p:
            print "opps"
        else:
            print

    print
    for i in conv_code.transitions_dict:
        print i

    '''
    #_,transitions_dict = Convolutional_Code.create_transition_func(8)

    t = (0,1)
    print
    print t
    f = Convolutional_Code.create_encoding_func([7,6])
    for s in range(8):
        print
        print binary_dot_prod(7,(s<<1)),binary_dot_prod(7,(s<<1)+1),binary_dot_prod(6,(s<<1)),binary_dot_prod(6,(s<<1)+1)
        print f({"t":t,"s":s})
    
    #for i in range(8):
        #print binary_dot_prod(7,i),binary_dot_prod(3,i)   
        #print
    #for i in range(10):
     #   print i,filter_width(i)   

    #f = binary_sym_channel(0.1,[("t","r")])
    #print f({"t":(0,0),"r":(0,0)})

    #print list(Convolutional_Code.encode([1,0,1,0,1,1],[7,6],3))
    '''
