from socket import *

# Daniels section
# ------------------------------------

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

from socket import socket, AF_INET, SOCK_STREAM

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Replace 'YOUR_LOCAL_IP' with your computer's local IP address
serverSocket.bind(('YOUR_LOCAL_IP', serverPort))

serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()




# Marwan