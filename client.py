import socket
from socket import *
import mainModule
import sys
from threading import Thread

###### If client receives a message while it is being prompted in the console, must save the prompt, output message, and reprompt #######
previous_message = ""

def main():
    #   Configure the server PORT and IP variables
    serverIP = '127.0.0.1'  # since running on same computer
    serverPort = 12000

    #   Get the username and port # for this client
    userName = input('What is your userName: ')
    clientIP = get_local_ip_address()
    clientPort = int(input("What is the clientPort #: "))


    #   Make a thread for incoming connections from the server
    #   when the server is sending a message from another client
    client_receiver_thread = Thread(target=thread_receives_from_server, args=(clientIP, clientPort))
    client_receiver_thread.daemon = True
    client_receiver_thread.start()

    register_with_server(serverIP, serverPort, userName, clientPort)

    #   Sending messages for server to forward
    while True:
        #   Before making new connection, ask user if they want to send money?
        previous_message = "Do you want to send message: "
        if not input("Do you want to send message: ").lower() == "yes":
            return
        client_to_server_socket = socket(AF_INET, SOCK_STREAM)
        previous_message = "Waiting for connection to server..."
        print("Waiting for connection to server...")
        client_to_server_socket.connect((serverIP, serverPort))
        send_credentials(client_to_server_socket, userName, clientPort)
        # send_target_credentials(client_to_server_socket)
        message_exchange(client_to_server_socket, userName)
        # client_to_server_socket.shutdown(SHUT_RDWR)
        client_to_server_socket.close()


def thread_receives_from_server(clientIP, clientPort):
    #  Creating the client's socket object
    client_listening_Socket = socket(AF_INET, SOCK_STREAM)
    # serverIP = get_local_ip_address()
    client_listening_Socket.bind((clientIP, clientPort))
    client_listening_Socket.listen(20)
    # print("The server is ready to receive")

    while True:
        #   Create the socket with which we will listen for messages from server, that are being forwarded
        server_to_client_Socket, addr = client_listening_Socket.accept()
        #   First receive the username of the origin client
        origin_client_username = server_to_client_Socket.recv(16384).decode()
        #   Send confirmation that received the username
        server_to_client_Socket.send("Client Received username".encode())
        #   Receive the Actual message
        message = server_to_client_Socket.recv(16384).decode()
        #   Send confirmation that received the message
        server_to_client_Socket.send("Client Received message".encode())
        if not message == "":
            print("\n\nMessage received from " + origin_client_username + ": " + message)
            print(previous_message)

        try:
            server_to_client_Socket.shutdown(SHUT_RDWR)
        except error as e:
            # print(f"Error shutting down socket: {e}")
            pass
        server_to_client_Socket.close()


def send_credentials(clients_connection_Socket, userName, clientPort):
    #   Send real Port number (as opposed to what addr[1] holds)
    clients_connection_Socket.send(str(clientPort).encode())
    #   Getting confirmation that server got Port Number
    clients_connection_Socket.recv(16384).decode()
    #   Sending Username
    clients_connection_Socket.send(userName.encode())
    #   Getting confirmation that server got Username
    clients_connection_Socket.recv(16384).decode()
    # print("Connected, and credentials sent...")


def message_exchange(socket_object, userName):
    #   Send the target username
    previous_message = 'To whom do you wish to send: '
    target_userName = input('To whom do you wish to send: ')
    socket_object.send(target_userName.encode())

    #   Get confirmation that server received target username
    target_confirmation = socket_object.recv(16384).decode()
    if target_confirmation == "This user doesn't exist!":
        previous_message = target_confirmation
        print(target_confirmation)
        return

    #   Send origin username
    socket_object.send(userName.encode())
    #   Get confirmation that server received origin username
    socket_object.recv(16384).decode()

    #   Input message to send to target, and send to server
    previous_message = 'Input message to send to ' + target_userName + " : "
    message = input('Input message to send to ' + target_userName + " : ")
    if message == "quit":
        socket_object.shutdown(SHUT_RDWR)  # will send empty string to the server
        socket_object.close()
        return
    socket_object.send(message.encode())

    #   Get confirmation that the message was received by the server, which will attempt to forward it
    socket_object.recv(16384).decode()

    # modifiedSentence = socket_object.recv(16384)
    # print('From Server: ', modifiedSentence.decode())


def register_with_server(serverIP, serverPort, userName, clientPort):
    client_to_server_socket = socket(AF_INET, SOCK_STREAM)
    print("Registering with server...")
    client_to_server_socket.connect((serverIP, serverPort))
    send_credentials(client_to_server_socket, userName, clientPort)
    client_to_server_socket.send("".encode())
    client_to_server_socket.close()


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
