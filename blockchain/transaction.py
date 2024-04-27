import auth
import hashlib, pickle, datetime

class Transaction():
    def __init__(self, sender: str, receiver: str, amount: int):
        self.sender: str = sender
        self.receiver: str = receiver
        self.amount: int = amount
        self.timestamp: str = str(datetime.datetime.now())
        self.signature: str = None

    def get_bytes_without_signature(self) -> bytes:
        return pickle.dumps(
            {
                "sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount,
                "timestamp": self.timestamp
            }
        )

    def sign(self, private_key, public_key) -> None:
        if self.sender == auth.str_from_public_key(public_key):
            signature = auth.sign(private_key, self.get_bytes_without_signature())
            self.signature = auth.str_from_signature(signature)

    def verify(self) -> bool:
        return self.signature is not None and auth.verify(auth.public_key_from_str(self.sender), auth.bytes_from_str_signature(self.signature), self.get_bytes_without_signature())

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    def __hash__(self) -> str:
        return hashlib.sha256(self.serialize()).hexdigest()

    def __str__(self) -> str:
        return f'sender: {self.sender}, receiver: {self.receiver}, amount: {self.amount}, at: {self.timestamp}'

    def __eq__(self, other) -> bool:
        return self.amount == other.amount \
                and self.sender == other.sender \
                and self.receiver == self.receiver \
                and self.timestamp == other.timestamp
