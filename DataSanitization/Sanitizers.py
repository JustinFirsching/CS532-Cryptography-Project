from abc import ABC, abstractstaticmethod
from typing import List


class DataSanitizer(ABC):
    @abstractstaticmethod
    def sanitize(message: str) -> str:
        pass


class AlphaNumericSanitizer(DataSanitizer):
    @staticmethod
    def sanitize(message: str) -> str:
        return "".join([m for m in message if m.isalphanum() or m == " "])


class AlphaSanitizer(DataSanitizer):
    @staticmethod
    def sanitize(message: str) -> str:
        return "".join([m for m in message if m.isalpha() or m == " "])


class NoSpacesSanitizer(DataSanitizer):
    @staticmethod
    def sanitize(message: str) -> str:
        return message.replace(" ", "")

class NumberOnlySanitizer(DataSanitizer):
    @staticmethod
    def sanitize(message: str) -> str:
        return "".join([m for m in message if m.isnum()])


class LowercaseCharacterSanitizer(DataSanitizer):
    @staticmethod
    def sanitize(message: str) -> str:
        return message.lower()


def apply_sanitizers(message: str, *sanitizers: List[DataSanitizer]):
    for sanitizer in sanitizers:
        message = sanitizer.sanitize(message)
    return message
