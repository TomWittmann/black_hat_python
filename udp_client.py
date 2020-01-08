'''
UDP is a connectionless protocol so there is no call to connect() beforehand.

UDP is a communication protocol across the internet used espeically for time-sensitive
transmissions such as video playbacks or DNS lookups. It speeds up communications by not recquiring
a handshake. 
'''

import socket

target_host = "127.0.0.1"
target_port = 80

# Create a socket object.
# AF_INET specifies ipv4 protocol.
# SOCK_DGRM specifies that the protocol is UDP.
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Send some data to the server. 
client.sendto("AAABBBCCC", (target_host, target_port))

# Receive some UDP data back from the server.
# It returns both  the data and the details of the remote host and port.
data, addr = client.recvfrom(4096)

print (data)