import threading
import random
import string
import hashlib
import time


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

def generate_random_id():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(20))


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
        #   Each client starts with 0, but is gifted 200 coins when joining the TCPcoin Exchange system
        self.coin = TCPcoin(0)

#################################################################
class TCPcoin:
    def __init__(self, amount):
        # self.id = generate_random_id() # removed since won't have individual coins
        self.symbol = "TCPC"
        self.amount = amount

#################################################################
#   A transaction will be in a block
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.id = generate_random_id()

#################################################################
class Blockchain:
    def __init__(self):
        self.chain = []
        #   Create the "genesis transaction"
        self.create_block('0')

    #   Will create a block that will also hold a transaction object
    def create_block(self, previous_hash, transaction=None):
        block = {'index': len(self.chain) + 1,
                 'timestamp': time.time(),
                 #  'proof': proof
                 'previous_hash': previous_hash,
                 'transaction': transaction
                 }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        #   Will be needed to get the previous_hash
        return self.chain[-1]

    # def proof_of_work(self, previous_proof):
    #     new_proof = 1
    #     check_proof = False
    #     while not check_proof:
    #         hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
    #         if hash_operation[:4] == '0000':
    #             check_proof = True
    #         else:
    #             new_proof += 1
    #     return new_proof

    def hash(self, block):
        encoded_block = str(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        return self.get_previous_block()['index'] + 1

    def mine_block(self):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)
        block = self.create_block(proof, previous_hash)
        return block
