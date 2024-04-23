from blockchain import Block, BlockChain, Transaction
import random

TRANSACTIONS_IN_BLOCK = 2
LEADING_ZEROS = 2

def create_blockchain(n = 5):
    block_chain = BlockChain(LEADING_ZEROS)
    
    for _ in range(n):
        block = Block()
        for _ in range(TRANSACTIONS_IN_BLOCK):
            block.add_transaction(Transaction(random.randint(0, 20), random.randint(0, 20), random.randint(1, 20000)))
        block.mine(block_chain.leading_zeros)
        block_chain.add_block(block)

        print(str(block_chain))
    
def create_blockchain_animation():
    block_chain = BlockChain(LEADING_ZEROS)
    while True:
        m = input("> ")
        if m == 'q':
            break

        block = Block()
        for _ in range(TRANSACTIONS_IN_BLOCK):
            block.add_transaction(Transaction(random.randint(0, 20), random.randint(0, 20), random.randint(1, 20000)))
        block.mine(block_chain.leading_zeros)
        block_chain.add_block(block)

        print(str(block_chain))

if __name__ == "__main__":

    #create_blockchain()
    
    create_blockchain_animation()
