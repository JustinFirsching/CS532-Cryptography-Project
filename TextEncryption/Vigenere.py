from string import ascii_lowercase
from random import choice

from TextEncryption import Cipher
from TextEncryption import Key
from DataSanitization.Sanitizers import AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer, apply_sanitizers


class VigenereCipher(Cipher):
    data_sanitizers = [AlphaSanitizer, LowercaseCharacterSanitizer, NoSpacesSanitizer]
    key_modifiers = [PadKeyModifier]
    @staticmethod
    def encrypt_message(message: str, key: Key):
        clean_msg = apply_sanitizers(message, *VigenereCipher.data_sanitizers)


    @staticmethod
    def decrypt_message(message: str, key: Key):
        pass

    @staticmethod
    def generate_key(key_size: int) -> Key:
        return "".join(choice(ascii_lowercase) for _ in range(key_size))

# Makes Repeating Key
def genRepeatingKey(plaintext, key):
    if len(key) == len(plaintext):
        return(key)
    elif len(key) < len(plaintext):
        key = list(key)
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
        return(''.join(key))

    return (key[:len(plaintext)])

# Encrypts message with key, generates key if not provided. Repeats key if provided
def encrypt(message, key='', isRandomKey = False):
    plaintext = stripText(message)
    key = stripText(key)
    if (key == '') or (isRandomKey is True):
        key = genRandomKey(plaintext)
    key = genRepeatingKey(plaintext, key)
    ciphertext = []
    for i in range(len(plaintext)):
        char = ( ord(plaintext[i]) + ord(key[i]) ) % 26
        char += ord('A')
        ciphertext.append(chr(char))
    return { 'ciphertext': ''.join(ciphertext), 'key': key }

# Decrypts ciphertext with key
def decrypt(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        char = ( ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        char += ord('A')
        plaintext.append(chr(char))
    return ''.join(plaintext)

message = 'Hello_World! ! !'
print(message)
encrypted_message = encrypt(message)
decrypted = decrypt(encrypted_message['ciphertext'], encrypted_message['key'])
print(decrypted)
