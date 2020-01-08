import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print >>sys.stderr, 'Starting up on %s port %s' % server_address

socket.bind(server_address)

socket.listen(1)

while True:
    #Wait for a connection.
    print >>sys.stderr, 'Waiting for a connection'
    connection, client_address = socket.accept()
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