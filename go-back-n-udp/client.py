# import socket
# from frame import *

# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 12345        # The port used by the server

# d1=dataframe(100,0,"Hello")
# print(d1.data)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# s.connect((HOST, PORT))
# s.sendall(b'Hello, world')
# data = s.recv(1024)

# print('Received', repr(data))

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()