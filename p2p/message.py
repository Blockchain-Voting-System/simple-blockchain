
class Message:

    NEW_TRANSACTION = 1
    TRANSACTION_TO_SIGN = 2
    NEW_BLOCK = 3
    UPDATE_BLOCKCHAIN = 4
    GET_BLOCKCHAIN = 5
    NODE_JOINED = 6
    NODE_LEFT = 7

    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.consumers = {
            self.NEW_TRANSACTION: self.new_transaction
        }

    def consume(self, blockchain):
        self.consumers[self.type](blockchain)

    def new_transaction(self, blockchain):
        print(self.data)
