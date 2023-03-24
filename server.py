from socket import *
from socket import socket, AF_INET, SOCK_STREAM


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

if __name__ == "__main__":
    serverPort = 12000
    serverIP = "127.0.0.1"

    #  Creating the socket object that will maintain a TCP connection
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # serverIP = get_local_ip_address()
    serverSocket.bind((serverIP, serverPort))

    #  Now the socket listens for a connection request
    serverSocket.listen(2)
    print('The server is ready to receive')

    while True:
        # when connection request is received:
        connectionSocket, addr = serverSocket.accept()
        # Receive and store the message being passed by the client
        sentence = connectionSocket.recv(1024).decode()
        # Capitalize the sentence
        capitalizedSentence = sentence.upper()
        # Send the capitalized sentence back to the client
        connectionSocket.send(capitalizedSentence.encode())
        # Print an indication that all went well
        print("Sent uppercase version of \"" + sentence +  "\" to client")
        connectionSocket.close()
