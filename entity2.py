from socket import *
from frame import *
from threading import *
import time
import pickle
import random
import string
from network import transmit

HOST = gethostbyname(gethostname())  # The receiver's hostname or IP address
PORT = 9998        # The port used by the receiver
address=(HOST,PORT)
mySocket=socket(AF_INET,SOCK_DGRAM)
mySocket.bind(address)
mySocket.settimeout(3)

otherSocket=socket(AF_INET, SOCK_DGRAM)
ADDRESS=(HOST,9999)
otherSocket.settimeout(0.01)


t0=time.time()
sentPackets=0
newPackets=0
resentPackets=0
newRecieved=0
totalRecieved=0
lock=Lock()

#Generate random words of given length
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

#Generate packets of given size
def generatePacket(index, size=0):
	length=(size-256)/8
	data=randomword(length)
	d=dataframe(size,index,data)
	return d

#This is our client function
#It generates and sends packet over the network and recieves acknowledgement for the packets sent
def sender():
	base=0
	window=7							# Window size
	sendNext=0							# Packet index to be sent nest
	timeout=1							# maximum waiting time before ack is recieved/packet resent
	lastackreceived= time.time()		# Time when the previous packets ack recieved for the first time
	packets=[]                          # window packets generated stored stored in this
	last_ack=-1							# Index of the previous ack recieved 
	
	global sentPackets, newPackets, resentPackets
	#SENDING PACKETS
	while True:
	    if(sendNext<base+window):
	        size=int(random.uniform(512,2048))
	        pkt=generatePacket(sendNext,size)
	        packets.append(pkt)
	        sendNext+=1
	        pickledpkt=pickle.dumps(pkt)
	        transmit(otherSocket,pickledpkt,ADDRESS)
	        with lock:
	        	sentPackets+=1
	        	newPackets+=1

	#RECEIPT OF AN ACK
	    try:
	        pickledack,sss = otherSocket.recvfrom(1024)
	        ack = pickle.loads(pickledack)

	        #Check the object being received is of type ackframe
	        if ack.__class__.__name__=="ackframe":
		        last_ack=ack.index
		        # slide window and reset timer
		        while ack.index>=base and packets:
		            lastackreceived = time.time()
		            for i in range(ack.index-base+1):
		                del packets[0]
		            base = ack.index + 1
	      #   else:
		    	# print "packet in ack ",ack.index

	#TIMEOUT
	    except:
	        #Resend the packets that were in the window
	        if(time.time()-lastackreceived>timeout):
	            for i in packets:
	                transmit(otherSocket,pickle.dumps(i),ADDRESS)
	                with lock:
		                sentPackets+=1
		                resentPackets+=1

#This is our server function
#It recieves packet over the network and sends acknowledgement for the packets recieved
def receiver():
	global newRecieved, totalRecieved
	expected_ack_idx=0

	last_pkt_received_time = time.time()
	start_time = time.time()

	while True:
	    try:
	        packet_raw,sender_address=mySocket.recvfrom(4096)
	        with lock:
	        	totalRecieved+=1
	        packet=pickle.loads(packet_raw)

	        #Check the object being received is of type dataframe
	        if packet.__class__.__name__=="dataframe":

	        	# Send the next ack if packet recieved in-order
		        if(packet.index==expected_ack_idx):
		            with lock:
		            	newRecieved+=1

		            send_packet=ackframe(256,expected_ack_idx)
		            expected_ack_idx += 1
		            transmit(mySocket,pickle.dumps(send_packet),sender_address)

		        # Send the previous ack
		        else:
		            send_packet=ackframe(256,expected_ack_idx-1)
		            transmit(mySocket,pickle.dumps(send_packet),sender_address)
	    except:
	    	#Nothing recieved
	    	x=0

def summary():
    global sentPackets, newPackets, resentPackets, newRecieved, totalRecieved, t0
	#Summary of previous 2 seconds
    while True:
	    # print "summary"
	    if time.time()-t0>2:
	    	with lock:
		    	print ""
		    	print "A brief summary of previous 2 seconds"
		    	print "Total number of packets sent: ", sentPackets
		    	print "Number of new packets generated: ", newPackets
		    	print "Number of packets resent: ", resentPackets
		    	print "Total number of packets recieved: ", totalRecieved
		    	print "Number of packets recieved in order: ", newRecieved
		    	print "##############################################"
		    	t0=time.time()
		    	sentPackets=0
		    	newPackets=0
		    	resentPackets=0
		    	newRecieved=0
		    	totalRecieved=0


if __name__=="__main__":

	t0=time.time()
	ts=Thread(target=sender)
	tr=Thread(target=receiver)
	su=Thread(target=summary)

	# start the 3 threads 
	ts.start()
	tr.start()
	su.start()