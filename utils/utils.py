from blockchain.blockchain import Block, Transaction
import random

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_block():
    block = Block()
    for _ in range(2):
        t = Transaction("1", "2", 100)
        t.timestamp = "123"
        block.add_transaction(t)
    block.mine(2)
    block.time_to_mine = 1.0
    block.nonce = 132
    return block
