import socket
import sys

if __name__ == '__main__':
    # Host IP address is my ip address
    HOST = socket.gethostbyname(socket.gethostname())

    # If the user has provided a port number, use it 
    # otherwise, use a default port number of 2048
    PORT = 2048
    
    if (len(sys.argv) > 1):
        try:
            PORT = int(sys.argv[1])
        except:
            print("Invalid Port Number!, using a default 2048")
            PORT = 2048

    
    # If the user has provided the output file name
    # use it, otherwise use 'output.txt' as the output file
    outfileName = 'output.txt'
    if (len(sys.argv) > 2):
        try:
            outfileName = sys.argv[2]
        except:
            print("Invalid output filename, using the default")


    #how many bytes to represent the length of message
    #as a string
    HEADER = 32

    # Server address tuple: ip and port
    ADDR =(HOST, PORT)

    # Specify a message that indicates the end of the stream from the
    # client side. If this message is received by the server, the server
    # closes the connection with this client 
    FIN_MESSAGE = "BYE!"

    # Create and IPv4 TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind it 
    s.bind(ADDR)

    # Wait for a client to connect
    s.listen(1) 

    print("Server is listening on %s:%d" % (HOST, PORT))

    # A counter to count how many messages were received by the server
    totalReceived = 0

    while True:
        # accept a connection from a client
        conn, addr = s.accept()
        print("Client %s:%s connected" % (addr[0], addr[1]))
        connected = True

        # Open a file for writing
        with open(outfileName, 'a') as f: 
            while connected :
                # The first thing to receive is the message length
                dataLen = conn.recv(HEADER)
                if dataLen :
                    dataLen = int(dataLen)

                    # Then receive the actual message
                    msg = conn.recv(dataLen)
		    print("[%s:%s] %s" %(addr[0], addr[1], msg))

                    # If the client sent a FIN message, close the
                    # client socket
                    if (msg == FIN_MESSAGE) :
                        connected = False 
                    else :
                    # Otherwise, increment the count of received messages
                        totalReceived += 1 
                    # Send an ACK to the client
                        conn.sendall(bytes("ACK[%d]"%totalReceived))
                    # And write the message to output.txt
                        f.write(msg)
                        f.write('\n')
            conn.close()


