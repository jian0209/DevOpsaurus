from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
from conf.config import Config as c


class AESCipher:
    def __init__(self, key):
        hashed_key = hashlib.sha512(key.encode()).hexdigest()[:32]
        self.key = bytes.fromhex(hashed_key)

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, enc: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted_data = base64.b64decode(enc)
        decrypted = cipher.decrypt(encrypted_data)
        return unpad(decrypted, AES.block_size).decode('utf-8')
