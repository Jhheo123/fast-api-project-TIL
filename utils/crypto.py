import hashlib
from passlib.context import CryptContext


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def _normalize(self, secret: str) -> str:
        return hashlib.sha256(secret.encode("utf-8")).hexdigest()
    def encrypt(self, secret: str) -> str:
        print(">>> CRYPTO VERSION: normalize enabled")  # 이게 찍히는지 확인!
        # normalized = self._normalize(secret)        
        return self.pwd_context.hash(secret)
    def verify(self, secret: str, hashed: str) -> bool:
        # normalized = self._normalize(secret)
        return self.pwd_context.verify(secret, hashed)