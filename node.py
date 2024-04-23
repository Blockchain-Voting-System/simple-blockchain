from typing import List
import random, pickle, threading, socket, ecdsa
from utils import bcolors

PRIVATE_KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'

signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(PRIVATE_KEY), curve=ecdsa.SECP256k1)
verifying_key = signing_key.get_verifying_key()
public_key_hex = verifying_key.to_string().hex()

class Node():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = random.randint(0, 10000000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_connections = []
        self.out_connections = []
        self.valid_blockchain = None

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        print(f"{bcolors.GREEN}Node started on address: {self.host}:{self.port}{bcolors.ENDC}")
        
        while True:
            try:
                conn, addr = self.sock.accept()
                self.in_connections.append(conn)
                print(f"Node connected: {bcolors.BLUE}{addr[0]}:{addr[1]}{bcolors.ENDC}")
                
                handle_connection = threading.Thread(target = self.handle_in_connection, args=(conn,))
                handle_connection.start()

            except Exception as e:
                print(f"{bcolors.FAIL}Server stopped!{bcolors.ENDC}")
                self.sock.close()
                break
            
    def handle_in_connection(self, socket):
        while True:
            try:
                msg = socket.recv(4096)
                print(msg)
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

        print(f"Connected to node {bcolors.BLUE}{host}:{port}{bcolors.ENDC}.")
        
    def send_to_all(self, data): 
        serialized = pickle.dumps(data)
               
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
