"""Standard cryptography manager for general encryption needs"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import logging

logger = logging.getLogger(__name__)


class CryptoManager:
    """Manager for standard encryption operations"""
    
    def __init__(self):
        # Generate or load encryption key
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        
        # AES-GCM for additional security
        self.aes_key = AESGCM.generate_key(bit_length=256)
        self.aes_gcm = AESGCM(self.aes_key)
        
        logger.info("Crypto manager initialized")
    
    def encrypt_bytes(self, data: bytes) -> bytes:
        """Encrypt bytes using Fernet"""
        return self.fernet.encrypt(data)
    
    def decrypt_bytes(self, encrypted_data: bytes) -> bytes:
        """Decrypt bytes using Fernet"""
        return self.fernet.decrypt(encrypted_data)
    
    def encrypt_aes_gcm(self, data: bytes, associated_data: bytes = b"") -> Tuple[bytes, bytes]:
        """Encrypt using AES-GCM"""
        nonce = os.urandom(12)
        ciphertext = self.aes_gcm.encrypt(nonce, data, associated_data)
        return nonce, ciphertext
    
    def decrypt_aes_gcm(self, nonce: bytes, ciphertext: bytes, associated_data: bytes = b"") -> bytes:
        """Decrypt using AES-GCM"""
        return self.aes_gcm.decrypt(nonce, ciphertext, associated_data)
