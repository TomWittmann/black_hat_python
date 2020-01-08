'''
TCP or transmission control protocol defines how to establish and maintain
a network conversation through which application programs can exchange data.

In TCP a connection is established and maintained until application programs
at each end have finished exchanging messages.

It provides error free data transmission, handles retransmission of dropped or garbled
packets as well as acknowledgement of all packets that have arrived.

It is part of the transport layer (layer 4).

Example: The HTTP program layer asks the TCP layer to set up the connection and send the file.
The TCP stack divides the file into data packets, numbers them and then forwards them individually
to the IP layer for delivery.

NOTE: Here we are assuming that our connection will always succeed. Also, we assume
the server is always expecting us to send data first (as opposed to servers that expect
to send data to you first and await your response). We also assume here that the server will
always send us data back in a timely fashion.

'''
import socket

target_host = 'localhost'
target_port = 9999

# Create a socket object.
# AF_INET says we are going to use a standard IPv4 address.
# SOCK_STREAM indicates this will be a TCP client.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client to the server.
client.connect((target_host, target_port))

# Send some data to the server.
client.send("I like soccer!")

# Receive some data from the server.
response = client.recv(4096)

print(response)