
import socket # for the sockets
import sys # for the command line arguments

# Method to call when the user has not provided the correct
# number of argument
def usage():
    print("Insufficient number of arguments")
    print("%s Usage:" % sys.argv[0])
    print("%s <server_ip> <server_port" % sys.argv[0])
    exit()

# Function to read a file and store it in a list
#	return: lines => list of strings, each string 
#			corresponds to a line of the file
def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def send(msg):
    # for each message, we send two messages:
    #       1- The length of the message (32 bytes string)
    #       2- The actual message (of the specified length)
    
    # all socket send and receive expect bytes, so encode it 
    message = msg

    # find the length of the message and convert it to a string
    messageLenStr = str(len(message))

    # if the string representing the length of the message is 
    # smaller than the specified header size (32 bytes), add 
    # padding of empty spaces as bytes
    messageLenStr += b' ' * (HEADER - len(messageLenStr))

    # send the string representing the message length
    s.send(messageLenStr)

    # send the actual message
    s.send(message)

    # wait for ACK
    reply = s.recv(32)

    # if we get a valid ACK , print it 
    if reply:
        print(reply)

if __name__ == '__main__':
    
    # Make sure that the user has provided the server IP and port number
    if (len(sys.argv) != 3):
        usage()

    # Parse command line arguments (server ip and port)
    HOST = socket.gethostbyname(sys.argv[1])
    PORT = int(sys.argv[2])

    # Specify the header size (the size of the length string in bytes)
    HEADER = 32

    # Specify a message that indicates the end of the stream, so that
    # when the server receives it, it closes this connection with this 
    # client
    FIN_MESSAGE = "BYE!"
    
    # Server address tuple: ip and port 
    SERVER = (HOST, PORT)

    # Read the input file 
    lines = readFile('input.txt')

    # create an IPv4 TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server using the socket
    s.connect(SERVER)

    # send each line in the file
    for line in lines:
        send(line)

    # at the end, send the FIN_MESSAGE
    send(FIN_MESSAGE)


