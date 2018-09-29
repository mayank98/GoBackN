from threading import *
from frame import *

def print_func():
    print("name\n")

t=Thread(target=print_func)

t.start()

print(ackframe(2,2).__class__.__name__)
print(dataframe(2,2,2).__class__.__name__)