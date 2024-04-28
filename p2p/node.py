from typing import List
import random, pickle, threading, socket
from utils.utils import bcolors
from blockchain.blockchain import Transaction, BlockChain, Block
import blockchain.auth as auth
from p2p.message import Message
from p2p.connection import Connection

class Node():

    def __init__(self, connection, private_key):
        self.connection: Connection = connection
        self.private_key = private_key
        self.public_key = auth.get_public_key(private_key)
        self.id = random.randint(0, 10000000)
        self.blockchain = BlockChain()
        self.msg_buffer = []
        self.connection.buff = self.msg_buffer

    def run(self):
        listen_thread = threading.Thread(target=self.connection.listen, daemon=False)
        listen_thread.start()

        consumer_thread = threading.Thread(target=self.consume_messages, daemon=False)
        consumer_thread.start()

    # TODO  concurrent modifying buffer by consumer and msg receiver in connection
    def consume_messages(self):
        while True:
            while len(self.msg_buffer) == 0: continue
            msg = self.msg_buffer.pop(0)
            msg.consume(self.blockchain)

    def send_signed_transaction(self, receiver, amount):
        t = Transaction(auth.str_from_public_key(self.public_key), receiver, amount)
        t.sign(self.private_key, self.public_key)
        self.blockchain.pending_transactions.append(t)
        self.broadcast(pickle.dumps(Message(Message.NEW_TRANSACTION, t)))

    # TODO open UDP channel for that ??? (for now connections is established and closed after sending the message)
    # or keep connection open
    def send_to(self, host, port, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data)

    def connect(self, host, port):
        self.connection.connect(host, port)

    def broadcast(self, data: bytes):
        self.connection.broadcast(data)

    def shutdown(self):
        self.connection.close()
