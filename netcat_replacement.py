'''
In servers without netcat installed it is useful to create a simple network client
and server that you can use to push files, or to have a listener that gives you command
line access.
'''

import sys
import socket
import getopt
import threading
import subprocess

# Define some global variables.
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command             - initialize a command shell"
    print "-u --upload=destination  - upon receivin connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    
    # Exit from python. 0 is considered successful termination.
    sys.exit(0)
    
def client_sender(buffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        # Connect to our target host.
        client.connect((target, port))    
    
        # Test if we have received input from stdin.
        if len(buffer):
            client.send(buffer)
        
        while True:
            
            # Wait for data back.
            recv_len = 1
            response = ""
            
            # If all is well, ship the data off to the remote target and receive data back
            # until there is no more data left to receive.
            while recv_len:
                
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                
                if recv_len < 4096:
                    break
                
            print response,
            
            # Wait for more input from the user and continue sending and receiving data
            # until the user kills the script.
            buffer = raw_input("")
            buffer += "/n"
            
            # Send it off.
            client.send(buffer)
            
    except:
        
        print "[*] Exception! Exiting."
        
        # Tear down the connection.
        client.close()
        
def server_loop():
    # Global keyword allows a user to modify a variable outside of the current scope.
    global target
    
    # If no target is defined, we listen on all interfaces.
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # Spin off a thread to handle our new client.
        client_thread = threading.Thread(target = client_handler, args = (client_socket,))
        client_thread.start()
        
def run_command():
    
    # Trim the newline.
    command = command.rstrip()
    
    # Run whatever command is passed in, running it on the local operating system and returning the output
    # from the command back to the client that is connected to us.
    # Subprocess library provides a powerful process-creation interface that gives you a number of ways
    # to start and interact with client programs.
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = True)
        
    except:
        output = "Failed to execute command.\r\n"
        
    # Send output back to the client.
    return output

# Function to do file uploads, command execution, and our shell.
def client_handler(client_socket):
    global upload
    global execute
    global command
    
    # Check for upload.
    if len(upload_destination):
        
        # Read in all of the bytes and write to our destination.
        file_buffer = ""
        
        # Keep reading data until none is available.
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
            
        # Now we take these bytes and try to write them out.
        try:
            # The wb flag ensures that we are writing the file with binary mode enabled which ensures that
            # uploading and writing a binary executable will be successful.
            file_descriptor = open(upload_destination, "wb")
            # Send the result back accross the network.
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            # Acknowledge that we wrote the file out.
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
            
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
            
    # Check for command execution.
    # Handle the command shell. It continues to execute commands as we send them in
    # and sends back the output.
    if len(execute):
        
        # Run the command.
        output = run_command(execute)
        
        client_socket.send(output)
        
    # Now we go into another loop if a command shell was requested:
    if command:
        
        while True:
            # Show a simple prompt.
            client_socket.send("<BHP:#> ")
            
            # Now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                
            # Send back the command output.
            response = run_command(cmd_buffer)
            
            # Send back the response.
            client_socket.send(response)
    
    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    # Len() returns the number of items in an object.
    # sys.argv is a list of arguments. argv[1:] does a list slice where you're checking 1 forward.
    # If sys.argv[1] was empty it would return 1 (false) and so not would make it true.
    # argv[1:] gets everything after the script name.
    if not len(sys.argv[1:]):
        usage()
        
    # Read the commandline options.
    # try except are how th handle exceptions.
    try:
        # getopt.getopt parses command line options and parameter list.
        opts, args = getopt.getopt(sys.argv[1:], "hel:t:p:cu",
        ["help", "listen", "execute", "target", "port", "command", "upload"])
    
    # getopt module is a parser for command line options.
    # getopt helps scripts to parse the command line arguments in sys.argv.
    # Exception is raised when an uncrecognized option is found in the argument list or when
    # an option requiring an argument is given none.
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled option"
        
    # Are we going to listen or just send data from stdin?
    # We are trying to mimic netcat to read data from stdin and send it accross the network.
    if not listen and len(target) and port > 0:
        
        # Read in the buffer from the commandline.
        # This will block, so send CTRL-D if not sending input
        # to stdin.
        buffer = sys.stdin.read()
        
        # Send data off.
        client_sender(buffer)
        
    # We are going to listen and potentially upload things, execute commands,
    # and drop a shell back depending on our command line options above.
    if listen:
        server_loop()
    
main()
                
    
    
