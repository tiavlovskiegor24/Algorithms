from message_passing import *
from collections import namedtuple,OrderedDict
from factor_graph import *
from operator import itemgetter

def binary_sym_channel(flip_prob,valid_variable_tuples = None):
    '''factory creates likelihood function for received and transmitted bits'''
    
    valid_variables_set = set([tuple(sorted(var_tuple)) for var_tuple in valid_variable_tuples])
    
    def likelihood_func(variables_dict):
        assert tuple(sorted(variables_dict.keys())) in valid_variables_set
        v1,v2 = variables_dict.values()
        return 1-flip_prob if v1 == v2 else flip_prob

    return likelihood_func


def binary_equality_constraint(valid_variables_tuples = None):
    '''factory creates equality check function for several binary variables'''
    valid_variables_set = set([tuple(sorted(var_tuple)) for var_tuple in valid_variables_tuples])
    
    def check_equality(variables_dict):
        assert tuple(sorted(variables_dict.keys())) in valid_variables_set
        #reduce(lambda cum,x:)
        values = variables_dict.values()
        return int(values[0]*len(values) == sum(values))

    return check_equality


def binary_parity_constraint(valid_variables_tuples = None):
    '''factory creates parity check function for several binary variables'''
    valid_variables_set = set([tuple(sorted(var_tuple)) for var_tuple in valid_variables_tuples])
    
    def check_parity(variables_dict):
        assert tuple(sorted(variables_dict.keys())) in valid_variables_set
        #reduce(lambda cum,x:)
        values = variables_dict.values()
        return 1-reduce(lambda cum,x:(cum+x) % 2,values)

    return check_parity
    


class Repeat_Code(Graph):
    def __init__(self,n_repeats,flip_prob,*args,**kwargs):
        super(Repeat_Code,self).__init__(type_="Repeat_Code",*args,**kwargs)
        self.n_repeats = n_repeats
        self.flip_prob = flip_prob
        self.create_graph()
        
    def create_graph(self):
        likelihood_factors = OrderedDict()
        transmitted_bits = [] 
        received_bits = []
        for i in range(self.n_repeats):
            transmitted_bits.append("t_{}".format(i))
            received_bits.append("r_{}".format(i))
            likelihood_factors["f_{}".format(i)] = (transmitted_bits[-1],received_bits[-1])


        self.likelihood_func = binary_sym_channel(self.flip_prob,likelihood_factors.values())
        likelihood_factors = [Factor.factor_tuple(name = name,
                                                  factor_func = self.likelihood_func,
                                                  connections = variables)
                              for name,variables in likelihood_factors.iteritems()]
        
        constraint_factors = OrderedDict()
        for j in range(1,self.n_repeats):
            constraint_factors["f_{}".format(i+j)] = (transmitted_bits[j-1],transmitted_bits[j])

        self.check_equality = binary_equality_constraint(constraint_factors.values())

        constraint_factors = [Factor.factor_tuple(name = name,
                                                  factor_func = self.check_equality,
                                                  connections = variables)
                              for name,variables in constraint_factors.iteritems()]    

        factors = likelihood_factors+constraint_factors

        v_f = {} # variables-factors dictionary
        for factor in factors:
            for v in factor.connections:
                if v not in v_f:
                    v_f[v] = [factor.name]
                else:
                    v_f[v].append(factor.name)


        received_bits = [Variable.variable_tuple(name = name,
                                                 domain = [0,1],
                                                 connections = v_f[name],
                                                 observed = None)
                         for name in received_bits]
        
        
        
        transmitted_bits = [Variable.variable_tuple(name = name,
                                                    domain = [0,1],
                                                    connections = v_f[name],
                                                    observed = None)
                            for name in transmitted_bits]
    

        # convert node_tuples to graph nodes
        factors = [Factor(**factor._asdict()) for factor in factors]
        received_bits = [Variable(**variable._asdict()) for variable in received_bits]
        transmitted_bits = [Variable(**variable._asdict()) for variable in transmitted_bits]


        for node in received_bits:
            self.add_node(node,category = "Received_bits")

        for node in transmitted_bits:
            self.add_node(node,category = "Transmitted_bits")

        for node in factors:
            self.add_node(node,category = "Factors")


    def encode(self,bit):
        return [bit]*self.n_repeats

    def decode(self,received_bits,**kwargs):
        for i,b in enumerate(received_bits):
            self.nodes["Received_bits"]["r_{}".format(i)].set_as_observed(b)

        self.run(init_node_type = "Variable",**kwargs)

        for node in self.nodes["Transmitted_bits"].values():
            print node.name,(1,node.compute(1)),(0,node.compute(0))
            
        

class Hamming_Code(Graph):

    def __init__(self,flip_prob,*args,**kwargs):
        super(Hamming_Code,self).__init__(type_="Repeat_Code",*args,**kwargs)
        self.flip_prob = flip_prob
        self.create_graph()

    def create_graph(self):
        likelihood_factors = OrderedDict()
        noise_bits = [] 
        syndrome_bits = ["z_0","z_1","z_2",
         #                "z_3",
        ]
        for i in range(7):
            noise_bits.append("n_{}".format(i))
            #syndrome_bits.append("r_{}".format(i))
            likelihood_factors["f_{}".format(i)] = (noise_bits[-1],"0")


        likelihood_func = binary_sym_channel(self.flip_prob,likelihood_factors.values())
        self.likelihood_func = lambda x: likelihood_func(dict(x.items()+[("0",0)]))

        likelihood_factors = [Factor.factor_tuple(name = name,
                                                  factor_func = self.likelihood_func,
                                                  connections = variables[:1])
                              for name,variables in likelihood_factors.iteritems()]
        
        constraint_factors = OrderedDict()
        #for j in range(1,self.n_repeats):
        constraint_factors["f_a"] = ("z_0","n_0","n_1","n_2","n_4")
        constraint_factors["f_b"] = ("z_1","n_1","n_2","n_3","n_5")
        constraint_factors["f_c"] = ("z_2","n_0","n_2","n_3","n_6")
        #constraint_factors["f_d"] = ("z_3","n_0","n_1","n_3","n_7")
        

        self.check_parity = binary_parity_constraint(constraint_factors.values())

        constraint_factors = [Factor.factor_tuple(name = name,
                                                  factor_func = self.check_parity,
                                                  connections = variables)
                              for name,variables in constraint_factors.iteritems()]    

        factors = likelihood_factors+constraint_factors

        v_f = {} # variables-factors dictionary
        for factor in factors:
            for v in factor.connections:
                if v not in v_f:
                    v_f[v] = [factor.name]
                else:
                    v_f[v].append(factor.name)

        syndrome_bits = [Variable.variable_tuple(name = name,
                                                 domain = [0,1],
                                                 connections = v_f[name],
                                                 observed = None)
                         for name in syndrome_bits]
        
        
        
        noise_bits = [Variable.variable_tuple(name = name,
                                                    domain = [0,1],
                                                    connections = v_f[name],
                                                    observed = None)
                            for name in noise_bits]
    

        # convert node_tuples to graph nodes
        factors = [Factor(**factor._asdict()) for factor in factors]
        syndrome_bits = [Variable(**variable._asdict()) for variable in syndrome_bits]
        noise_bits = [Variable(**variable._asdict()) for variable in noise_bits]


        for node in syndrome_bits:
            self.add_node(node,category = "Syndrome_bits")

        for node in noise_bits:
            self.add_node(node,category = "Noise_bits")

        for node in factors:
            self.add_node(node,category = "Factors")


    #def encode(self,bit):
     #   return [bit]*self.n_repeats

    def decode(self,syndrome_bits,**kwargs):
        for i,b in enumerate(syndrome_bits):
            self.nodes["Syndrome_bits"]["z_{}".format(i)].set_as_observed(b)

        self.run(init_node_type="Variable",**kwargs)

        for name,node in self.nodes["Noise_bits"].iteritems():
            max_prob = max([(1,node.compute(1)),(0,node.compute(0))],key=itemgetter(1))
            if max_prob[-1] > 1.9:
                self.nodes["Noise_bits"][name].set_as_observed(max_prob[0])

        self.run(init_node_type="Variable",**kwargs)

        for name,node in self.nodes["Noise_bits"].iteritems():
            max_prob = max([(1,node.compute(1)),(0,node.compute(0))],key=itemgetter(1))
            print name,max_prob
            

if __name__=="__main__":
    
    
    repeat_code = Repeat_Code(n_repeats = 7,flip_prob = 0.1)

    received_bits = [1,1,1,0,0,0,0]
    repeat_code.decode(received_bits,limit = 7,message_type = "max_mult")
    #print reduce(lambda cum,x:cum*(0.9),received_bits,1)

    h_code = Hamming_Code(flip_prob=0.1)
    syndrome_bits = [1,0,0]
    h_code.decode(syndrome_bits,limit = 10,message_type = "max_mult")
