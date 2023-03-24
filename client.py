import socket
from socket import *

# TCP Client code from textbook

serverName = '127.0.0.1'

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    sentence = input('Input lowercase sentence (type quit to exit):')
    if sentence == "quit":
        break
    clientSocket.send(sentence.encode()) 
    modifiedSentence = clientSocket.recv(16384) 
    print('From Server: ', modifiedSentence.decode())

clientSocket.close()