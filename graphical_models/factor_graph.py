from message_passing import *
from collections import namedtuple
from operator import itemgetter

class Factor(Node):

    #named tuple for the convenient factor creation
    factor_tuple = namedtuple("Factor_tuple",["name","factor_func","connections"])
    
    def __init__(self,factor_func,*args,**kwargs):
        super(Factor,self).__init__(type_ = "Factor",*args,**kwargs)
        self.compute = factor_func

    def __call__(self,**kwargs):
        return self.compute(**kwargs)

    def message_func(self,to_variable,feed_dict,message_type = "sum_prod",**kwargs):

        evaluations = {}
        variables = {}
        for variable,evals in feed_dict.iteritems():
            variables[variable] = set(evals.keys())
            for v in evals:
                evaluations[(variable,v)] = evals[v]
            
        def message(x,**kwargs):
            #if message_type == "sum_prod":
            result = 0
            #elif message_type == "max_sum":
             #   result = -float("inf")

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
                #assert message_type == "max_mult"
                if message_type == "sum_prod":
                    result += factor_value*cum_prod
                elif message_type == "max_mult":
                    result = max(result,factor_value*cum_prod)
            return result

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
        if observed is not None:
            self.set_as_observed(observed)
        else:
            self.set_as_hidden()

    def set_as_observed(self,value):
        assert value in self.domain
        self.observed = value

    def set_as_hidden(self):
        self.observed = None

    def message_func(self,to_factor,feed_dict,message_type = "sum_prod",**kwargs):

        
    #    def message(x):
     #       return reduce(lambda cum,f:cum*f(x),feed_dict.values(),1)

      #  return (message,self.domain if self.observed is None else self.observed)

        self.message_type = message_type
        evaluations = {}
        values = self.domain #if self.observed is None else self.observed
        for v in values:
            evaluations[v] = reduce(lambda cum,f:cum*f(v),feed_dict.values(),1)

        if message_type == "sum_prod":    
            norm_const = sum(evaluations.values())
            if norm_const == 0: print evaluations
            for v in evaluations:
                evaluations[v] = evaluations[v]*1./norm_const 

        #if message_type == "sum_prod":
        if self.observed is None:
            return evaluations
        else:
            return {self.observed:1.}
        #else:
         #   return max(,key = itemgetter(1))

    def unpack_messages(self):
        for from_,f in self.received.iteritems():
            print "\n\tFrom {}".format(from_)
            for v in self.domain:            
               print "\t"*2,v,f(v) 
    
    def compute(self,v):
        
        assert v in self.domain

        if self.observed is not None:
            #print "Variable is observed with value {}".format([x for x in self.observed][0])
            return 1. if v == self.observed else 0.

        result = reduce(lambda cum,f:cum * f(v),self.received.values(),1)
        if self.message_type == "sum_prod":
            norm_const = self.compute_norm_const()
            result = result*1./norm_const
        return result

    def compute_norm_const(self):
        evaluations = {}
        for value in self.domain:
            evaluations[value] = reduce(lambda cum,f:cum * f(value),self.received.values(),1)

        return sum(evaluations.values())    
    
    
class Recurrent_Variable(Variable):
    '''Variable which can send message to several "timesteps" of itself'''
    def __init__(self,n_steps = 1,transition_func = None,observed_steps = None,*args,**kwargs):
        
        super(Recurrent_Variable,self).__init__(*args,**kwargs)
        
        self.n_steps = n_steps
        self.steps = []
        self.steps.append(dict(received = {con:None for con in self.connections},
                          to_send = dict([("n",{})]+
                                         [(con,{}) for con in self.connections])))
        for i in range(1,n_steps-1):
            self.steps.append(dict(received = {con:None for con in self.connections},
                              to_send = dict([("p",{}),("n",{})]+
                                             [(con,{}) for con in self.connections])))
        self.steps.append(dict(received = {con:None for con in self.connections},
                          to_send = dict([("p",{})]+
                                         [(con,{}) for con in self.connections])))
                      
        self.set_as_observed(observed_steps)
        self.go_to_step(0)
        
        self.transition_func = transition_func
        if self.transition_func is None:
            self.transition_func = lambda x: 1
        self.transition_factor = Factor(name="t_factor".format(self.name),
                                        factor_func = self.transition_func,
                                        connections = ["p","n"],
        )

    def set_as_observed(self,observed_steps):
        if observed_steps is not None:
            assert all((v in self.domain) or (v is None) for v in observed_steps)
            assert len(observed_steps)==self.n_steps,(self.n_steps,len(observed_steps))
            self.observed_steps = observed_steps
        else:
            self.observed_steps = [None]*self.n_steps
        self.go_to_step(0)

        
    def go_to_step(self,step):
        self.current_step = step
        self.received = self.steps[step]["received"]

        self.observed = self.observed_steps[step]

        self.to_send = {con:contents for con,contents
                        in self.steps[step]["to_send"].iteritems()
                        if con in self.connections}
        
        self.to_send_steps = self.steps[step]["to_send"]
        #print id(self.to_send_steps["n"]) == id(self.steps[step]["to_send"]["n"])
        #{con:contents for con,contents
                              #in self.steps[step]["to_send"].iteritems()
                              #if con in ["p","n"]}

    def send(self,init = False,*args,**kwargs):

        #send messages to outside connection
        for message in super(Recurrent_Variable,self).send(when = self.current_step,init = init,*args,**kwargs):
            yield message
        
        #now send messages to next or previous steps
        
        for step in ["p","n"]:

            if step not in self.to_send_steps:
                continue

            #skip
            if not init and len(self.to_send_steps[step]) < len(self.to_send_steps)-1:
                #print "\t",step,self.current_step
                continue
            to_step = step
            
            from_step = "p" if to_step == "n" else "n"
            feed_dict = dict(self.to_send_steps[to_step])
            #del self.to_send_steps[to_step][:]

            
            self.to_send_steps[to_step].clear()

            assert len(self.to_send_steps[to_step]) == len(self.steps[self.current_step]["to_send"][to_step])

            
            message_to = message_tuple(to = "t_factor",
                                       from_ = from_step,
                                       when = self.current_step,
                                       content = self.message_func(to_step,feed_dict,**kwargs))

            #print "\t",message_to
            self.transition_factor.receive(message_to,*args,**kwargs)            
            message_back = list(self.transition_factor.send(when = self.current_step,show = True,**kwargs)).pop()
            assert message_back is not None

                        
            # go to next step
            next_step = self.current_step + (1 if to_step == "n" else -1)
            #print "{} goes from step {} to {}".format(self.name,self.current_step,next_step)
            self.go_to_step(next_step)
            
            
            #to_step,_,content = message_back
            message_back = message_back._asdict()

            #print "Message from {} to {} at step {}".format(message_back["from_"],message_back["to"],self.current_step)
            #for v in self.domain:
             #   print v,message_back["content"](v)
            #print
            
            from_step = "p" if message_back["to"] == "n" else "n"
            self.received[from_step] = message_back['content']
            
            for step in ["p","n"]:
                if step != from_step and step in self.to_send_steps:
                    self.to_send_steps[step][from_step] = message_back["content"]
                    #self.to_send_steps[step].append((from_step,message_back['content']))

            #send any messages from following step
            list(self.send(*args,**kwargs))
            #print self.current_step
                
        
    def receive(self,message,*args,**kwargs):
        #assert message.when == self.current_step,(message.when,self.current_step,self.name)
        super(Recurrent_Variable,self).receive(message = message,*args,**kwargs)
        #to,from_,content = message

        message = message._asdict()

        #print "Message from {} to {}".format(message["from_"],message["to"])
        #for v in self.domain:
         #   print v,message["content"](v)
        
        for step in ["n","p"]:
            if step in self.to_send_steps:
                self.to_send_steps[step][message['from_']] = message["content"]
                #self.to_send_steps[step].append((message['from_'],message['content']))


class Observed_Recurrent_Variable(Variable):
    def __init__(self,observed_steps = [],*args,**kwargs):
        super(Observed_Recurrent_Variable,self).__init__(*args,**kwargs)
        self.set_as_observed(observed_steps)        
    
    def send(self,*args,**kwargs):
        assert self.observed_steps,"Variable node did not recieve list of observations"
        try:
            self.observed = self.observations.next()
        except StopIteration:
            return

        for message in super(Observed_Recurrent_Variable,self).send(*args,**kwargs):
            yield message

    def reset(self):
        self.observations = iter(self.observed_steps)

    def set_as_observed(self,observed_steps):
        observed_steps = observed_steps if observed_steps is not None else []
        if observed_steps:
            assert all(obs in self.domain for obs in observed_steps),(observed_steps,self.domain)
        self.observed_steps = observed_steps
        self.reset()

    
              

if __name__=="__main__":

    node = Observed_Recurrent_Variable(name = "test",
                                       #observed_steps = [1,0,0,1],
                                       connections = ["factor"],
                                       domain = [0,1],
    )

    node.set_observations([1,0,1,1,0,1,1,0])

    '''
    node = Recurrent_Variable(name = "test",
                              n_steps = 3,
                              observed_steps = None,
                              connections = ["factor"],
                              domain = [0,1],
                              transition_func = None)

    node.set_as_observed([1,0,1])
    '''

    for i in range(150):
        
        
        node.receive(message_tuple(to = "test",
                                   from_ = "factor",
                                   when = None,
                                   content = lambda x:True)
                     )
        out  = list(node.send())
        if out:
            print out
    exit()




    for i in range(5):
        
        print
        print node.current_step
        for i,step in enumerate(node.steps):
            print "\t",i,step["to_send"]
        node.receive(message_tuple(to = "test",
                                   from_ = "factor",
                                   when = node.current_step,
                                   content = lambda x:True)
                     )
        print
        for i,step in enumerate(node.steps):
            print "\t",i,step["to_send"]

        print list(node.send())
    exit()


        
    print node.steps[node.current_step]
    print
    
    print node.current_step
    print node.to_send_steps
    print node.to_send
    print node.steps[node.current_step]
    print
    
    
    print node.current_step
    print node.to_send_steps
    print node.to_send
    print node.steps[node.current_step]
    print
    
    exit()
    print list(node.send())
    print node.current_step
    print node.to_send_steps
    print node.to_send
    print node.to_send_steps
    print node.steps[node.current_step]
    print list(node.send())
