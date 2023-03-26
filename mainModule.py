import threading



# class ThreadSafeList:
#     def __init__(self):
#         self._list = []
#         self._lock = threading.Lock()
#
#     def append(self, item):
#         with self._lock:
#             self._list.append(item)
#
#     def remove(self, item):
#         with self._lock:
#             self._list.remove(item)
#
#     def __getitem__(self, index):
#         with self._lock:
#             return self._list[index]
#
#     def __setitem__(self, index, value):
#         with self._lock:
#             self._list[index] = value
#
#     def __len__(self):
#         with self._lock:
#             return len(self._list)
#
#     def __str__(self):
#         with self._lock:
#             return str(self._list)
#
#     def __iter__(self):
#         return ThreadSafeListIterator(self)
#
#
# class ThreadSafeListIterator:
#     def __init__(self, thread_safe_list):
#         self._thread_safe_list = thread_safe_list
#         self._index = 0
#         self._lock = self._thread_safe_list._lock.__enter__()
#
#     def __next__(self):
#         try:
#             if self._index >= len(self._thread_safe_list):
#                 raise StopIteration
#             value = self._thread_safe_list[self._index]
#             self._index += 1
#             return value
#         except:
#             self._thread_safe_list._lock.__exit__(None, None, None)
#             raise
#
#     def __del__(self):
#         self._thread_safe_list._lock.__exit__(None, None, None)


def compare_clients_userName(client1, client2) -> bool:
    if client1.userName == client2.userName:
        return True
    else:
        return False


def compare_clients_clientIP(client1, client2) -> bool:
    if client1.clientIP == client2.clientIP:
        return True
    else:
        return False


def compare_clients_clientPort(client1, client2) -> bool:
    if client1.clientPort == client2.clientPort:
        return True
    else:
        return False

def clients_equal(client1, client2) -> bool:
    if client1.userName == client2.userName and client1.clientIP == client2.clientIP and client1.clientPort == client2.clientPort:
        return True
    else:
        return False

class Client:
    def __init__(self, clientUserName, clientIP, clientPort):
        self.userName = clientUserName
        self.clientIP = clientIP
        self.clientPort = clientPort
