from message_passing import *

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


if __name__=="__main__":
    
    squad = Graph()
    n_soldiers = 10
    for i in range(n_soldiers):
        if i == 0:
            connections = []
        else:
            connections = [str(i-1)]
        node = Soldier(name=str(i),connections = connections)
        squad.add_node(node)
        #print squad.leaves

    squad.add_node(Soldier(name=str(i+1),connections = ["4"]))
    squad.add_node(Soldier(name=str(i+2),connections = [str(i+1)]))
    
    
    squad.run()

    for i in squad.nodes["Soldier"].values():
        #print i.count()
        if i.count() != len(squad.nodes["Soldier"]):
            print "error with ",i.name
            break
    else:
        print "everything is great"
        print "there are {} soldiers in the squad".format(i.count())
