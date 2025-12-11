from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

def load_private_key(path: str):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

def load_public_key(path: str):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = plaintext.decode("utf-8")
    if len(seed) != 64 or any(c not in "0123456789abcdef" for c in seed.lower()):
        raise ValueError("Invalid 64-char hex seed format")
    
    return seed.lower()

def sign_message(message: str, private_key) -> bytes:
    return private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
