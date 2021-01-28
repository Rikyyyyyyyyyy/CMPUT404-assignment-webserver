import socket
import sys
from urllib import request

HOST, PORT = "localhost", 8080
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    socket.connect((HOST, PORT))
    #socket.sendall(data)
    url = data + "/do-not-implement-this-page-it-is-not-found"

    print(url)
    req = request.urlopen(url, None, 3)

    # Receive data from the server and shut down
    received = socket.recv(1024)
finally:
    socket.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))