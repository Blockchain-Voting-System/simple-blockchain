from typing import List
import hashlib, time, pickle
from blockchain.transaction import Transaction

# sender, receiver - public wallet addresses
    
class Block:
    def __init__(self, previous_hash: str = None):
        self.transactions: List[Transaction] = []
        self.previous_hash: str = previous_hash
        self.hash: str = ""
        self.nonce: int = 0
        self.time_to_mine: int = None

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def serialize(self) -> bytes:
        return pickle.dumps(self)
    
    def calculate_hash(self) -> str:
        self.hash = self.__hash__()
        return self.hash
    
    def mine(self, leading_zeros: int) -> None:
        start = time.time()
        self.calculate_hash()
        print("mining...")
        while not self.hash[0:leading_zeros] == "0" * leading_zeros:
            self.nonce += 1
            self.time_to_mine = time.time() - start
            self.calculate_hash()
            print(f"nonce: {self.nonce}, time: {time.time()-start} {self.hash[0:10]}", end='\r')
        print()

    def __str__(self) -> str:
        transaction_str = "\n".join(f"|   {t}" for t in self.transactions)
        return  f"|------------------------------------------------\n" \
                f"| hash: {self.hash}\n" \
                f"| prev_hash: {self.previous_hash}\n" \
                f"| transactions:\n{transaction_str}\n" \
                f"| nonce: {self.nonce}\n" \
                f"| time_to_mine: {self.time_to_mine}\n" \
                f"|------------------------------------------------\n|" \
    
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
    
    def validate(self) -> bool:
        for i in range(1, len(self.blocks)):
            print(self.blocks[i].previous_hash)
            print(self.blocks[i-1].__hash__())
            if self.blocks[i].previous_hash != self.blocks[i-1].__hash__():
                return False
        return True

    def __str__(self) -> str:
        return "\n".join(f"{b}" for b in self.blocks)
    