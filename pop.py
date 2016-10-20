from time import time
from collections import deque

list1 = range(10000000)
list2 = deque(range(10000000))

t1 = time()
while list1:
    list1.pop()
print time() - t1

t2 = time() 
while list2:
    list2.popleft()
print time() - t2