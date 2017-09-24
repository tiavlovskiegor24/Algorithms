from collections import deque,OrderedDict

class Message(object):
    '''Generic class for messages between nodes'''
    def __init__(self,to,from_,content):
        self.to = to
        self.from_ = from_
        self.description = "Message to '{}' from '{}'".format(to,from_)
        self.content = content


class Node(object):
    '''Generic class for the node in message passing graph'''

    def __init__(self,name = None,type_=None,connections = []):
        self.name = name
        self.type_ = type_
        self.received = {}
        self.connections = set()
        self.to_send = {}
        self.sent_count = 0
        for con_name in connections:
            self.add_connection(con_name)
        
        
    def n_connections(self):
        '''method returns the number of connections'''
        return len(self.received)

    def get_connections(self):
        '''method returns the list of connection names'''
        return self.received.keys()
    
    def add_connection(self,con_name):
        '''method adds new connection to the node'''
        self.received[con_name] = None
        self.to_send[con_name] = []
        self.connections.add(con_name)

    def reset_sent_count(self):
        self.sent_count = 0
        

    def send(self,to_list = None,
             init = False,
             limit = None,
             reset_sent_count = False,
             verbose = False,
             **kwargs
    ):
        '''
        method sends messages to connections if 
        received messages are available
        '''

        if reset_sent_count:
            self.sent_count = 0
            
        if limit is not None:
            if self.sent_count == limit*self.n_connections():
                return

        if to_list is None:
            to_list = list(self.get_connections())
            
        for to_connection in to_list:
            
            #if to_connection in self.sent:
             #   yield None
              #  continue
                
            if not init and len(self.to_send[to_connection]) < self.n_connections()-1:
                yield None
                continue

            feed_dict = dict(self.to_send[to_connection])
            del self.to_send[to_connection][:]
            
            if verbose:
                print "creating message from {} to {}".format(self.name,to_connection)    
            yield (to_connection,self.name,self.message_func(to_connection,feed_dict,**kwargs))
            if not init:
                self.sent_count += 1

    def receive(self,message):
        '''method to receive message from a connection'''
        to,from_,content = message
        assert to == self.name
        assert from_ in self.received,(self.name,from_,self.get_connections())
        self.received[from_] = content

        for c in self.get_connections():
            if c != from_:
                self.to_send[c].append((from_,content))

        
    def message_func(self,to_connection,**kwargs):
        '''method generates messages for the connected nodes'''
        return lambda x:None

class Recurrent_Node(Node):
    '''Node which can send message to several "timesteps" of itself'''
    def __init__(self,n_steps = 0,*args,**kwargs):
        super(Recurrent_Node,self).__init__(*args,**kwargs)
        self.n_steps = n_steps
        self.current_step = 0
        for i in range(n_steps):
            self.add_connection("{}_{}".format(self.name,i))

    def send(self,*args,**kwargs):
        to_list = list(self.get_connections())
        exclude_set = set(["{}_{}".format(self.name,i) for i in range(self.n_steps)])
        to_list = [con for con in to_list if con not in exclude_set]
        for message in super(Recurrent_Node,self).send(to_list = to_list,*args,**kwargs):
            yield message

    def recieve(self,message,*args,**kwargs):
        to,from_,content = message
        if to.split("_")[0] in self.received:
            message = (to.split("_")[0],from_,content)
            super(Recurrent_Node,self).receive(message)
        else:
            print "Message misdirected",to,from_
            
        
        
    
class Graph(object):
    '''object which routes messages between nodes'''
    
    def __init__(self,type_=None):
        self.type_ = type_
        self.nodes = {"all":OrderedDict()}
        self.leaves = {}
        self.message_Q = deque()
    
    def add_node(self,node,category):

        if category is not None:
            if category not in self.nodes:
                self.nodes[category] = OrderedDict()

            self.nodes[category][node.name] = node
            
        if node.type_ not in self.nodes:
            self.nodes[node.type_] = {}
        self.nodes[node.type_][node.name] = node

        if node.name not in self.nodes["all"]:
            self.nodes["all"][node.name] = node

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
            
    def reset_message_Q(self):
        self.message_Q = deque()

    def clear_message_Q(self):

        c = 0
        while self.message_Q:
            c += 1
            message = self.message_Q.popleft()
            to = message[0]
            assert to in self.nodes,(to,self.nodes.keys())
            to_node = self.nodes[to]
            to_node.receive(message)
            if c > 1e6:
                #print "infinite loop"
                break #return
        
                
    def run(self,n_iters = 1e6,init_node_type = None,**kwargs):
        '''method runs the forward-backward message passing'''

        #for node_name,node in self.leaves.iteritems():
         #   messages = list(m for m in node.send() if m is not None)
          #  message_Q.extend(messages)

          
        if init_node_type is None:
            init_node_type = "all"
            init = False
        else:
            init = True
            
            
        for node_name,node in self.nodes[init_node_type].iteritems():
            messages = list(m for m in node.send(init = init,**kwargs) if m is not None)
            self.message_Q.extend(messages)
                
        c = 0
        while self.message_Q:
            c += 1
            message = self.message_Q.popleft()
            to = message[0]
            assert to in self.nodes["all"],(to,self.nodes["all"].keys())
            to_node = self.nodes["all"][to]
            to_node.receive(message)
            #if to not in self.leaves:
            for m in to_node.send(**kwargs):
                if m is not None:
                    self.message_Q.append(m)
            if c > n_iters:
                print "infinite loop"
                break #return
            
        print "Message passing is finished"
