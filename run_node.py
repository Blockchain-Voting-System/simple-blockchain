from node import Node
from utils import bcolors
import random, threading

HOST = "127.0.0.1"
PORT = random.randint(49152, 65536)

commands = f"""
Below are listed available commands:
    {bcolors.BLUE}/connect{bcolors.ENDC} [host]:[port]
    {bcolors.BLUE}/send{bcolors.ENDC} --host [host] --port [port] [message]
    {bcolors.BLUE}/q{bcolors.ENDC}
    {bcolors.BLUE}/h{bcolors.ENDC}
"""

if __name__ == "__main__":
    print(commands)
    
    running = True
    
    node = Node(HOST, PORT)

    t = threading.Thread(target=node.run, daemon=False)
    t.start()

    while running:
        try:
            inp = input(">")
            split = inp.split()
            
            if len(split)==0:
                continue
            
            if split[0] == '/connect':
                host, port = split[1].split(sep=':')
                node.connect_to_node(host, int(port))
            
            elif split[0] == '/send':
                node.send_to_all(inp[6:])
            
            elif split[0] == '/q':
                node.shutdown()
                running = False
            
        except:
            running = False
    
    t.join()

