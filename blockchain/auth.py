from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

def load_private_key_from_file(file_path: str) -> RSAPrivateKey:
    private_key = None
    try:
        key_file = open(file_path, "rb")
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    except:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        key_file = open("key.pem", "w")
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
        )
    key_file.close()
    return private_key

def load_private_key() -> RSAPrivateKey:
    return load_private_key_from_file("./key.pem")

def get_public_key(private_key: RSAPrivateKey) -> RSAPublicKey:
    return private_key.public_key()

def public_key_from_str(public_key_str: str) -> RSAPublicKey:
    public_key_str = "-----BEGIN PUBLIC KEY-----" + public_key_str + "-----END PUBLIC KEY-----"
    return serialization.load_pem_public_key(public_key_str.encode())

def str_from_public_key(public_key: RSAPublicKey) -> str:
    public_key_human = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_string = "".join(public_key_human.decode().split(sep='\n')[1:-2])
    return public_key_string

def sign(private_key: RSAPrivateKey, b: bytes) -> bytes:
    return private_key.sign(
        b,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def str_from_signature(signature: bytes) -> str:
    return signature.hex()

def bytes_from_str_signature(str_signature: str) -> bytes:
    return bytes.fromhex(str_signature)

def verify(public_key: RSAPublicKey, signature: bytes, b: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            b,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature as e:
        return False
