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
        check_credentials(connectionSocket, addr, clientList)
        message_exchange(connectionSocket, addr, clientList)
        # connectionSocket.shutdown(SHUT_RDWR)
        connectionSocket.close()


def check_credentials(connectionSocket, addr, clientList):
    curr_clients_username = connectionSocket.recv(16384).decode()
    curr_client = mainModule.Client(curr_clients_username, addr[0])
    # print("Just connected: " + curr_clients_username + ", " + str(addr[0]))

    #   Check if they are already in the client list. If not, add them to it.
    if not client_exists_in_client_list(clientList, curr_client):
        clientList.append(curr_client)
        print(curr_clients_username + " added to client list")


def message_exchange(connectionSocket, addr, clientList):
    sentence = connectionSocket.recv(16384).decode()
    if not sentence == "":
        #   Capitalize the sentence
        capitalizedSentence = sentence.upper()
        #   Send the capitalized sentence back to the client
        connectionSocket.send(capitalizedSentence.encode())
        #   Print an indication that all went well
        print("Sent uppercase version of \"" + sentence + "\" to client")
    else:
        connectionSocket.send("Cannot Capitalize empty string".encode())
        print("Sent warning upon receiving empty string")


def client_exists_in_client_list(clientList, client) -> bool:
    #   Bug to fix: that person with same username joins, but diff port+IP
    #   In which case we need to remove the same user from the list to not have duplicates
    for i in clientList:
        if mainModule.clients_equal(i, client):
            return True
    return False





def callmain():
    main()

if __name__ == "__main__":
    callmain()