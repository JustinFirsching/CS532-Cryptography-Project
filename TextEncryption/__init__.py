from abc import ABC, abstractclassmethod, abstractstaticmethod
from typing import Any, Generic, Tuple, TypeVar, Type, Union


KeyTypeT = TypeVar('KeyTypeT', bound='Key')
class Key(Generic[KeyTypeT]):
    def __init__(self, key_data: KeyTypeT):
        self._key_data = key_data
        self._key_type = type(key_data)

    def get_key(self) -> KeyTypeT:
        return self._key_data

    def get_key_type(self) -> Type:
        return self._key_type


class KeyModifier(ABC):
    @abstractstaticmethod
    def modify_key(key: Key, message: str) -> Key:
        pass


class Cipher(ABC):
    desired_key_type = str
    @abstractstaticmethod
    def encrypt_message(message: str, key: Key) -> str:
        pass

    @abstractstaticmethod
    def decrypt_message(message: str, key: Key) -> str:
        pass

    @abstractstaticmethod
    def generate_key(key_size: int) -> Key:
        pass
