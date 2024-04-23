import random
from blockchain.blockchain import Transaction, Block, BlockChain

from blockchain.auth import *

TRANSACTIONS_IN_BLOCK = 2
LEADING_ZEROS = 1

def create_blockchain(n = 20):
    block_chain = BlockChain(LEADING_ZEROS)
    
    for _ in range(n):
        block = Block()
        for _ in range(TRANSACTIONS_IN_BLOCK):
            block.add_transaction(Transaction(random.randint(0, 20), random.randint(0, 20), random.randint(1, 20000)))
        block.mine(block_chain.leading_zeros)
        block_chain.add_block(block)
        print(block)
        print(str(block_chain))
        
    print(block_chain.validate())
    
def create_blockchain_animation():
    block_chain = BlockChain(LEADING_ZEROS)
    while True:
        m = input("~ ")
        if m == 'q':
            break

        block = Block()
        for _ in range(TRANSACTIONS_IN_BLOCK):
            block.add_transaction(Transaction(random.randint(0, 20), random.randint(0, 20), random.randint(1, 20000)))
        block.mine(block_chain.leading_zeros)
        block_chain.add_block(block)

        print(str(block_chain))
        
def sign_transaction():
    private_key = load_private_key()
    public_key = auth.get_public_key(private_key)
    
    t = Transaction(auth.str_from_public_key(public_key), "sadfsafdasfbcxvb", 123321)
    t.timestamp = "1234"
    t.sign(private_key, public_key)

    print(t.verify())
    print(t.signature)
    
def verify_transaction():
    private_key = load_private_key()
    public_key = get_public_key(private_key)
    t = Transaction(str_from_public_key(public_key), "sadfsafdasfbcxvb", 123321)
    t.timestamp = "1234"
    t.signature = "a8e78b5cef24c40a483ba9872588ec54afa958283f3f32128617940e314f94f131ba2bcde3f76ee28e0d0dcd1026b832e05c32aaef4322492c4b8d06d54e27ed90311c32c512079bb8cb0a095324e636f4fbc53727b1e4c63e2a66ca43e204a8b01cc4d8c224b9c6fa308f00193fae360712632591f9f9edabf1d5f051877dd785496466746383dab8cb2c2fe230221cf12968aaa487b2a6434ed805a8fd3593e243719d759dd4f42d6696e204f88b2661c620549589b72051efa774a52cd3e03dc0f030ebf9cd5e5be4d286134932a570d8e825f616b2db316f8b4e77674730c301f4c75a82e0baa59e6e5cd6c634b7adc1487cd453fff072883d3207455853"
    
    print(t.verify())

if __name__ == "__main__":

    #create_blockchain()
    
    create_blockchain_animation()
    
    #sign_transaction()

    #verify_transaction()
