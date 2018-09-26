from socket import *
from frame import *
# from BadNet5 import *
import pickle
# import hashlib
import sys
import os
import math
import time

HOST='127.0.0.1'
PORT=9999

address=(HOST,PORT)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(address)
serverSocket.settimeout(3)
print "Ready to serve"

expected_ack_idx=1
current_ack_idx=1

last_pkt_received_time = time.time()
start_time = time.time()

while True:
    try:
        # packet_raw,client_address=serverSocket.recvfrom(2024)
        packet_raw=serverSocket.recv(2024)
        packet=pickle.loads(packet_raw)

        if(packet.index==expected_ack_idx):
            print "Received inorder", expected_ack_idx
            # if rcvpkt[1]:
            #     f.write(rcvpkt[1])
            # else:
            #     endoffile = True
            expected_ack_idx += 1
#               create ACK (seqnum,checksum)
            # sndpkt = []
            # sndpkt.append(expected_ack_idx)
            
            send_packet=ackframe(256,expected_ack_idx)
            # h = hashlib.md5()
            # h.update(pickle.dumps(sndpkt))
            # sndpkt.append(h.digest())
            # BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
            serverSocket.send(pickle.dumps(send_packet))
            print "New Ack", expected_ack_idx

        else:
#       default? discard packet and resend ACK for most recently received inorder pkt
            print "Received out of order", packet.index
            # sndpkt = []
            # sndpkt.append(expected_ack_idx)
            # h = hashlib.md5()
            # h.update(pickle.dumps(sndpkt))
            # sndpkt.append(h.digest())
            send_packet=ackframe(256,expected_ack_idx)
            serverSocket.send(pickle.dumps(send_packet))
            # BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
            print "Ack", expected_ack_idx
    except:
        print("adfasdf")