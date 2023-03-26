import socket
from socket import *
import mainModule


def main():
    #  Configure the client PORT and IP variables
    serverIP = '127.0.0.1'  # since running on same computer
    serverPort = 12000

    #  Get the username and port # for this client
    userName = input('What is your userName: ')
    clientIP = serverIP
    clientPort = int(input("What is the clientPort #: "))

    #  Creating the server's socket object
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.bind((clientIP, clientPort))
    make_initial_connection_to_server(clientSocket, userName, serverIP, serverPort)


    # while True:
    #     sentence = input('Input lowercase sentence (type quit to exit):')
    #     if sentence == "quit":
    #         break
    #     clientSocket.send(sentence.encode())
    #     modifiedSentence = clientSocket.recv(16384)
    #     print('From Server: ', modifiedSentence.decode())
    #     clientSocket.close()

def make_initial_connection_to_server(clientSocket, userName, serverIP, serverPort):
    """
    This function runs as soon as the client program runs, and it makes the initial connection
    to the server, where it sends the username, and the server then registers it, and as long as
    the server runs, it will remember the clients that have registered to it this way. But the
    client will send this to the server each time it starts, and the server will check its list
    to see if it already knows this client.
    """
    clientSocket.connect((serverIP, serverPort))
    print("Successfully connected to server")

    #   Send server the username
    clientSocket.send(userName.encode())

    #   CHECKPOINT
    while True:
        pass


def callmain():
    main()
if __name__ == "__main__":
    callmain()
