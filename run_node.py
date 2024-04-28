from p2p.node import Node
from utils.utils import bcolors
import random, threading, pickle
from blockchain.auth import load_private_key_from_file
from p2p.connection import Connection

HOST = "127.0.0.1"
PORT = random.randint(49152, 65536)

commands = f"""
Below are listed available commands:
    {bcolors.BLUE}/connect [host]:[port]
    /send --host [host] --port [port] [message]
    /q
    /h
    /send_signed_transaction{bcolors.ENDC}
"""

if __name__ == "__main__":
    print(commands)

    running = True

    private_key = load_private_key_from_file("key.pem")

    connection = Connection(HOST, PORT)
    node = Node(connection, private_key)
    node.run()

    while running:
        try:
            inp = input("~ ")
            split = inp.split()

            if len(split) == 0:
                continue

            if split[0] == '/connect':
                host, port = split[1].split(sep=':')
                node.connect(host, int(port))

            elif split[0] == '/send':
                if split[1] == '--host':
                    host = split[2]
                    if split[3] != '--port':
                        continue
                    port = int(split[4])
                    node.send_to(host, port, pickle.dumps(" ".join(split[5:])))

                node.broadcast(pickle.dumps(inp[6:]))

            elif split[0] == '/send_signed_transaction':
                receiver = input("  receiver: ")
                amount = int(input("  amount: "))
                node.send_signed_transaction(receiver, amount)

            elif split[0] == '/q':
                node.shutdown()
                running = False

        except:
            running = False
