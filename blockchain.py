from typing import List
import hashlib
import datetime
import sys
import time
import pickle

# sender, receiver - wallet public addresses

class Serializable:

    def serialize(self):
        return pickle.dumps(self)
    
    def hash(self) -> str:
        return hashlib.sha256(self.serialize()).hexdigest()

class Transaction(Serializable):
    def __init__(self, sender: int, receiver: int, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = str(datetime.datetime.now())
        self.signature = None

    def sign(self):
        pass

    def __str__(self):
        return f'sender: {self.sender}, receiver: {self.receiver}, amount: {self.amount}, at: {self.timestamp}'
    
    def __eq__(self, other):
        return self.amount == other.amount and self.sender == other.sender and self.receiver == self.receiver and self.timestamp == other.timestamp
    
class Block:
    def __init__(self, previous_hash: str = None):
        self.transactions: List[Transaction] = []
        self.previous_hash: str = previous_hash
        self.hash: str = ""
        self.nonce: int = 0
        self.time_to_mine: int = None

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def serialize(self):
        return pickle.dumps(self)
    
    def calculate_hash(self) -> str:
        self.hash = self.__hash__()
        return self.hash
    
    def mine(self, leading_zeros):
        start = time.time()
        
        self.calculate_hash()
        while not self.hash[0:leading_zeros] == "0"*leading_zeros:
            self.nonce += 1
            self.calculate_hash()
            
        self.time_to_mine = time.time() - start

    def __str__(self) -> str:
        transaction_str = "\n".join(f"   {t}" for t in self.transactions)
        return  f"hash: {self.hash}\n" \
                f"prev_hash: {self.previous_hash}\n" \
                f"transactions:\n{transaction_str}\n" \
                f"nonce: {self.nonce}\n" \
                f"time_to_mine: {self.time_to_mine}\n"
    
    def __hash__(self) -> str:
        return hashlib.sha256(self.serialize()).hexdigest()
    
class BlockChain:
    def __init__(self, leading_zeros=2):
        self.leading_zeros = leading_zeros
        self.blocks: List[Block] = [self.create_genesis()]

    def create_genesis(self) -> Block:
        block = Block("")
        block.mine(self.leading_zeros)
        return block
    
    def add_block(self, block: Block) -> None:
        block.previous_hash = self.blocks[-1].hash
        self.blocks.append(block)

    def get_size(self) -> int:
        return len(self.blocks)

    def __str__(self) -> str:
        return "\n".join(f"{b}" for b in self.blocks)
    


t = Transaction(1,1,1)
print(t.hash())
print(t.hash())