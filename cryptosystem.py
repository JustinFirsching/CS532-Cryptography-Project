import os
import re
import sys

import numpy as np

from enum import Enum
from cv2 import cv2

from TextEncryption import Cipher
from TextEncryption.Vigenere import VigenereCipher
from TextEncryption import Key
from Steganography import *


RANDOM_STR_KEY_SIZE = 32
RANDOM_MATRIX_KEY_SIZE = 2


class Capability(Enum):
    ENCRYPT = 0
    DECRYPT = 1


def get_targeted_event() -> Capability:
    selection = None
    while(selection is None):
        print("Select the targeted operation")
        print("[1] Encrypt")
        print("[2] Decrypt")
        user_input = input("Selection: ").lower().strip()
        if user_input in ["1", "[1]", "encrypt", "[1] encrypt"]:
            selection = Capability.ENCRYPT
        elif user_input in ["2", "[2]", "decrypt", "[2] decrypt"]:
            selection = Capability.DECRYPT
        else:
            print("Invalid Selection!", file=sys.stderr)
    return selection

def get_text_encryption() -> Cipher:
    # TODO: Implement more than one encryption method
    return VigenereCipher

def get_text() -> str:
    # Strip the input to get rid of random spaces at beginning or end
    return input("Enter the text you would like to use: ").strip()

def get_str_key(cipher: Cipher, required: bool = False) -> Key:
    if required:
        input_key = ""
        while not input_key:
            input_key = input("Key: ").strip()
        key = Key(input_key)
    else:
        user_input = input("Desired Key (Press Enter to Generate a Random One): ")
        if user_input:
            key = Key(user_input)
        else:
            key = cipher.generate_key(RANDOM_STR_KEY_SIZE)
            print(f"Your text encryption key is: {key.get_key()}")
    return key

def get_matrix_key(cipher: Cipher, required: bool = False) -> Key:
    pass

def get_key(cipher: Cipher, required: bool = False) -> Key:
    if cipher.desired_key_type is np.ndarray:
        key_fetcher = get_matrix_key
    else:
        key_fetcher = get_str_key
    return key_fetcher(cipher, required)


def get_image(min_size: int = 0, required=False) -> np.ndarray:
    image = None
    if required:
        while image is None:
            user_input = input("Path to image file: ").strip()
            if os.path.isfile(user_input):
                try:
                    image = cv2.imread(user_input)
                except Exception as ex:
                    print(f"Failed to read image!\n{ex.withtraceback}", file=sys.stderr)
                    exit(1)

    else:
        while image is None:
            user_input = input("Path to the image file (Press Enter to Generate a Random Image): ").strip()
            if not user_input:
                image_dims = get_square_dimensions(min_size)
                image = get_random_image(*image_dims)
                break
            elif not os.path.isfile(user_input):
                print(f"Could not find file {user_input}", file=sys.stderr)
                continue

            # Always read as color image
            image_read = cv2.imread(user_input, cv2.IMREAD_COLOR)
            valid_size = valid_image_size(image_read, min_size)
            if(valid_size):
                image = image_read
            else:
                print(f"Image is not large enough. Select an image with AT LEAST {min_size} pixels.",
                      file=sys.stderr)
    return image

def run_encryption():
    text_encryptor = get_text_encryption()
    text = get_text()
    key = get_key(text_encryptor)
    encrypted_message = text_encryptor.encrypt_message(text, key)
    min_pixels = get_minimum_size(encrypted_message)
    image = get_image(min_pixels)
    embedded_image = embed_message(encrypted_message, image)
    cv2.imwrite("Output.png", embedded_image)

def run_decryption():
    image = get_image(required=True)
    extracted_text = extract_message(image)
    text_decryptor = get_text_encryption()
    key = get_key(text_decryptor, True)  # The key is required here to get the actual text
    decrypted_message = text_decryptor.decrypt_message(extracted_text, key)
    print(decrypted_message)

def main():
    loop = True
    while(loop):
        method = get_targeted_event()
        if method is Capability.ENCRYPT:
            run_encryption()
        else:
            run_decryption()

        loop_input = input("Do you want to run again? [y/N] ")
        loop = loop_input.lower() in ["y", "yes"]


if __name__ == "__main__":
    main()

