# import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()
# with conn:
#     print('Connected by', addr)
#     while True:
#         data = conn.recv(1024)
#         if not data:
#             break
#         conn.sendall(data)



import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()