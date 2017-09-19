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
        for variable,(func,domain) in feed_dict.iteritems():
            variables[variable] = domain
            for value in domain:
                evaluations[(variable,value)] = func(value)
            
        def message(x,**kwargs):
            marginal = 0

            remaining = set(variables.keys())
            if variables:
                g = self.generate_combinations(variables,remaining)
            else:
                g = [[]]
            
            for instances_list in g:
                feed_dict = dict([(to_variable,x)]+instances_list)
                factor_value = self.compute(**feed_dict)
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
                    g = generate_combinations(variables_dict,
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

    def message_func(self,to_factor,feed_dict):
            
        def message(x):
            return reduce(lambda cum,f:cum*f(x),feed_dict.values(),1)

        return (message,self.domain if self.observed is None else self.observed)

    def compute_marginal(self,v):

        if self.observed is not None:
            print "Variable is observed with value {}".format([x for x in self.observed][0])
            return None
        
        assert v in self.domain
        
        
        marginal = reduce(lambda cum,f:cum * f(v),self.received.values(),1)

        norm_const = self.compute_norm_const()
        
        return marginal*1./norm_const

    def compute_norm_const(self):
        evaluations = {}
        for value in self.domain:
            evaluations[value] = reduce(lambda cum,f:cum * f(value),self.received.values(),1)

        return sum(evaluations.values())    
    
    
if __name__=="__main__":
    
    def f_1(r1,x1):
        return 0.9 if x1 == r1 else 0.1

    def f_2(r2,x2):
        return 0.9 if x2 == r2 else 0.1

    def f_3(r3,x3):
        return 0.9 if x3 == r3 else 0.1

    def f_4(x1,x2):
        return 1 if x1 == x2 else 0

    def f_5(x2,x3):
        return 1 if x2 == x3 else 0

    def f_6(x1,x3):
        return 1 if x1 == x3 else 0
    
    graph = Graph()

    factors = [("f1",f_1,["x1","r1"]),
               ("f2",f_2,["x2","r2"]),
               ("f3",f_3,["x3","r3"]),
               ("f4",f_4,["x1","x2"]),
               ("f5",f_5,["x2","x3"]),
               ("f6",f_6,["x1","x3"]),
    ]

    factors = [Factor.factor_tuple(*f) for f in factors]
    
    v_f = {} # variables-factors dictionary
    for factor in factors:
        for v in factor.connections:
            if v not in v_f:
                v_f[v] = [factor.name]
            else:
                v_f[v].append(factor.name)

                
    received_bits = [("r1",[0,1],v_f["r1"],0),
                     ("r2",[0,1],v_f["r2"],1),
                     ("r3",[0,1],v_f["r3"],0)]

    received_bits = [Variable.variable_tuple(*v) for v in received_bits]
    
    transmitted_bits = [("x1",[0,1],v_f["x1"],None),
                       ("x2",[0,1],v_f["x2"],None),
                       ("x3",[0,1],v_f["x3"],None)]

    transmitted_bits = [Variable.variable_tuple(*v) for v in transmitted_bits]


    # convert node_tuples to graph nodes
    factors = [Factor(**factor._asdict()) for factor in factors]
    received_bits = [Variable(**variable._asdict()) for variable in received_bits]
    transmitted_bits = [Variable(**variable._asdict()) for variable in transmitted_bits]
    
    

    for node in received_bits:
        graph.add_node(node,category = "Received")

    for node in transmitted_bits:
        graph.add_node(node,category = "Transmitted")

    for node in factors:
        graph.add_node(node,category = "Factors")

    graph.run(n_iters = 200)

    for i in graph.nodes["Transmitted"].values():
        print i.name,(1,i.compute_marginal(1)),(0,i.compute_marginal(0))
