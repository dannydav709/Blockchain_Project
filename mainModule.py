# def compare_clients_userName(client1, client2) -> bool:
#     if client1.userName == client2.userName:
#         return True
#     else:
#         return False
#
#
# def compare_clients_clientIP(client1, client2) -> bool:
#     if client1.clientIP == client2.clientIP:
#         return True
#     else:
#         return False
#
#
# def compare_clients_clientPort(client1, client2) -> bool:
#     if client1.clientPort == client2.clientPort:
#         return True
#     else:
#         return False

def clients_equal(client1, client2) -> bool:
    if client1.userName == client2.userName and client1.clientIP == client2.clientIP:
        return True
    else:
        return False

class Client:
    def __init__(self, clientUserName, clientIP):
        self.userName = clientUserName
        self.clientIP = clientIP
        # self.clientPort = clientPort

#          and client1.clientIP == client2.clientIP and client1.clientPort == client2.clientPort
