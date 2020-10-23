from random import choice
from string import ascii_lowercase
from typing import Tuple

from CryptoSystem.Key.KeyModifiers import RepeatToMessageLengthModifier, LowercaseKeyModifier, apply_modifiers
from CryptoSystem.Key import Key, KeyPart
from CryptoSystem.Ciphers import TextCipher
from CryptoSystem.DataSanitization.Sanitizers import AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer, apply_sanitizers


class VigenereCipher(TextCipher):
    data_sanitizers = [AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer]
    key_modifiers = [RepeatToMessageLengthModifier, LowercaseKeyModifier]
    @staticmethod
    def encrypt(message: str, key_part: KeyPart) -> str:
        # Create a temporary key since we know this is only relevant for text anyways
        key = Key(key_part, None, None)
        clean_msg = apply_sanitizers(message, *VigenereCipher.data_sanitizers)
        valid_key = apply_modifiers(key, message, *VigenereCipher.key_modifiers)
        key_data = valid_key.get_text_key().key
        ciphertext = ""
        for i in range(len(clean_msg)):
            clean_msg_int = ord(clean_msg[i]) - ord('a')
            key_data_int = ord(key_data[i]) - ord('a')
            char = (clean_msg_int + key_data_int)  % 26
            char += ord('A')
            ciphertext += chr(char)
        return ciphertext

    @staticmethod
    def decrypt(message: str, key: Key) -> str:
        clean_msg = apply_sanitizers(message, *VigenereCipher.data_sanitizers)
        valid_key = apply_modifiers(key, message, *VigenereCipher.key_modifiers)
        key_data = valid_key.get_text_key().key
        plaintext = ""
        for i in range(len(message)):
            cipher_int = ord(clean_msg[i]) - ord('a')
            key_int = ord(key_data[i]) - ord('a')
            char = (cipher_int - key_int + 26) % 26
            char += ord('A')
            plaintext += chr(char)
        return plaintext

    @staticmethod
    def generate_key_part(key_size: int) -> KeyPart:
        return KeyPart("".join(choice(ascii_lowercase) for _ in range(key_size)))

