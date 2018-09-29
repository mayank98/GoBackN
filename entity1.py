from socket import *
from frame import *
from threading import *
import time
import pickle
import random

HOST = gethostbyname(gethostname())  # The receiver's hostname or IP address
PORT = 9999        # The port used by the receiver
address=(HOST,PORT)
mySocket=socket(AF_INET,SOCK_DGRAM)
mySocket.bind(address)
mySocket.settimeout(3)

otherSocket=socket(AF_INET, SOCK_DGRAM)
ADDRESS=(HOST,9998)
otherSocket.settimeout(0.01)


def generatePacket(index, size=0):
    data="Hello"
    d=dataframe(size,index,data)
    return d

#This is our client function
def sender():
	base=0
	window=7
	sendNext=0
	timeout=1
	lastackreceived= time.time()
	packets=[]                          #window packets generated stored stored in this

	last_ack=-1
	

	while True:
	    if(sendNext<base+window):
	        size=int(random.uniform(512,2048))
	        pkt=generatePacket(sendNext,size)
	        packets.append(pkt)
	        sendNext+=1
	        pickledpkt=pickle.dumps(pkt)
	        print "sending packet"
	        # otherSocket.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
	        otherSocket.sendto(pickledpkt,ADDRESS)
	        # print otherSocket.recv(1024)
	        print "yes"

	#RECEIPT OF AN ACK
	    try:
	        pickledack,sss = otherSocket.recvfrom(1024)
	        # ack = []
	        ack = pickle.loads(pickledack)
	        print "Received ack for", ack.index
	        #           slide window and reset timer
	        last_ack=ack.index

	        while ack.index>=base and packets:
	            lastackreceived = time.time()
	            for i in range(ack.index-base+1):
	                del packets[0]
	            base = ack.index + 1

	#TIMEOUT
	    except:
	        print last_ack," in except"
	        if(time.time()-lastackreceived>timeout):
	            for i in packets:
	                print "resend"
	                otherSocket.sendto(pickle.dumps(i),ADDRESS)

def receiver():
	expected_ack_idx=0

	last_pkt_received_time = time.time()
	start_time = time.time()

	while True:
	    try:
	        # packet_raw,sender_address=mySocket.recvfrom(2024)
	        print("mauank");
	        packet_raw,sender_address=mySocket.recvfrom(4096)
	        print("mauank2",sender_address);
	        
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
	            # BadNet.transmit(mySocket, pickle.dumps(sndpkt), senderAddress[0], senderAddress[1])
	            mySocket.sendto(pickle.dumps(send_packet),sender_address)
	            print "New Ack", expected_ack_idx

	        else:
	#       default? discard packet and resend ACK for most recently received inorder pkt
	            print "Received out of order", packet.index
	            # sndpkt = []
	            # sndpkt.append(expected_ack_idx)
	            # h = hashlib.md5()
	            # h.update(pickle.dumps(sndpkt))
	            # sndpkt.append(h.digest())
	            send_packet=ackframe(256,expected_ack_idx-1)
	            mySocket.sendto(pickle.dumps(send_packet),sender_address)
	            # BadNet.transmit(mySocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
	            print "Ack", expected_ack_idx
	    except:
	        print("adfasdf")

if __name__=="__main__":
	ts=Thread(target=sender)
	tr=Thread(target=receiver)

	ts.start()
	tr.start()


