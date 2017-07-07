from collections import namedtuple
from math import log
from fractions import gcd,Fraction

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
        

def add_fractions(frac1,frac2):
    num = frac1[0]*frac2[1]+frac1[1]*frac2[0]
    if num == 0:
        den = 1
    else:
        den = frac1[1]*frac2[1]
    divisor = gcd(num,den)
    
    return num/divisor,den/divisor

def mul_fractions(frac1,frac2):
    num = frac1[0]*frac2[0]
    if num == 0:
        den = 1
    else:
        den = frac1[1]*frac2[1]
    divisor = gcd(num,den)
    return num/divisor,den/divisor

def compl_fraction(frac):
    return frac[1]-frac[0],frac[1]

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

def cum_probs_rounded(ensemble = None,precision = 16):
    if ensemble is None:
        return
    Q = {}
    R = {}
    symbols,counts = zip(*ensemble)
    total_counts = sum(counts)
    del counts
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
    return Q,R,total_counts

        
def cum_probs(ensemble = None):
    if ensemble is None:
        return
    Q = {}
    R = {}
    symbols,counts = zip(*ensemble)
    total_counts = sum(counts)
    del counts
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
    return Q,R,total_counts
    '''
    list implemetations
    if Q:
        Q.append(prob+Q[-1])

    else:
        Q.append(prob)

    R.append(1-Q[-1])

    return zip(symbols,Q),zip(symbols,R)
    '''
'''
def binary_generator(x):
    remainder = x
    scale = -1
    while True:
        digit,quotient = divmod(remainder,2**scale)
        if digit < 1:
            scale -= 1
            yield "0"
        else:
            yield "1"
            remainder = quotient
            scale -= 1

def binary_generator(num_den,scale=1):
    num,den = num_den
    remainder = x
    scale = 1
    while True:

        if 2*num >= den:
            digit = "1"
        else:
            digit = "0"
            
        terminate = yield digit
        if terminate:
            return scale,(num,den)
        
        num = (2*num) - (int(digit) * den)
            
        scale += 1

def binary_generator(num_den,scale=1):
    num,den = num_den
    scale = scale
    while True:

        if 2*num >= den:
            digit = "1"
        else:
            digit = "0"
            
        stop = yield digit,scale
        if stop == "stop":
            yield (num,den),scale
            break
        
        num = (2*num) - (int(digit) * den)
            
        scale += 1
'''
def binary_discretizer(frac,precision = 16):
    frac = frac
    for i in range(precision):

        if 2*frac.numerator >= frac.denominator:
            digit = "1"
        else:
            digit = "0"
            
        stop = yield digit
        if stop == "stop":
            yield frac,scale
            break
        
        frac = 2*frac-int(digit)


def binary_generator(frac,scale=1):
    frac = frac
    scale = scale
    while True:

        if 2*frac.numerator >= frac.denominator:
            digit = "1"
        else:
            digit = "0"
            
        stop = yield digit,scale
        if stop == "stop":
            yield frac,scale
            break
        
        frac = 2*frac-int(digit)
        
        
        scale += 1

class Arithmetic_Codes(object):
    def __init__(self,model_class,ensemble,terminate):

        self.t_symbol,t_prob = terminate

        self.model = model_class(ensemble,\
                                 ("terminate",t_prob))
        
        
    def decode(self,code):
        Q,R,total_counts = cum_probs(self.model.send(None))
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
                    #print "Hello"
                    return message+self.t_symbol

                #update message 
                message += symbol

        
                # rescale interval
                u -= getattr(Q,symbol)
                v -= getattr(Q,symbol)

                u /= (getattr(R,symbol) - getattr(Q,symbol))
                v /= (getattr(R,symbol) - getattr(Q,symbol))
                p = v - u
                
                Q,R,total_counts = cum_probs(self.model.send(symbol))
                idx = 0
        return message

    def terminate_code(self,u,v,code):

        half = Fraction(1,2)
        while True:
            while True:
                if u >= half:
                    code += "1"
                    u -= half
                    v -= half
                elif v <= half:
                    code += "0"
                else:
                    break

                u /= half
                v /= half

            if u == 0:
                code += "0"
                return code
            elif v == 1:
                code += "1"
                return code
            elif (half-u) >= (v-half):
                v = half
            else:
                u = half
                
    def encode(self,message):
        Q,R,total_counts = cum_probs(self.model.send(None))
        code = ""
        u = Fraction(0,1)
        u_scale = 1
        v = Fraction(1,1)
        v_scale = 1
        #p = v-u
        
        for i,c in enumerate(message):

            #print c

            if c == self.t_symbol:
                c = "terminate"

            u_update = Fraction(getattr(Q,c),total_counts)
            v_update = Fraction(getattr(R,c),total_counts)

            #print u,v
            #print u_update,v_update
            
            
            '''
            u = add_fractions(mul_fractions(u,compl_fraction(u_update)),
                             mul_fractions(v,u_update))

            v = add_fractions(mul_fractions(u,compl_fraction(v_update)),
                             mul_fractions(v,v_update))
            '''
            u = u*(1-u_update) + v*u_update
            v = u*(1-v_update) + v*v_update

            #u = u.numerator,u.denominator
            #v = v.numerator,v.denominator
            

            if c == "terminate":
                #print u
                #print v
                code = self.terminate_code(u,v,code)

                return code

            #v = add_fractions(u,getattr(R,c))
            #u = add_fractions(u,getattr(Q,c))
            #v = getattr(R,c)
            #u = getattr(Q,c)

            #p = v-u
            #print u,v
            
            b_gen_v = binary_generator(v,v_scale)
            b_gen_u = binary_generator(u,u_scale)
            
            while True:
                v_b,scale_v = b_gen_v.next()
                u_b,scale_u = b_gen_u.next()

                assert scale_v == scale_u
                #print v_b,u_b

                if v_b == "0":
                    code += "0"
                elif u_b == "1":
                    code += "1"
                    #u -= .5
                    #v -= .5
                else:
                    #print "Hello"
                    u,scale_u = b_gen_u.send("stop")
                    v,scale_v = b_gen_v.send("stop")
                    #u = Fraction(*u)
                    #v = Fraction(*v)
                    
                    assert scale_v == scale_u,"interval scales do not match"
                    Q,R,total_counts = cum_probs(self.model.send(c))
                    break

                #print code
                
                '''
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
                '''
        
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

    #print mul_fractions((3,5),(12,89))
    
    mes = "aabaabbabbbbabbbabbabbbbbabbabbabbbabbaaabba#"
    mes  = 20*"aaaaaaaaaaaaabaaaaaaaaaaaaaabaaaaaaabaaaaaaaaabaaaaaaaaaaaaaababaaaaaaaaaaaaaaaaaaaaaaaaaabbaaaaaaab"+"#"
    print len(mes)
    print mes
    ac = arithmetic_codes(Laplace_probs,zip(symbols,probs),terminate)
    #cc = arithmetic_codes(const_probs,zip(symbols,probs),terminate)
    code = ac.encode(mes)
    print len(code)
    print code
    #m = ac.decode(code)
    #print "\n",m
    
    #print m == mes
