from typing import List
import random, pickle, threading, socket
from utils.utils import bcolors
from blockchain.blockchain import Transaction, BlockChain, Block

# TODO when in_connection comes, node cant send message to it

def create_blockchain(n = 3):
    block_chain = BlockChain(2)

    for _ in range(n):
        block = Block()
        block.previous_hash = block_chain.blocks[-1].hash
        for _ in range(2):
            block.add_transaction(Transaction(str(random.randint(0, 20)), str(random.randint(0, 20)), random.randint(1, 20000)))
        block.mine(block_chain.leading_zeros)
        block_chain.add_block(block)

    return block_chain

class Node():

    def __init__(self, host, port, private_key):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.id = random.randint(0, 10000000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_connections = []
        self.out_connections = []
        self.blockchain = create_blockchain()

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        print(f"{bcolors.GREEN}Node started on address: {self.host}:{self.port}{bcolors.ENDC}")

        while True:
            try:
                conn, addr = self.sock.accept()
                self.in_connections.append(conn)
                print(f"Node connected: {bcolors.BLUE}{addr[0]}:{addr[1]}{bcolors.ENDC}")

                handle_connection = threading.Thread(target = self.listen_for_messages, args=(conn,))
                handle_connection.start()

            except Exception as e:
                print(f"{bcolors.FAIL}Server stopped!{bcolors.ENDC}")
                self.sock.close()
                break

    def listen_for_messages(self, socket):
        while True:
            try:
                msg = socket.recv(4096)
                received_blockchain = pickle.loads(msg)
                print(received_blockchain)
                # TODO doesnt work, maybe generating hash in different terminal produces different output
                print(f"verified: {received_blockchain.validate()}")
            except Exception as e:
                print(f"{bcolors.BOLD}Node disconnected.{bcolors.ENDC}")
                self.in_connections.remove(socket)
                socket.close()
                break

    def connect_to_node(self, host, port):
        print(f"Connecting to node {bcolors.BLUE}{host}:{port}{bcolors.ENDC} ...")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.out_connections.append(s)

        handle_connection = threading.Thread(target = self.listen_for_messages, args=(s,))
        handle_connection.start()

        print(f"Connected to node {bcolors.BLUE}{host}:{port}{bcolors.ENDC}.")

    def sign_transaction(self, transaction: Transaction):
        pass

    def send_to_all(self, data):
        serialized = self.blockchain.serialize()

        for conn in self.out_connections:
            conn.sendall(serialized)

        for conn in self.in_connections:
            conn.sendall(serialized)

    def shutdown(self):
        for sock in self.in_connections:
            sock.close()
        for sock in self.out_connections:
            sock.close()
        self.sock.close()
