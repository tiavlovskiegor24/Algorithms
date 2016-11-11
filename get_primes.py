import math
def is_prime(number):
    
    if number > 1:
        
        if number == 2:
            return True
        
        if number % 2 == 0:
            return False
        
        for current in range(3,int(math.sqrt(number)+1),2):
            if number % current == 0:
                return False
        return True
    return False
    
def get_primes(number):
    while True:
        if is_prime(number):
            number = yield number
        number += 1
        
def solve_euler_10():
    total = 2
    for next_prime in get_primes(3):
        if next_prime < 2000000:
            total += next_prime
        else:
            print total
            return total
            

def print_succesive_primes(iterations,base = 10):
    
    prime_generator = get_primes(base)
    print prime_generator.send(None)
    
    for power in range(iterations):
        print prime_generator.send(base**power)
        
        
        
        
            
g = get_primes(3)
#solve_euler_10()

print_succesive_primes(10)