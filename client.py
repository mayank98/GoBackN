from socket import *
from frame import *
import time
import pickle
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9999        # The port used by the server

#create client socket
clientSocket=socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(0.001)
clientSocket.connect((HOST, PORT))


base=0
window=7
sendNext=0
timeout=0.01
lastackrecieved= time.time()
packets=[]							#window packets generated stored stored in this

def generatePacket(index, size=0):
	data="Hello"
	d=dataframe(size,index,data)
	return d

def windowPacket(ind):
	if ind<len(packets):
		return packets[ind]
	else:
		return None

while True:
	if(sendNext<base+window):
		size=int(random.uniform(512,2024))
		pkt=generatePacket(sendNext,size)
		packets.append(pkt)
		sendNext+=1
		pickledpkt=pickle.dumps(pkt)
		clientSocket.send(pickledpkt)

#RECEIPT OF AN ACK
	try:
		pickledack= clientSocket.recv(256)
		ack = []
		ack = pickle.loads(pickledack)
		print "Received ack for", ack.index
		#           slide window and reset timer
		while ack.index>base and packets:
			lastackreceived = time.time()
			for i in range(ack.index-base+1):
				del window[i]
			base = ack.index + 1

#TIMEOUT
	except:
		if(time.time()-lastackreceived>timeout):
			for i in window:
				clientSocket.send(pickle.dumps(packets[i]))






# d1=dataframe(100,0,"Hello")
# print(d1.data)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))