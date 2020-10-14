from random import choice
from string import ascii_lowercase
from typing import Tuple

from TextEncryption.KeyModifiers import RepeatToMessageLengthModifier, LowercaseKeyModifier, apply_modifiers
from TextEncryption import Cipher
from TextEncryption import Key
from DataSanitization.Sanitizers import AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer, apply_sanitizers


class VigenereCipher(Cipher):
    data_sanitizers = [AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer]
    key_modifiers = [RepeatToMessageLengthModifier, LowercaseKeyModifier]
    @staticmethod
    def encrypt_message(message: str, key: Key) -> str:
        clean_msg = apply_sanitizers(message, *VigenereCipher.data_sanitizers)
        valid_key = apply_modifiers(key, message, *VigenereCipher.key_modifiers)
        key_data = valid_key.get_key()
        ciphertext = ""
        for i in range(len(clean_msg)):
            clean_msg_int = ord(clean_msg[i]) - ord('a')
            key_data_int = ord(key_data[i]) - ord('a')
            char = (clean_msg_int + key_data_int)  % 26
            char += ord('A')
            ciphertext += chr(char)
        return ciphertext

    @staticmethod
    def decrypt_message(message: str, key: Key) -> str:
        clean_msg = apply_sanitizers(message, *VigenereCipher.data_sanitizers)
        valid_key = apply_modifiers(key, message, *VigenereCipher.key_modifiers)
        key_data = valid_key.get_key()
        plaintext = ""
        for i in range(len(message)):
            cipher_int = ord(clean_msg[i]) - ord('a')
            key_int = ord(key_data[i]) - ord('a')
            char = (cipher_int - key_int + 26) % 26
            char += ord('A')
            plaintext += chr(char)
        return plaintext

    @staticmethod
    def generate_key(key_size: int) -> Key:
        return Key("".join(choice(ascii_lowercase) for _ in range(key_size)))

