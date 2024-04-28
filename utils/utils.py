from blockchain.blockchain import Block, Transaction, BlockChain
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

def create_sample_transaction(sender):
    transaction = Transaction(sender, "abcd123", 100)
    transaction.timestamp = "long time ago"
    return transaction

def create_sample_block(prev_hash):
    block = Block()
    block.previous_hash = prev_hash
    for _ in range(2):
        t = create_sample_transaction("sndr")
        t.signature = "signature"
        block.transactions.append(t)
    return block

def create_sample_blockchain():
    blockchain = BlockChain()
    blockchain.leading_zeros = 1
    for _ in range(3):
        block = create_sample_block(blockchain.blocks[-1].hash)
        block.mine(blockchain.leading_zeros)
        blockchain.add_block(block)
    return blockchain
