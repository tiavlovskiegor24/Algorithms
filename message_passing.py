from collections import deque

class Node(object):
    def __init__(self,name = None,type_=None,connections = []):
        self.name = name
        self.type_ = type_
        self.received = {}
        self.to_send = {}
        for con_name in connections:
            self.add_connection(con_name)
        
        
    def n_connections(self):
        return len(self.received)

    def get_connections(self):
        return self.received.keys()
    
    def add_connection(self,con_name):
        self.received[con_name] = None
        self.to_send[con_name] = []
        


    def send(self,to_connection = None):

        
        if to_connection is not None:
            to_list = [to_connection]
        else:
            to_list = list(self.get_connections())

        for to_connection in to_list:
            
            #if to_connection in self.sent:
             #   yield None
              #  continue
                
            if len(self.to_send[to_connection]) < self.n_connections()-1:
                yield None
                continue

            feed_dict = dict(self.to_send[to_connection])
            self.to_send[to_connection] = []
            #self.sent.add(to_connection)
            yield (to_connection,self.name,self.message_func(to_connection,feed_dict))


    def receive(self,message):
        to,from_,content = message
        assert to == self.name
        assert from_ in self.get_connections()
        self.received[from_] = content

        for c in self.get_connections():
            if c != from_:
                self.to_send[c].append((from_,content))

        
    def message_func(self,to_connection,**kwargs):
        '''method generates messages for the connected nodes'''
        return lambda x:None

        
class Factor(Node):

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

        remaining = set(variables.keys())
        if variables:
            g = self.generate_combinations(variables,remaining)
        else:
            g = [[]]
        
        def message(x,**kwargs):
            marginal = 0
            for instances_list in g:
                feed_dict = dict([(to_variable,x)]+instances_list)
                factor_value = self.compute(**feed_dict)
                cum_prod = reduce(lambda cum,var_val: cum * evaluations[var_val],
                                  instances_list,1)
                marginal += factor_value*cum_prod
            print marginal
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

    def __init__(self,domain,*args,**kwargs):
        super(Variable,self).__init__(type_ = "Variable",*args,**kwargs)
        self.domain = set(domain)

    def message_func(self,to_factor,feed_dict):
        def message(x):
            return reduce(lambda cum,f:cum*f(x),feed_dict.values(),1)

        return (message,self.domain)

    def compute_marginal(self,v):
        assert v in self.domain

        for f in self.received.values():
            print f(v)
        return reduce(lambda cum,f:cum * f(v),self.received.values(),1)

    
class Soldier(Node):

    def __init__(self,*args,**kwargs):
        super(Soldier,self).__init__(type_ = "Soldier",*args,**kwargs)
    
    def message_func(self,to_neighbour,feed_dict):
        def message():
            return reduce(lambda cum,v:cum+v(),feed_dict.values(),1)

        return message

    def count(self):
        self.c = reduce(lambda cum,v:cum+v(),self.received.values(),1)

        return self.c


    
class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.leaves = {}
    
    def add_node(self,node):
        if node.type_ not in self.nodes:
            self.nodes[node.type_] = {}
            
        self.nodes[node.type_][node.name] = node

        if node.name not in self.nodes:
            self.nodes[node.name] = node

        if node.n_connections() == 1:
            self.leaves[node.name] = node

        for con_name in node.get_connections():
            if con_name not in self.nodes:
                continue
            con_node = self.nodes[con_name]
            con_node.add_connection(node.name)
            if con_node.n_connections() == 1:
                self.leaves[con_name] = con_node
            elif con_name in self.leaves:
                del self.leaves[con_name]
            

    def run(self):
        message_Q = deque()
        for node_name,node in self.leaves.iteritems():
            messages = list(m for m in node.send() if m is not None)
            message_Q.extend(messages)
            
        c = 0
        while message_Q:
            message = message_Q.popleft()
            to = message[0]
            assert to in self.nodes,(to,self.nodes.keys())
            to_node = self.nodes[to]
            to_node.receive(message)
            if to not in self.leaves:
                for m in to_node.send():
                    if m is not None:
                        message_Q.append(m)

            if c > 1e5:
                print "infinite loop"
                return
            
        print "finished"
                    
    
if __name__=="__main__":
    
    def f_1(x1):
        return 0.9 if x1 == 1 else 0.1

    def f_2(x2):
        return 0.9 if x2 == 1 else 0.1

    def f_3(x3):
        return 0.1 if x3 == 1 else 0.9


    def f_4(x1,x2):
        return 1 if x1 == x2 else 0

    def f_5(x2,x3):
        return 1 if x2 == x3 else 0


    
    graph = Graph()
    n_soldiers = 10
    for i in range(n_soldiers):
        if i == 0:
            connections = []
        else:
            connections = [str(i-1)]
        node = Soldier(name=str(i),connections = connections)
        graph.add_node(node)
        #print graph.leaves

    graph.add_node(Soldier(name=str(i+1),connections = ["4"]))
    graph.add_node(Soldier(name=str(i+2),connections = [str(i+1)]))
    
    
    graph.run()

    for i in graph.nodes["Soldier"].values():
        #print i.count()
        if i.count() != len(graph.nodes["Soldier"]):
            print "error with ",i.name
            break
    else:
        print "everything is great"


    graph = Graph()

    factors = [("f1",f_1,["x1"]),
               ("f2",f_2,["x2"]),
               ("f3",f_3,["x3"]),
               ("f4",f_4,["x1","x2"]),
               ("f5",f_5,["x2","x3"])]
    
    variables = [("x1",[0,1],["f1"]),
                 ("x2",[0,1],["f2","f4"]),
                 ("x3",[0,1],["f3","f5"])]

    for var in variables:
        name,domain,connections = var
        node = Variable(name = name,domain = domain,connections = connections)
        graph.add_node(node)

    for fac in factors:
        name,factor_func,connections = fac
        node = Factor(name = name,factor_func = factor_func,connections = connections)
        graph.add_node(node)

    graph.run()

    #for i in graph.nodes["Variable"].values():
     #   print i.compute_marginal(1)
        
            
    
    
