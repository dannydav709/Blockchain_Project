from socket import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import threading
import queue
import mainModule


resource_lock = threading.Lock()
clientList_resource_Lock = threading.Lock()


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

    #   Make a thread for incoming connections from the server
    #   when the server is sending a message from another client

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
        client_thread = Thread(target=handle_client, args=(connectionSocket, addr, clientList))
        client_thread.start()


def handle_client(connectionSocket, addr, clientList):
    check_credentials(connectionSocket, addr, clientList)
    message_forwarding(connectionSocket, addr, clientList)
    try:
        connectionSocket.shutdown(SHUT_RDWR)
    except error as e:
        # print(f"Error shutting down socket: {e}")
        pass
    connectionSocket.close()


def check_credentials(connectionSocket, addr, clientList):
    #   Receiving Port Number
    curr_clients_port = connectionSocket.recv(16384).decode()
    #   Sending confirmation that got credentials
    connectionSocket.send("Got port".encode())
    #   Receiving Username
    curr_clients_username = connectionSocket.recv(16384).decode()

    # print(curr_clients_username + " " + str(addr[0]) + " " + curr_clients_port + " connected")
    #   Sending confirmation that server got credentials
    connectionSocket.send("Got username".encode())

    #   Create client object with information give
    curr_client = mainModule.Client(curr_clients_username, addr[0], curr_clients_port)

    #   If necessary, add client to clientList
    #   Check if they are already in the client list. If not, add them to it.
    with resource_lock:
        if not client_exists_in_client_list(clientList, curr_client):
            clientList.append(curr_client)
            print(curr_clients_username + " added to client list")


def message_forwarding(connectionSocket, addr, clientList):
    #   Get target username from the origin client
    target_username = connectionSocket.recv(16384).decode()
    #   Check that the target exists, if not, will need to send message telling the client that they don't
    target_client = find_in_clientList(clientList, target_username)
    if target_client is None:
        try:
            connectionSocket.send("This user doesn't exist!".encode())
        except ConnectionError:
            pass
        return

    #   Send confirmation that received the target username
    connectionSocket.send("Received target username...".encode())

    #   Get origin userName
    origin_userName = connectionSocket.recv(16384).decode()
    #   Send confirmation that received the origin username
    connectionSocket.send("Received origin username...".encode())

    #   Get the message from the client to send to the target
    message_to_forward = connectionSocket.recv(16384).decode()
    #   Send confirmation that received the message
    connectionSocket.send("Received Message to send to target client".encode())

    if not message_to_forward == "":
        #   Create the socket that will be used to send the message to the target
        server_to_forward_Socket = socket(AF_INET, SOCK_STREAM)
        server_to_forward_Socket.connect((target_client.clientIP, int(target_client.clientPort)))
        #   Send the username of client that is sending the message:
        server_to_forward_Socket.send(origin_userName.encode())
        #   Receive confirmation that the client got the username
        server_to_forward_Socket.recv(16384).decode()
        #   Send the Actual message
        server_to_forward_Socket.send(message_to_forward.encode())
        #   Receive confirmation that client recieved message
        server_to_forward_Socket.recv(16384).decode()

        #   Print an indication that all went well
        print("Successfully forwarded message to: " + target_username)
    else:
        # connectionSocket.send("Cannot forward empty message".encode())
        # print("Sent warning upon receiving empty string")
        return


#   Must use resource lock pre-using this function
def client_exists_in_client_list(clientList, client) -> bool:
    #   Bug to fix: that person with same username joins, but diff port+IP
    #   In which case we need to remove the same user from the list to not have duplicates
    for i in clientList:
        if mainModule.clients_equal(i, client):
            return True
    return False


def check_username_exists_in_client_list(clientList, username) -> bool:

    for i in clientList:
        if i.userName == username:
            return True
    else:
        return False


def find_in_clientList(clientList, target_username):
    with clientList_resource_Lock:
        for i in clientList:
            if i.userName == target_username:
                return i
        else:
            return None


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



def callmain():
    main()
if __name__ == "__main__":
    callmain()