import sys, time, unittest, hashlib
from blockchain.blockchain import BlockChain, Block, Transaction
import blockchain.auth as auth

class BlockchainTest(unittest.TestCase):

    def test_chain_validation(self):
        # when & then
        self.assertTrue(create_sample_blockchain().validate())

    def test_chain_validation_returns_false_when_not_valid(self):
        # given
        sample_blockchain = create_sample_blockchain()
        sample_blockchain.blocks[1].hash = hashlib.sha256("asdf".encode()).hexdigest()

        # when & then
        self.assertFalse(sample_blockchain.validate())

    def test_sign_and_verify_transaction(self):
        # given
        private_key, public_key = load_key_pair()
        transaction = create_sample_transaction(auth.str_from_public_key(public_key))

        # when
        transaction.sign(private_key, public_key)

        # then
        self.assertTrue(transaction.verify())

    def test_verify_transaction_returns_false_when_wrong_signature(self):
        # given
        private_key, public_key = load_key_pair()
        transaction = create_sample_transaction(auth.str_from_public_key(public_key))

        # when
        transaction.signature = auth.str_from_signature(auth.sign(private_key, "idk".encode()))

        #then
        self.assertFalse(transaction.verify())


def load_key_pair():
    private_key = auth.load_private_key_from_file("./resources/test_private_key.pem")
    public_key = auth.get_public_key(private_key)
    return private_key, public_key

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


if __name__ == '__main__':
    unittest.main()
