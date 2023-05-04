import threading
import random
import string
import hashlib
import time


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


#################################################################
class Client:
    def __init__(self, clientUserName, clientIP, clientPort):
        self.userName = clientUserName
        self.clientIP = clientIP
        self.clientPort = clientPort
        #   Each client starts with 0, but is gifted 200 coins when joining the TCPcoin Exchange system
        self.coin: float = 0.0


#################################################################
class TCPcoin:
    def __init__(self, amount):
        # self.id = generate_random_id() # removed since won't have individual coins
        self.symbol = "TCPC"
        self.amount = amount


#################################################################
#   A transaction will be in a block
class Transaction:
    def __init__(self, sender: string, receiver: string, amount):
        self.sender_userName = sender
        self.receiver_userName = receiver
        self.amount: float = amount
        self.id = generate_random_id()


#################################################################
class Blockchain:
    def __init__(self):
        self.chain = []

        #   Initial block with a genesis_hash
        genesis_transaction = Transaction("Genesis", "Genesis", 0)
        block = {'index': len(self.chain) + 1,
                 'timestamp': time.time(),
                 #  'proof': proof
                 'hash_of_previous_block': 'Genesis_hash',
                 'transaction': genesis_transaction
                 }
        # block['curr_block_hash'] = self.hash(block)  # Compute the hash of the new block
        self.chain.append(block)
        #   Create the "genesis transaction"
        # self.create_block()
        # self.chain[0]['hash_of_previous_block'] = 'Genesis_hash'


    # #   Will create a block that will also hold a transaction object
    # def create_block(self, hash_of_previous_block, transaction: Transaction = None):
    #     block = {'index': len(self.chain) + 1,
    #              'timestamp': time.time(),
    #              #  'proof': proof
    #              'hash_of_previous_block': hash_of_previous_block,
    #              'transaction': transaction
    #              }
    #     # block['curr_block_hash'] = self.hash(block)  # Compute the hash of the new block
    #     self.chain.append(block)
    #     return block

    #   Will create a block that will also hold a transaction object
    def create_block(self, transaction: Transaction):
        block = {'index': len(self.chain) + 1,
                 'timestamp': time.time(),
                 #  'proof': proof
                 'hash_of_previous_block': self.hash(self.get_previous_block()),
                 'transaction': transaction
                 }
        # block['curr_block_hash'] = self.hash(block)  # Compute the hash of the new block
        self.chain.append(block)
        return block


    def get_previous_block(self):
        #   Used to get the last block in the chain
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
        block_to_encode = str(block).encode()
        #   compute the SHA-256 hash of the encoded block, and convert the hash into a hexadecimal string
        return hashlib.sha256(block_to_encode).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['hash_of_previous_block'] != self.hash(previous_block):
                return False
            #   Commented out because we removed the proof of work feature
            # previous_proof = previous_block['proof']
            # proof = block['proof']
            # hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # if hash_operation[:4] != '0000':
            #     return False
            previous_block = block
            block_index += 1
        return True

    def print_blockchain(self):
        for block in self.chain:
            print("\n")
            print(f"Block {block['index']}:")
            print(f"  Timestamp: {block['timestamp']}")
            print(f"  Previous Hash: {block['hash_of_previous_block']}")
            print(f"  Transaction:")
            print(f"    From: {block['transaction'].sender_userName}")
            print(f"    To: {block['transaction'].receiver_userName}")
            print(f"    Amount: {block['transaction'].amount}")
            print(f"    Transaction: {block['transaction'].id}")
            print("\n")

    def print_last_block(self):
        block = self.chain[-1]  # Get the last block in the chain
        print("\n")
        print(f"Block {block['index']}:")
        print(f"  Timestamp: {block['timestamp']}")
        print(f"  Previous Hash: {block['hash_of_previous_block']}")
        print(f"  Transaction:")
        print(f"    From: {block['transaction'].sender_userName}")
        print(f"    To: {block['transaction'].receiver_userName}")
        print(f"    Amount: {block['transaction'].amount}")
        print(f"    Transaction: {block['transaction'].id}")
        print("\n")


    #   Not needed since we will only have 1 transaction per block
    # def add_transaction(self, transaction):
    #     self.transactions.append(transaction)
    #     return self.get_previous_block()['index'] + 1

    # def mine_block(self):
    #     previous_block = self.get_previous_block()
    #     # previous_proof = previous_block['proof']
    #     # proof = self.proof_of_work(previous_proof)
    #     hash_of_previous_block = self.hash(previous_block)
    #     block = self.create_block(, hash_of_previous_block)
    #     return block

def testing_Blockchain():
    pass
    # mainBlockchain = Blockchain()
    # mainBlockchain.create_block("fake_trans")
    # print(mainBlockchain.chain)

if __name__=="__main__":
    testing_Blockchain()
