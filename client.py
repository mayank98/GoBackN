from socket import *
from frame import *
import time
import pickle
import random

HOST = gethostbyname(gethostname())  # The server's hostname or IP address
PORT = 9999        # The port used by the server

# HOST = gethostbyname("www.google.com")  # The server's hostname or IP address
# PORT = 80

#create client socket
clientSocket=socket(AF_INET, SOCK_DGRAM)
ADDRESS=(HOST,PORT)
# clientSocket.connect(ADDRESS)

# clientSocket=socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((HOST,PORT))
# clientSocket=create_connection((HOST, PORT))
clientSocket.settimeout(0.01)


base=0
window=7
sendNext=0
timeout=1
lastackreceived= time.time()
packets=[]                          #window packets generated stored stored in this

last_ack=-1
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
        size=int(random.uniform(512,2048))
        pkt=generatePacket(sendNext,size)
        packets.append(pkt)
        sendNext+=1
        pickledpkt=pickle.dumps(pkt)
        print "sending packet"
        # clientSocket.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        clientSocket.sendto(pickledpkt,ADDRESS)
        # print clientSocket.recv(1024)
        print "yes"

#RECEIPT OF AN ACK
    try:
        pickledack,sss = clientSocket.recvfrom(1024)
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
                clientSocket.sendto(pickle.dumps(i),ADDRESS)



# d1=dataframe(100,0,"Hello")
# print(d1.data)
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)

# print('Received', repr(data))