from collections import deque

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
        self.to_send = {}
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
        

    def send(self,to_connection = None):
        '''
        method sends messages to connections if 
        received messages are available
        '''
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
        '''method to receive message from a connection'''
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


    
class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.leaves = {}
    
    def add_node(self,node,category):

        if category is not None:
            if category not in self.nodes:
                self.nodes[category] = {}

            self.nodes[category][node.name] = node
            
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
        '''method runs the forward-backward message passing'''
        
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
            
        print "Message passing is finished"
