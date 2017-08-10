from collections import namedtuple,OrderedDict
from math import log

def Laplace_probs(ensemble,terminate):
    symbols,_ = zip(*ensemble)
    symbols = list(symbols)

    t_symbol,t_prob = terminate
    t_count = 1

    initial_counts = int(t_count/t_prob)
    initial_counts = initial_counts-t_count - (initial_counts-t_count) % len(symbols)
    initial_counts = initial_counts/len(symbols)
    
    counts = [initial_counts for _ in symbols]
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
        next_symbol = yield zip(symbols,[count+1 for count in counts]+[t_count])#probs)

        if next_symbol == t_symbol:
            #print "End of message"
            entropy = sum([prob*log(1/prob,2) for prob in probs[:-1]])
            print "Entropy is {}".format(entropy)
            # reset counts and probs
            counts = [initial_counts for _ in counts]
            total_counts = sum(counts)
            probs = [(count+1)*(1-t_prob)/(total_counts+n) \
                     for count in counts]
            probs.append(t_prob)
            t_count = max(1,total_counts/9)

            continue

        if next_symbol is None:
            continue

        if next_symbol not in s_pointers:
            print "Invalid symbol"
            continue

        counts[s_pointers[next_symbol]] += 1
        total_counts += 1
        probs = [(count+1)*(1-t_prob)/(total_counts+n) \
                 for count in counts]
        probs.append(t_prob)
        t_count = max(1,total_counts/9+1)
        
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

def cum_intervals(ensemble = None,u = 0,r = None,precision = 16):
    if r is None:
        r = 2 ** (precision)

    assert u+r <= 2**precision
    whole = 2**precision
    
    if ensemble is None:
        return
    Q = OrderedDict()
    R = OrderedDict()
    symbols,counts = zip(*ensemble)
    total_count = sum(counts)
    
    del counts
    cum_count = 0
    prev = 0

    for symbol,count in ensemble:
        cum_count += count
        assert cum_count * r <= total_count * 2**(precision)
        R[symbol] = prev = cum_count*r/total_count

    assert R.values()[-1] <= r
    for i,s in enumerate(R.keys()):
        Q[s] = (R.values()[i-1] if i > 0 else u)
        R[s] = max(Q[s]+1,R[s] + u)
        
    return Q,R

        
def binary(frac,precision = 16):
    frac = frac
    b = 0
    for i in range(precision):

        if 2*frac.numerator >= frac.denominator:
            d = 1
        else:
            d = 0

        b =  (b << 1) + d
        
        frac = 2*frac-int(d)

    return b

class Arithmetic_Codes(object):
    def __init__(self,model_class,ensemble,terminate):

        self.t_symbol,t_prob = terminate

        self.model = model_class(ensemble,\
                                 ("terminate",t_prob))

        self.precision = 16
        
        
    def decode(self,code):
        precision = self.precision
        whole = 2**precision
        half = whole/2
        quarter = whole/4
        
        z = 0
        u = 0
        v = whole
        r = v-u
        s = None
        
        #initialise z down to precision
        pointer = 0
        for i in range(min(precision,len(code))):

            z += int(code[pointer])*2**(precision-(i+1))
            pointer += 1

        while True:
            
            Q,R = cum_intervals(self.model.send(s),u = u,r = r,precision = precision)

            for s in Q:
                if Q[s] <= z and R[s] > z:
                    break
            else:
                break

            if s == "terminate":
                yield self.t_symbol
                break
                    
            yield s
    
            u = Q[s]
            v = R[s]
            r = v-u
    
            while v <= half:
                u *= 2
                v *= 2
                r = v-u
                z *= 2
                if pointer < len(code):
                    z += int(code[pointer])
                    pointer += 1


            while u >= half:
                u = (u-half) * 2
                v = (v-half) * 2
                r = v - u
                z = (z-half) * 2
                if pointer < len(code):
                    z += int(code[pointer])
                    pointer += 1



            while u >= quarter and v <= 3*quarter:
                u = (u-quarter) * 2
                v = (v-quarter) * 2
                r = v - u
                z = (z-quarter) * 2
                if pointer < len(code):
                    z += int(code[pointer])
                    pointer += 1
                
    def encode(self,message):
        precision = self.precision
        whole = 2**precision
        half = whole/2
        quarter = whole/4
        #code = ""
        u = 0
        v = whole
        r = v-u
        Q,R = cum_intervals(self.model.send(None),u = u,r = r,precision = precision)
        
        s = 0
        for ind,c in enumerate(message):
            if c == self.t_symbol:
                c = "terminate"
            
            u = Q[c]
            v = R[c]
            r = v - u

            while v <= half:
                
                yield "0"
                for _ in range(s):
                    yield "1"
                s = 0
                u *= 2
                v *= 2
                r = v-u

            while u >= half:
                
                yield "1"
                for _ in range(s):
                    yield "0"
                s = 0
                u = (u-half) * 2
                v = (v-half) * 2
                r = v-u

            while u >= quarter and v <= half+quarter:
                u = (u-quarter) * 2
                v = (v-quarter) * 2
                r = v-u
                s += 1

            if c == "terminate":            
                if u <= quarter:
                    yield "0"
                    for _ in range(s+1):
                        yield "1"
                else:
                    yield "1"
                    for _ in range(s+1):
                        yield "0"
                break
            
            Q,R = cum_intervals(self.model.send(c),u = u,r = r,precision = precision)
            

if __name__ == "__main__":

    symbols = ["a","b"]
    probs = [0.1,0.9]

    terminate = ("#",.1)
    ac = Arithmetic_Codes(Laplace_probs,zip(symbols,probs),terminate)
    mes = "aaaaaaaaaaaaaaaaaaaaaaaabaaaaaaabaaaaaaaabaaaaaaaabaaaaaaaaaaabaaabaaaaaaabaaaaaaabaaabbaaaaaaaaaaabaaabbababaaabbaaabaaaaaaabbbaaaaabbbaaaaaaaaaaaaabbabb"*1000+"#"
    #mes = "b#"
    code = list(ac.encode(mes))
    ac = Arithmetic_Codes(Laplace_probs,zip(symbols,probs),terminate)
    print "".join(code)
    
    d_mes = list(ac.decode(code))
    print "\n","".join(d_mes)
    print len(mes)
    print len(code)
    assert mes == "".join(d_mes)
    
