import socket
from socket import *
import mainModule
import sys
from threading import Thread

''' If client receives a message while they are being prompted in the console, 
must save the prompt, output received message, and re-prompt. '''
current_prompt_to_console = ""


def main():
    global current_prompt_to_console
    #   Configure the server PORT and IP variables
    serverIP = '127.0.0.1'  # since running on same computer
    serverPort = 12000

    #   Get the username and port # for this client, from the user (for now)
    userName = input('What is your userName: ')
    #   clientIP (and server as well) should be 127.0.0.1 when running all on one device
    clientIP = '127.0.0.1'
    #   clientIP = get_local_ip_address()
    clientPort = int(input("What is the clientPort #: "))

    #   Make a thread for incoming connections from the server when the server is
    #       forwarding a message from another client
    #   Also kind of like staring "server" (in this case, this client) before the clients have access to it
    #       (in this case, server is the client)
    client_receiver_thread = Thread(target=thread_receives_messages_from_server, args=(clientIP, clientPort))
    client_receiver_thread.daemon = True
    client_receiver_thread.start()

    register_with_server(serverIP, serverPort, userName, clientPort)

    #   Sending messages to server, for server to forward
    while True:
        #   Before making new connection, ask user if they want to send money?
        current_prompt_to_console = "Do you want to send message: "
        if not input("Do you want to send message: ").lower() == "yes":
            return
        #   Make a socket for the client to connect to server to send money to others
        client_to_server_socket = socket(AF_INET, SOCK_STREAM)
        current_prompt_to_console = "Waiting for connection to server..."
        print("Waiting for connection to server...")
        #   Use new socket to connect to the server
        client_to_server_socket.connect((serverIP, serverPort))
        #   Send this client's credentials
        send_credentials(client_to_server_socket, userName, clientPort)
        #   After sending credentials, send the message
        message_exchange(client_to_server_socket, userName)
        #   Try to shut down the connection before closing it
        try:
            client_to_server_socket.shutdown(SHUT_RDWR)
        except error as e:
            #   print(f"Error shutting down socket: {e}")
            pass
        client_to_server_socket.close()


def thread_receives_messages_from_server(clientIP, clientPort):
    #   Create the client's socket object, that will listen for connection requests from server (initial handshake)
    client_listening_Socket = socket(AF_INET, SOCK_STREAM)
    client_listening_Socket.bind((clientIP, clientPort))
    client_listening_Socket.listen(20)

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
            print("\n" + current_prompt_to_console)

        try:
            server_to_client_Socket.shutdown(SHUT_RDWR)
        except error as e:
            #   print(f"Error shutting down socket: {e}")
            pass
        server_to_client_Socket.close()


#   This function will register this client with the server, so the server becomes aware of it and can forward messages to it
def register_with_server(serverIP, serverPort, userName, clientPort):
    #   Make a socket that we will use to send this client's credentials to the server
    client_to_server_socket = socket(AF_INET, SOCK_STREAM)
    print("Registering with server...")
    client_to_server_socket.connect((serverIP, serverPort))
    #   Call the send_credentials function, that takes care of sending all necessary info to server
    send_credentials(client_to_server_socket, userName, clientPort)
    #   Sending an empty "target_username" to the "message_forwarding" function in the server, since only registering now.
    client_to_server_socket.send("".encode())
    #   Get confirmation that server received empty message meant as ending to registration process

    client_to_server_socket.close()


#   This function corresponds to the "get_client_credentials function in the server"
def send_credentials(clients_connection_Socket, userName, clientPort):
    #   Get message from server saying that it's ready to receive credentials
    clients_connection_Socket.recv(16384).decode()
    #   Send real Port number (as opposed to what addr[1] holds)
    clients_connection_Socket.send(str(clientPort).encode())
    #   Getting confirmation that server got Port Number
    clients_connection_Socket.recv(16384).decode()
    #   Sending Username
    clients_connection_Socket.send(userName.encode())
    #   Getting confirmation that server got Username
    clients_connection_Socket.recv(16384).decode()
    #   print("Connected, and credentials sent...")


def message_exchange(client_to_server_socket, userName):
    global current_prompt_to_console

    ###   Sending the target username:

    current_prompt_to_console = 'To whom do you wish to send: '
    #   Ask user who they wish to send to
    target_userName = input('To whom do you wish to send: ')

    #   Send target username
    client_to_server_socket.send(target_userName.encode())

    #   Get confirmation that server received target username
    target_confirmation = client_to_server_socket.recv(16384).decode()
    if target_confirmation == "This user doesn't exist!":
        current_prompt_to_console = target_confirmation
        print("\n" + target_confirmation)
        return

    #   Send origin username
    client_to_server_socket.send(userName.encode())
    #   Get confirmation that server received origin username
    client_to_server_socket.recv(16384).decode()

    #   Input message to send to target, and send to server
    current_prompt_to_console = 'Input message to send to ' + target_userName + " : "
    message = input('Input message to send to ' + target_userName + " : ")
    if message == "quit":
        client_to_server_socket.shutdown(SHUT_RDWR)  # will send empty string to the server
        client_to_server_socket.close()
        return
    client_to_server_socket.send(message.encode())

    #   Get confirmation that the message was received by the server, which will attempt to forward it
    client_to_server_socket.recv(16384).decode()

    #   modifiedSentence = client_to_server_socket.recv(16384)
    #   print('From Server: ', modifiedSentence.decode())


def get_local_ip_address():
    try:
        #   Create a temporary socket and connect to a dummy IP address
        with socket(AF_INET, SOCK_DGRAM) as temp_socket:
            temp_socket.connect(("10.255.255.255", 1))
            local_ip_address = temp_socket.getsockname()[0]
    except Exception:
        #   Fallback to loopback address if the method above fails
        local_ip_address = "127.0.0.1"
    return local_ip_address


def callmain():
    main()


if __name__ == "__main__":
    callmain()
