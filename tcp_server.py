import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

# Create a new socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Pass in the IP address and port we want the server to listen on.
# bind() associates the socket with the server address.
# The address is localhost.
server.bind((bind_ip, bind_port))

# Tell the server to start listening with a maximum backlog of connections set to 5.
# Backlog specifies the number of pending connections the queue will hold.
# When multiple clients connect to the server, the server then holds the incoming requests in a queue.
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# Client handling thread.
# Performs the recv() and then sends a simple message back to the client.
def handle_client(client_socket):
    
    # Receive data from the socket. Maximum size of data is buffsize which here is 1024.
    request = client_socket.recv(1024)
    
    print "[*] Received: %s" % request
    
    # Send back a packet.
    client_socket.send("ACK!")
    
    client_socket.close()
    
# Waiting for an incoming connection.
while True:
    
    # When the client connects we receive the client socket into the client variable.
    # We also receive the remote connection details into the addr variable.
    client,addr = server.accept()
    
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
    
    # Spin up our client thread to handle incoming data.
    # We create a new thread object that points to our handle_client function and pass
    # it the client socket object as an argument.
    client_handler = threading.Thread(target=handle_client, args=(client,))
    
    # Start the thread to handle the client connection (our main server loop is ready to handle another incoming connection).
    client_handler.start()    
