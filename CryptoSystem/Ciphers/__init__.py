from abc import ABC, abstractstaticmethod
from typing import Any


from CryptoSystem.Key import Key, KeyPart


class Cipher(ABC):
    desired_key_type = str
    @abstractstaticmethod
    def encrypt(target: Any, key: Any) -> Any:
        pass

    @abstractstaticmethod
    def decrypt(target: Any, key: Any) -> Any:
        pass

    @abstractstaticmethod
    def generate_key_part(key_size: Any) -> Any:
        pass


class TextCipher(Cipher):
    desired_key_type = str
    @abstractstaticmethod
    def encrypt(message: str, key_part: KeyPart) -> str:
        pass

    @abstractstaticmethod
    def decrypt(message: str, key: Key) -> str:
        pass

    @abstractstaticmethod
    def generate_key_part(key_size: int) -> KeyPart:
        pass
