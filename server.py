from socket import *
from frame import *
# from BadNet5 import *
import pickle
# import hashlib
import sys
import os
import math
import time

HOST=gethostbyname(gethostname())
PORT=9999

address=(HOST,PORT)
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(address)
serverSocket.settimeout(3)
# serverSocket.listen(1)
print "Ready to serve"

expected_ack_idx=0
current_ack_idx=0

last_pkt_received_time = time.time()
start_time = time.time()

while True:
    try:
        # packet_raw,client_address=serverSocket.recvfrom(2024)
        print("mauank");
        packet_raw,sss=serverSocket.recvfrom(4096)
        print("mauank2");
        
        packet=pickle.loads(packet_raw)

        if(packet.index==expected_ack_idx):
            print "Received inorder", expected_ack_idx
            # if rcvpkt[1]:
            #     f.write(rcvpkt[1])
            # else:
            #     endoffile = True
#               create ACK (seqnum,checksum)
            # sndpkt = []
            # sndpkt.append(expected_ack_idx)
            
            send_packet=ackframe(256,expected_ack_idx)
            expected_ack_idx += 1
            # h = hashlib.md5()
            # h.update(pickle.dumps(sndpkt))
            # sndpkt.append(h.digest())
            # BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
            serverSocket.sendto(pickle.dumps(send_packet),address)
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
            serverSocket.sendto(pickle.dumps(send_packet),address)
            # BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
            print "Ack", expected_ack_idx
    except:
        print("adfasdf")