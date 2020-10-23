import pickle

from abc import ABC, abstractclassmethod, abstractstaticmethod
from typing import Any, Generic, Tuple, TypeVar, Type, Union

import numpy as np

KeyPartTypeT = TypeVar('KeyPartTypeT', str, int, np.ndarray)
class KeyPart(Generic[KeyPartTypeT]):
    def __init__(self, key_data: KeyPartTypeT):
        self.key = key_data
        self.key_type = type(key_data)


class Key:
    def __init__(self, text_key: KeyPart, image_row_key: KeyPart, image_col_key: KeyPart):
        self._text_key = text_key
        self._image_row_key = image_row_key
        self._image_col_key = image_col_key

    @classmethod
    def import_key(cls, filepath: str):
        with open(filepath, "rb") as f:
            return pickle.load(f)

    def export_key(self, filepath: str):
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    def get_text_key(self) -> KeyPart:
        return self._text_key

    def set_text_key(self, key: KeyPart) -> KeyPartTypeT:
        self._text_key = key

    def get_image_keys(self) -> Tuple[KeyPart, KeyPart]:
        return (self._image_row_key, self._image_col_key)

    def set_image_keys(self, image_row_key: KeyPart, image_col_key: KeyPart):
        self._image_row_key = image_row_key
        self._image_col_key = image_col_key


class KeyModifier(ABC):
    @abstractstaticmethod
    def modify_key(key: Key, message: str) -> Key:
        pass
