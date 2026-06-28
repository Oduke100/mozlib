from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64, hashlib, os

class Encrypt:
    def __init__(self, data, level, key):
        self.data = data 
        self.level = level
        self.key = key

    def encrypt(self):
        if self.level == "E":
            self.encoded = base64.b64encode(self.data.encode())
        
        elif self.level == "M":
            key = base64.urlsafe_b64encode(hashlib.sha256(self.key.encode()).digest())
            self.f = Fernet(key)
            self.encoded = self.f.encrypt(self.data.encode())
        
        elif self.level == "H":
            key = hashlib.sha256(self.key.encode()).digest()
            iv = os.urandom(16)

            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            self.encoded = iv + encryptor.update(self.data.encode()) + encryptor.finalize()

        else:
            return "Invalid encrypt-level!"
        
        return self.encoded
        
    def decrypt(self):
        if self.level == "E":
            decoded = base64.b64decode(self.encoded).decode()
        
        elif self.level == "M":
            decoded = self.f.decrypt(self.encoded).decode()

        elif self.level == "H":
            iv = self.encoded[:16]
            key = hashlib.sha256(self.key.encode()).digest()
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted = (decryptor.update(self.encoded[16:]) + decryptor.finalize()).decode()

            return decrypted
        
        else:
            return "Invalid decrypt-level!"
        
        return decoded