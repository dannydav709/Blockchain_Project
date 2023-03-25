import socket
import threading
import time


def handle_client(conn1, conn2):
    # Create threads to handle incoming messages from each client
    client1_thread = threading.Thread(target = handle_client_messages, args = (conn1, conn2))
    client2_thread = threading.Thread(target = handle_client_messages, args = (conn2, conn1))

    # Start the threads
    client1_thread.start()
    client2_thread.start()

def handle_client_messages(conn1, conn2):
    # while True:
    #     # Receive data from the client
    #     data = conn1.recv(1024)
    #     if not data:
    #         break
    #
    #     # Forward the received data to the other client
    #     conn2.sendall(data)
    #
    # # Close the connection
    # conn1.close()
    time.sleep(2)
    print("Thread closing this function x")

def start_server():
    # # Create a TCP socket object
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    # # Bind the socket to a specific IP address and port number
    # server_address = ("localhost", 5000)
    # server_socket.bind(server_address)
    #
    # # Listen for incoming connections
    # server_socket.listen(2)
    # print("Server listening on {}:{}".format(*server_address))
    #
    # # Accept two client connections
    # conn1, addr1 = server_socket.accept()
    # print("Client 1 connected: {}".format(addr1))
    #
    # conn2, addr2 = server_socket.accept()
    # print("Client 2 connected: {}".format(addr2))

    # Start handling client messages
    conn1 = "hi"
    conn2 = "bye"
    handle_client(conn1, conn2)

if __name__ == "__main__":
    start_server()
    print ("main thread ends here\n")