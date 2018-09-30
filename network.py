from socket import *
from random import *
from frame import *

drop_prob_dataframe = 0.1
drop_prob_ackframe = 0.05


def transmit(in_socket,message,address):
    
    drop_prob=0
    if (message.__class__.__name__=="ackframe"):
        drop_prob=drop_prob_ackframe
    else:
        drop_prob=drop_prob_dataframe

    # send ack/packet if the number generated greater than drop prob
    if (random() > drop_prob):
        in_socket.sendto(message,address)