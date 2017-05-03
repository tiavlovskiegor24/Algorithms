from collections import namedtuple
from math import log

def Laplace_probs(ensemble,terminate):
    symbols,_ = zip(*ensemble)
    symbols = list(symbols)
    t_symbol,t_prob = terminate
    counts = [0 for _ in symbols]
    total_counts = sum(counts)
    n = len(counts)
    probs = [(count+1)*(1-t_prob)/(total_counts+n) \
             for count in counts]
    
    s_pointers = {}
    for i,symbol in enumerate(symbols):
        s_pointers[symbol] = i

    probs.append(t_prob)
    symbols.append(t_symbol)

    while True:
        next_symbol = yield zip(symbols,probs)

        if next_symbol == t_symbol:
            #print "End of message"
            entropy = sum([prob*log(1/prob,2) for prob in probs[:-1]])
            #print "Entropy is {}".format(entropy)
            # reset counts and probs
            counts = [0 for _ in counts]
            total_counts = sum(counts)
            probs = [(count+1)*(1-t_prob)/(total_counts+n) \
                     for count in counts]
            probs.append(t_prob)

            continue

        if next_symbol is None:
            continue

        if next_symbol not in s_pointers:
            print "Invalid symbol"
            continue

        counts[s_pointers[next_symbol]] += 1
        total_counts = sum(counts)
        probs = [(count+1)*(1-t_prob)/(total_counts+n) \
                 for count in counts]
        probs.append(t_prob)

        
            
def const_probs(ensemble,terminate):
    if ensemble is None:
        return 
    symbols,probs = zip(*ensemble)
    symbols = list(symbols)
    t_symbol,t_prob = terminate
    probs = [prob*(1-t_prob) for prob in probs]
    probs.append(t_prob)
    symbols.append(t_symbol)
    while True:
        symbol = yield zip(symbols,probs)
        if symbol not in symbols:
            print "Invalid symbol"
            continue
        if symbol == t_symbol:
            print "End of message"
            
            continue

def cum_probs(ensemble = None):
    if ensemble is None:
        return
    Q = {}
    R = {}
    symbols,_ = zip(*ensemble)
    #Q = namedtuple("Lower_cum_probs",symbols)
    #R = namedtuple("Upper_cum_probs",symbols)
    cum_prob = 0
    # dict implementation
    for symbol,prob in ensemble:
        Q[symbol] = cum_prob
        #setattr(Q,symbol,cum_prob)
        cum_prob += prob
        R[symbol] = cum_prob
        #setattr(R,symbol,cum_prob)

    Q = namedtuple("Lower_cum_probs",symbols)(**Q)
    R = namedtuple("Lower_cum_probs",symbols)(**R)
    return Q,R
    '''
    list implemetations
    if Q:
        Q.append(prob+Q[-1])

    else:
        Q.append(prob)

    R.append(1-Q[-1])

    return zip(symbols,Q),zip(symbols,R)
    '''
    
class arithmetic_codes(object):
    def __init__(self,model_class,ensemble,terminate):

        self.t_symbol,t_prob = terminate

        self.model = model_class(ensemble,\
                                 ("terminate",t_prob))
        
        
    def decode(self,code):
        Q,R = cum_probs(self.model.send(None))
        n_symbols = len(Q)
        message = ""
        u = 0.
        v = 1.
        p = v - u
        for i,d in enumerate(code):
            
            #update interval
            u += p*0.5*int(d)
            v -= p*0.5*(1-int(d))
            p = v - u
            # loop through the symbols
            idx = 0
            #for idx,symbol in enumerate(Q._fields):
            while True:

                symbol = Q._fields[idx % n_symbols]
                if u < getattr(Q,symbol):
                    break
                
                if v > getattr(R,symbol):
                    idx += 1
                    continue

                if symbol == "terminate":
                    #terminate decoding
                    print "Hello"
                    return message+self.t_symbol

                #update message 
                message += symbol

        
                # rescale interval
                u -= getattr(Q,symbol)
                v -= getattr(Q,symbol)

                u /= (getattr(R,symbol) - getattr(Q,symbol))
                v /= (getattr(R,symbol) - getattr(Q,symbol))
                p = v - u
                
                Q,R = cum_probs(self.model.send(symbol))
                idx = 0
        return message

    def terminate_code(self,u,v,code):
        
        while True:
            while True:
                if u >= 0.5:
                    code += "1"
                    u -= 0.5
                    v -= 0.5
                elif v <= 0.5:
                    code += "0"
                else:
                    break

                u /= 0.5
                v /= 0.5

            if u == 0:
                code += "0"
                return code
            elif v == 1:
                code += "1"
                return code
            elif (0.5-u) >= (v-0.5):
                v = 0.5
            else:
                u = 0.5
                
    def encode(self,message):
        Q,R = cum_probs(self.model.send(None))
        code = ""
        u = 0.
        v = 1.
        p = v-u
        
        for i,c in enumerate(message):

            if c == self.t_symbol:
                self.model.send("terminate")
                v = u + p*getattr(R,"terminate")
                u += p*getattr(Q,"terminate")
                code = self.terminate_code(u,v,code)
    
                return code
            
            v = u + p*getattr(R,c)
            u += p*getattr(Q,c)

            p = v-u

            while True:
                if v <= .5:
                    code += "0"
                elif u > .5:
                    code += "1"
                    u -= .5
                    v -= .5
                else:
                    Q,R = cum_probs(self.model.send(c))
                    break

                u /= .5
                v /= .5
                p = v-u
        
        
if __name__ == "__main__":
    symbols = ["a","b"]
    probs = [0.1,0.9]
    terminate = ("#",.1)
    #model = const_probs(zip(symbols[:],probs),terminate)
    #model.send(None)
    #print model.send("a")
    #L_model = Laplace_probs(symbols[:],terminate)
    #print L_model.send(None)
    #print L_model.send("a")
    #mes = "abababbbbaaabbbbbbbbbbbababbbbbabbabaababbabbbbabbabbabbbbaabbbbabbabbbbbbabbbabbabbabbbbbbbbbbbbababbbbabbabbbababba#"
    #mes = "bbbbbbbbbbbabbbbbbbbcbbabbabbbbcbbbbbbbbbabbbabbbbbabbbbbbbbbbbbbbbabbbbbbbbbbbabbbbbbbabbbbbbbbbbabbbbbbbabbbbabbbbabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcbbbbbbbbabbbbbbabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbabbbbbbcbbbbbbabbbbbbbbbbbbbabbbbbbbbbbbbbbbbbbabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbabbbbbbcbbbbbb#"
    
    #mes = "aabaabbabbbbabbbabbabbbbbabbabbabbbabbaaabba#"
    mes  = "aaaaaaaaaaaaabaaaaaaaaaaaaaabaaaaaaabaaaaaaaaabaaaaaaaaaaaaaababaaaaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaab#"
    print mes
    ac = arithmetic_codes(Laplace_probs,zip(symbols,probs),terminate)
    cc = arithmetic_codes(const_probs,zip(symbols,probs),terminate)
    code = ac.encode(mes)
    print code
    m = ac.decode(code)
    print "\n",m
    
    print m == mes
