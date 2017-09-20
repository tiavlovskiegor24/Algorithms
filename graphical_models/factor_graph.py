from message_passing import *
from collections import namedtuple

class Factor(Node):

    #named tuple for the convenient factor creation
    factor_tuple = namedtuple("Factor_tuple",["name","factor_func","connections"])
    
    def __init__(self,factor_func,*args,**kwargs):
        super(Factor,self).__init__(type_ = "Factor",*args,**kwargs)
        self.compute = factor_func

    def __call__(self,**kwargs):
        return self.compute(**kwargs)

    def message_func(self,to_variable,feed_dict):

        evaluations = {}
        variables = {}
        for variable,evals in feed_dict.iteritems():
            variables[variable] = set(evals.keys())
            for v in evals:
                evaluations[(variable,v)] = evals[v]
            
        def message(x,**kwargs):
            marginal = 0

            remaining = set(variables.keys())
            if variables:
                g = self.generate_combinations(variables,remaining)
            else:
                g = [[]]
            
            for instances_list in g:
                feed_dict = dict([(to_variable,x)]+instances_list)
                factor_value = self.compute(feed_dict)
                cum_prod = reduce(lambda cum,var_val: cum * evaluations[var_val],
                                  instances_list,1)

                marginal += factor_value*cum_prod
            return marginal

        return message

    @staticmethod
    def generate_combinations(variables_dict,remaining):

        for variable in remaining:    
            for value in variables_dict[variable]:
                if len(remaining) == 1:
                    yield [(variable,value)]
                else:
                    g = Factor.generate_combinations(variables_dict,
                                              remaining - set([variable]))
                    for instances_list in g:
                        yield [(variable,value)]+instances_list


                        

class Variable(Node):

    # namedtuple for simplified initialisation of variable nodes
    variable_tuple = namedtuple("Variable_tuple",["name","domain","connections","observed"])
    
    def __init__(self,domain,observed = None,*args,**kwargs):
        super(Variable,self).__init__(type_ = "Variable",*args,**kwargs)
        self.domain = set(domain)
        self.observed = None if observed is None else set([observed])

    def set_as_observed(self,value):
        assert value in self.domain
        self.observed = set([value])

    def set_as_unobserved(self):
        self.observed = None

    def message_func(self,to_factor,feed_dict):

        
    #    def message(x):
     #       return reduce(lambda cum,f:cum*f(x),feed_dict.values(),1)

      #  return (message,self.domain if self.observed is None else self.observed)

        evaluations = {}
        values = self.domain if self.observed is None else self.observed
        for v in values:
            evaluations[v] = reduce(lambda cum,f:cum*f(v),feed_dict.values(),1)

        norm_const = sum(evaluations.values())
        for v in evaluations:
            evaluations[v] = evaluations[v]*1./norm_const 

        return evaluations
    
    
    def compute_marginal(self,v):

        assert v in self.domain
        
        if self.observed is not None:
            #print "Variable is observed with value {}".format([x for x in self.observed][0])
            return 1. if v in self.observed else 0.
        
        marginal = reduce(lambda cum,f:cum * f(v),self.received.values(),1)

        norm_const = self.compute_norm_const()
        
        return marginal*1./norm_const

    def compute_norm_const(self):
        evaluations = {}
        for value in self.domain:
            evaluations[value] = reduce(lambda cum,f:cum * f(value),self.received.values(),1)

        return sum(evaluations.values())    
    
    
