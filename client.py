import socket
from socket import *
import mainModule
import sys


def main():
    #   Configure the client PORT and IP variables
    serverIP = '127.0.0.1'  # since running on same computer
    serverPort = 12000

    #   Get the username and port # for this client
    userName = input('What is your userName: ')
    clientIP = serverIP
    clientPort = int(input("What is the clientPort #: "))


    #   Sending messages
    while True:
        #   Before making new connection, ask user if they want to send money?
        if not input("Do you want to send crypto: ").lower() == "yes":
            return
        clients_connection_Socket = socket(AF_INET, SOCK_STREAM)
        print("Waiting for connection to server...")
        clients_connection_Socket.connect((serverIP, serverPort))
        send_credentials(clients_connection_Socket, userName, serverIP, serverPort)
        message_exchange(clients_connection_Socket)
        # clients_connection_Socket.shutdown(SHUT_RDWR)
        clients_connection_Socket.close()


def send_credentials(clients_connection_Socket, userName, serverIP, serverPort):
    clients_connection_Socket.send(userName.encode())
    clients_connection_Socket.recv(16384).decode()
    print("Connected, and credentials sent...")


def message_exchange(clients_connection_Socket):
    sentence = input('Input lowercase sentence (type quit to exit): ')
    if sentence == "quit":
        clients_connection_Socket.shutdown(SHUT_RDWR)
        clients_connection_Socket.close()
        sys.exit()
    clients_connection_Socket.send(sentence.encode())
    modifiedSentence = clients_connection_Socket.recv(16384)
    print('From Server: ', modifiedSentence.decode())



def callmain():
    main()
if __name__ == "__main__":
    callmain()
