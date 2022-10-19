import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from backports.pbkdf2 import pbkdf2_hmac


def gen_vkey(mas_key: str, salt: bytes) -> bytes:
    passwd = mas_key.encode("utf8")
    return pbkdf2_hmac("sha256", passwd, salt, 100000, 32)


def gen_rsa() -> tuple[bytes, bytes]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return key.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ), \
           key.private_bytes(
               serialization.Encoding.DER,
               serialization.PrivateFormat.PKCS8,
               serialization.NoEncryption()
           )


def rsa_enc(plaintext: str, key_bytes: bytes) -> bytes:
    return serialization.load_der_public_key(key_bytes).encrypt(
        plaintext.encode("utf8"),
        padding.OAEP(
            padding.MGF1(hashes.SHA256()),
            hashes.SHA256(),
            None
        )
    )


def rsa_dec(ciphertext: bytes, key_bytes: bytes) -> str:
    return serialization.load_der_private_key(key_bytes, None).decrypt(
        ciphertext,
        padding.OAEP(
            padding.MGF1(hashes.SHA256()),
            hashes.SHA256(),
            None
        )
    ).decode("utf8")


def aes_enc(data: bytes, key: bytes) -> bytes:
    data = data + bytearray((16 - (len(data) % 16)) % 16)  # Pad to the block size
    iv = os.urandom(16)
    enc = Cipher(algorithms.AES256(key), modes.CBC(iv)).encryptor()
    return iv + enc.update(data) + enc.finalize()


def aes_dec(data: bytes, key: bytes) -> bytes:
    iv = data[:16]
    ciphertext = data[16:]
    dec = Cipher(algorithms.AES256(key), modes.CBC(iv)).decryptor()
    return (dec.update(ciphertext) + dec.finalize()).rstrip(b'\0')


def hash_url(data: str, salt: bytes) -> bytes:
    h = hashes.Hash(hashes.SHA256())
    h.update(data.encode("utf8"))
    temp = h.finalize() + salt

    h = hashes.Hash(hashes.SHA256())
    h.update(temp)
    return h.finalize()


