from collections import deque

class Node(object):
    def __init__(self,name,type_,connections):
        self.name = name
        self.type_ = type_
        self.connections = connections
        self.n_connections = len(self.connections)
        self.connections_name = connections_name
        self.connections_type = connections_type
        self.received = {c:[] for c in self.connections}
        self.to_send = {c:[] for c in self.connections}



    def send(self,to_connection = None):

        
        if to_connection is not None:
            to_list = [to_connection]
        else:
            to_list = list(self.connections)

        for to_connection in to_list:
            if len(self.to_send[to_connection]) < self.n_connection-1:
                yield None

            feed_dict = dict(self.to_send[to_connection])
            self.to_send[to_connection] = []
            yield self.message_func(to_connection,feed_dict)


    def receive(self,message):
        to,from_,content = message
        assert to == self.name
        assert from_ in self.connections
        self.recieved[from_] = content

        for c in (self.connections-from_):
            self.to_send[c].append((from_,content))

        
    def message_func(self,to_connection,**kwargs):
        '''method generates messages for the connected nodes'''
        return lambda x:None

        
class Factor(Node):

    def __init__(self,factor_func,**kwargs):
        super(Factor,self).__init__(type_ = "Factor",**kwargs)
        self.compute = factor_func

    def __call__(self,**kwargs):
        return self.compute(**kwargs)

    def message_func(self,to_variable,feed_dict):

        evaluations = {}
        for variable,func in feed_dict:
            for value in self.variables[variable]:
                evaluations[(variable,value)] = func(v)
        
                            
        remaining = set(self.variables.keys())-set([to_variable])
        g = self.generate_combinations(self.variables,remaining)
        
        def message(x,**kwargs):
            marginal = 0
            for instances_list in g:
                feed_dict = dict([(to_variable,x)]+instances_list)
                factor_value = self.compute(**feed_dict)
                cum_prod = reduce(lambda cum,var_val: cum * evaluations[var_val],instances_list)
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
                    g = generate_combinations(variables_dict,remaining - set([variable]))
                    for instances_list in g:
                        yield [(variable,value)]+instances_list


                        
class Variable(Node):

    def __init__(self,**kwargs):
        super(Variable,self).__init__(type_ = "Variable",**kwargs)

    def message_func(self,to_factor,feed_dict):
        
        def message(x):
            '''message from Variable {} to Factor {}'''.format(self.name,to_factor)
            return reduce(lambda cum,f:cum*f(x),feed_dict.values())

        return message

class Solder(Node):
    def message_func(self,to_neighbour,feed_dict):
        def message(x):
            '''message from Solder {} to Solder {}'''.format(self.name,to_neighbour)

            return reduce(lambda cum,v:cum+v,feed_dict.values(),1)


class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.leaves = {}
    
    def add_node(self,node):
        if node.type_ not in self.nodes:
            self.nodes[node.type_] = {}
            
        self.nodes[node.type_][node.name] = node

        if node.n_connections == 1:
            self.leaves[node.name] = node

    def run(self):
        message_Q = deque()
        for node_name,node in self.leaves.iteritems():
            messages = list(m for m in node.send() if m is not None)
            message_Q.append(messages)

        while message_Q
    
    
    
def f_1(x1):
    return 0.9 if x1 == 1 else 0.1

def f_2(x2)
    return 0.9 if x2 == 1 else 0.1

def f_3(x3)
    return 0.1 if x2 == 1 else 0.9


def f_4(x1,x2):
    return 1 if x1 == x2 else 0

def f_4(x2,x3):
    return 1 if x3 == x3 else 0


    
