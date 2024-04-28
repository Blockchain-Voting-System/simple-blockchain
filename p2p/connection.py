import random, pickle, threading, socket
from utils.utils import bcolors

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.in_connections = []
        self.out_connections = []
        self.buff = []

    def listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        print(f"{bcolors.GREEN}Node started on address: {self.host}:{self.port}{bcolors.ENDC}")

        while True:
            try:
                conn, addr = self.sock.accept()
                self.in_connections.append(conn)
                print(f"Node connected: {bcolors.BLUE}{addr[0]}:{addr[1]}{bcolors.ENDC}")
                print(self.in_connections)
                print(self.out_connections)

                handle_connection = threading.Thread(target = self.receive, args=(conn,))
                handle_connection.start()

            except Exception as e:
                print(f"{bcolors.FAIL}Server stopped!{bcolors.ENDC}")
                self.sock.close()
                break

    def receive(self, socket):
        while True:
            try:
                msg = socket.recv(4096)
                received = pickle.loads(msg)
                self.buff.append(received)
                print(received)
            except Exception as e:
                print(f"{bcolors.BOLD}Node disconnected.{bcolors.ENDC}")
                self.in_connections.remove(socket)
                socket.close()
                break

    def connect(self, host, port):
        print(f"Connecting to node {bcolors.BLUE}{host}:{port}{bcolors.ENDC} ...")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.out_connections.append(s)

        handle_connection = threading.Thread(target = self.receive, args=(s,))
        handle_connection.start()

        print(f"Connected to node {bcolors.BLUE}{host}:{port}{bcolors.ENDC}.")

    def broadcast(self, data: bytes):
        for conn in self.out_connections:
            conn.sendall(data)

        for conn in self.in_connections:
            conn.sendall(data)

    def close(self):
        for sock in self.in_connections:
            sock.close()
        for sock in self.out_connections:
            sock.close()
        self.sock.close()
