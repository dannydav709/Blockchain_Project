import socket
from socket import *

def get_local_ip_address():
    try:
        # Create a temporary socket and connect to a dummy IP address
        with socket(AF_INET, SOCK_DGRAM) as temp_socket:
            temp_socket.connect(("10.255.255.255", 1))
            local_ip_address = temp_socket.getsockname()[0]
    except Exception:
        # Fallback to loopback address if the method above fails
        local_ip_address = "127.0.0.1"
    return local_ip_address


# TCP Client code from textbook

serverName = get_local_ip_address()
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

while True:
    sentence = input('Input lowercase sentence (type quit to exit):')
    if sentence == "quit":
        break
    clientSocket.send(sentence.encode()) 
    modifiedSentence = clientSocket.recv(16384) 
    print('From Server: ', modifiedSentence.decode())

clientSocket.close()