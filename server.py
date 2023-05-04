from socket import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import threading
import queue
from mainModule import Transaction
import mainModule


#   This is used for when threads access the client list. Only one thread should be able to access the list at a time
resource_lock = threading.Lock()
clientList_resource_Lock = threading.Lock()
transaction_queue: list[Transaction] = []
mainBlockchain: mainModule.Blockchain = mainModule.Blockchain()



def main():
    global mainBlockchain

    #   Configure the server PORT and IP variables
    serverPort = 12000

    #   ServerIP is dynamic when not all clients are running on one device
    serverIP = get_local_ip_address()
    #   serverIP (and clients' as well) should be 127.0.0.1 when running all on one device
    # serverIP = '127.0.0.1'

    #   Maintain a list of users
    clientList = []  # contains list of Client objects

    #   Creating the server's socket object
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))

    #   Start listening for incoming connections from the clients
    serverSocket.listen(20)
    print("Server's IP address is: " + str(serverIP))
    print('The server is ready to receive')

    mainBlockchain.print_blockchain()

    #   Make a thread for incoming connections from the server
    #   when the server is sending a message from another client

    """
        In this while loop, we are waiting for incoming connection requests,
        which will be serviced by a thread to take care of the forwarding of the message
        to the appropriate target client.   
    """
    while True:

        """
            After a client connects to the server socket (the handshake), accept the connection "into" a new socket.
            ".accept()" returns a 2-tuple. 
            "addr" holds a 2-tuple (IP , port #) of the client.
        """
        connectionSocket, addr = serverSocket.accept()
        client_thread = Thread(target=handle_client, args=(connectionSocket, addr, clientList))
        client_thread.start()


''' Each thread that is meant to handle a client will execute this function. 
    Will check the clients credentials,then will forward message. '''
def handle_client(connectionSocket, addr, clientList):
    """ The thread checks if the client it's serving exists in the clientList,
    and then forwards its message to the target. """
    get_client_credentials(connectionSocket, addr, clientList)
    money_forwarding(connectionSocket, addr, clientList)


    #   Shutting down the socket after message forwarding succeeded.
    #   Try-except needed here since if the other side shut down the connection first, this would give an error.
    try:
        connectionSocket.shutdown(SHUT_RDWR)
    except error as e:
        # print(f"Error shutting down socket: {e}")
        pass
    connectionSocket.close()


#   This function get the current clients port number, then username,
#   and deals with registering the client into the clientList if needed
def get_client_credentials(connectionSocket, addr, clientList):
    #   Send message that ready to receive credentials
    connectionSocket.send("Ready to receive credentials".encode())
    #   Receiving Port Number from client
    curr_clients_port = connectionSocket.recv(16384).decode()
    #   Sending confirmation that received port number from client
    connectionSocket.send("Got port".encode())
    #   Receiving Username from client
    curr_clients_username = connectionSocket.recv(16384).decode()
    #   Sending confirmation that received username from client
    connectionSocket.send("Got username".encode())

    ####    Now will either send money for gift (if first time registry), or empty

    #   Create client object with info given (to later enter into list of all clients, or to check if already exists)
    curr_client = mainModule.Client(curr_clients_username, addr[0], curr_clients_port)

    #   If necessary, add client to clientList
    #   Check if they are already in the client list. If not, add them to it.
    with resource_lock:
        if not client_exists_in_client_list(clientList, curr_client):
            clientList.append(curr_client)
            print(curr_clients_username + " registered...")
            #   Send gift for registering with TCPcoin exchange
            TCPcoin_to_send = "{:.2f}".format(float(200))
            connectionSocket.send(TCPcoin_to_send.encode())
            mainBlockchain.create_block(Transaction("TCPcoin Exchange Server", curr_clients_username, TCPcoin_to_send))
            curr_client.coin = 200.0
            mainBlockchain.print_last_block()

        else:
            connectionSocket.send((str(get_client_object_in_clientList(clientList, curr_clients_username).coin)).encode())
            # connectionSocket.send("Already Registered before".encode())


def money_forwarding(connectionSocket, addr, clientList):
    global mainBlockchain

    #   Get target username from the origin client
    target_username = connectionSocket.recv(16384).decode()

    #   Check that the target exists, if not, will need to send message telling the client that they don't exist
    if target_username != "":
        target_client = get_client_object_in_clientList(clientList, target_username)
    else:
        connectionSocket.send("Got the empty message".encode())
        return

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

    #   Get the money from the client to send to the target
    money_to_forward = connectionSocket.recv(16384).decode()

    #   Send confirmation that received the money
    connectionSocket.send("Received money to send to target client".encode())

    if not money_to_forward == "":
        #   Create the socket that will be used to send the message to the target
        server_to_forward_Socket = socket(AF_INET, SOCK_STREAM)
        server_to_forward_Socket.connect((target_client.clientIP, int(target_client.clientPort)))
        #   Send the username of origin client, to the target client :
        server_to_forward_Socket.send(origin_userName.encode())
        #   Receive confirmation that the client got the username
        server_to_forward_Socket.recv(16384).decode()
        #   Send the money to the target client (from the origin client)
        server_to_forward_Socket.send(money_to_forward.encode())
        #   Receive confirmation that target client received money
        server_to_forward_Socket.recv(16384).decode()

        #   Decrement the balance within Client object of the origin client
        origin_client = get_client_object_in_clientList(clientList, origin_userName)
        origin_client.coin = origin_client.coin - float(money_to_forward)

        #   Increment the balance within Client object of the target client
        target_client.coin = target_client.coin + float(money_to_forward)


        #   Make the transaction and add to blockchain
        mainBlockchain.create_block(Transaction(origin_userName, target_username, money_to_forward))
        mainBlockchain.print_last_block()

        #   Print an indication that all went well
        print("Successfully forwarded message from: " + origin_userName + " to " + target_username)
    else:
        # connectionSocket.send("Cannot forward empty message".encode())
        # print("Sent warning upon receiving empty string")
        return


#   Must use resource lock pre-using this function (for now)!!!!!!!!!
#   Checks if client (object) exists in the clientList
def client_exists_in_client_list(clientList, client) -> bool:
    #   Bug to fix: that person with same username joins, but diff port+IP
    #   In which case we need to remove the same user from the list to not have duplicates

    #   Go through clientList. Return true or false.
    for i in clientList:
        if mainModule.clients_equal(i, client):
            return True
    return False


#   Checks if client (username) exists in the clientList
def check_username_exists_in_client_list(clientList, username) -> bool:
    with clientList_resource_Lock:
        for i in clientList:
            if i.userName == username:
                return True
        else:
            return False


#   Returns client object if client exists in the clientList
def get_client_object_in_clientList(clientList, target_username):
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