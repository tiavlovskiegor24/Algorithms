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



class Convolutional_Code(Graph):

    def __init__(self,filters,,flip_prob,*args,**kwargs):
        super(Convolutional_Code,self).__init__(type_="Convolutional_Code",*args,**kwargs)
        self.filters = filters
        self.n_filters = len(self.filters)
        self.flip_prob = flip_prob
        self.create_graph()

    def create_graph(self):
        likelihood_factor = Factor(name = "likelihood",
                                   factor_func = binary_sym_channel(self.flip_prob,[("t","r")]),
                                   connections = ["t","r"]
        )
        self.add_node(likelihood_factor,category = "Likelihood_factor")

        transmitted_bits = Recurrent_Variable(name = "t",
                                              n_steps = self.n_repeats,
                                              transition_func = check_equality,
                                              #binary_equality_constraint([("n","p")]),
                                              domain = [0,1],
                                              connections = ["likelihood"],
                                              observed_steps = None,
                                              
        )
        self.add_node(transmitted_bits,category = "Transmitted_bits")

        received_bits = Recurrent_Variable(name = "r",
                                           n_steps = self.n_repeats,
                                           connections = ["likelihood"],
                                           domain = [0,1],
                                           observed_steps = None)

        self.add_node(received_bits,category = "Received_bits")
