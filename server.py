from socket import *
from socket import socket, AF_INET, SOCK_STREAM
import threading
import queue
import mainModule


def main():

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

    #  Maintain a list of users
    clientList = []  # contains list of Client objects

    """
        In this while loop, we are waiting for incoming connection requests,
        which will be serviced by another function to take care of the sending of the message
        to the appropriate target client.   
    """
    while True:
        """
            After a client connects to the server socket, accept the connection.
            This is only a handshake though, so now we create another socket for
            the actual connection where messages are exchanged. ".accept()" returns a 2-tuple. 
            "addr" holds a 2-tuple as well.
        """
        connectionSocket, addr = serverSocket.accept()
        service_a_connection(connectionSocket, addr, clientList)


def service_a_connection(connectionSocket, addr, clientList):

    """
        Here, we first check if this user exists in the list of users,
        if not, we add them to it. If yes, we proceed.
    """

    #   Ask client program for the username (which it will have from when the client program started)
    #   This should be taken care of in the "make_initial_connection_to_server" function in the client program
    curr_clients_username = connectionSocket.recv(16384).decode()
    curr_client = mainModule.Client(curr_clients_username, addr[0], addr[1])

    #   Check if they are already in the client list. If not, add them to it.
    if not exists_in_client_list(clientList, curr_client):
        clientList.append(curr_client)
        print(curr_clients_username + " added to client list")

    #   Receive and store a message being passed by the client
    sentence = connectionSocket.recv(16384).decode()
    if not sentence == "":
        #   Capitalize the sentence
        capitalizedSentence = sentence.upper()
        #   Send the capitalized sentence back to the client
        connectionSocket.send(capitalizedSentence.encode())
        #   Print an indication that all went well
        print("Sent uppercase version of \"" + sentence + "\" to client")
    connectionSocket.close()


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


def exists_in_client_list(clientList, client) -> bool:
    for i in clientList:
        if client.userName == i.userName:
            return True
        else:
            return False


def main():

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

    #  Maintain a list of users
    clientList = []  # contains list of Client objects

    """
        In this while loop, we are waiting for incoming connection requests,
        which will be serviced by another function to take care of the sending of the message
        to the appropriate target client.   
    """
    while True:
        """
            After a client connects to the server socket, accept the connection.
            This is only a handshake though, so now we create another socket for
            the actual connection where messages are exchanged. ".accept()" returns a 2-tuple. 
            "addr" holds a 2-tuple as well.
        """
        connectionSocket, addr = serverSocket.accept()
        service_a_connection(connectionSocket, addr, clientList)


def callmain():
    main()
if __name__ == "__main__":
    callmain()
