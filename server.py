from socket import *
from socket import socket, AF_INET, SOCK_STREAM
import threading
import queue

# # Using textbooks server application (very basic)
# serverPort = 12000
# serverSocket = socket(AF_INET,SOCK_STREAM)
# serverSocket.bind(('',serverPort))
# serverSocket.listen(1)
# print('The server is ready to receive')
# while True:
#     connectionSocket, addr = serverSocket.accept()
#     sentence = connectionSocket.recv(1024).decode()
#     capitalizedSentence = sentence.upper()
#     connectionSocket.send(capitalizedSentence.encode())
#     connectionSocket.close()


#  Setting the port number and IP address that the server will use for the TCP connection


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


def service_a_connection(connectionSocket):
    # Receive and store the message being passed by the client
    sentence = connectionSocket.recv(1024).decode()
    # Capitalize the sentence
    capitalizedSentence = sentence.upper()
    # Send the capitalized sentence back to the client
    connectionSocket.send(capitalizedSentence.encode())
    # Print an indication that all went well
    print("Sent uppercase version of \"" + sentence + "\" to client")
    connectionSocket.close()


if __name__ == "__main__":

    #  Configure the server PORT and IP variables
    serverPort = 12000
    serverIP = "127.0.0.1"

    #  Creating the server's socket object
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # serverIP = get_local_ip_address()
    serverSocket.bind((serverIP, serverPort))

    #  Start listening for incoming connections from the clients
    serverSocket.listen(20)
    print('The server is ready to receive')

    """
    In this while loop, we are waiting for incoming connection requests,
    which will be serviced by another function to take care of the sending of the message
    to the appropriate target client.   
    """
    while True:
        """
        After a client connects to the server socket, accept the connection.
        This is only a handshake though, so now we create another socket for
        the actual connection where messages are exchanged. .accept() returns a 2-tuple. 
        addr holds a 2-tuple as well.
        """
        connectionSocket, addr = serverSocket.accept()
        service_a_connection(connectionSocket)
