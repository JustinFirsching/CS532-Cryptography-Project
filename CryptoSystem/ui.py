import os
import sys

import ipywidgets as widgets
from IPython.display import display, FileLink
import numpy as np

from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, Tuple

from cv2 import cv2

from CryptoSystem.Strategy import encrypt, decrypt
from CryptoSystem.Ciphers import Cipher
from CryptoSystem.Ciphers.Vigenere import VigenereCipher
from CryptoSystem.Key import Key, KeyPart
from CryptoSystem.Steganography import get_random_image, get_random_square_image, \
                                       get_minimum_size, get_square_dimensions, \
                                       valid_image_size, extract_message, embed_message


RANDOM_STR_KEY_SIZE = 32
RANDOM_MATRIX_KEY_SIZE = 2


class CLIDecrypter:
    def __init__(self, text_encrypter: Cipher = VigenereCipher):
        self.cipher = text_encrypter

    def _get_image(self) -> np.ndarray:
        image_read = None
        while image_read is None:
            try:
                image_file = input("Enter the path to the image: ")
                if not os.path.isfile(image_file):
                    raise FileNotFoundError(f"Could not find file {image_file}")
                image_read = cv2.imread(image_file, cv2.IMREAD_COLOR)
            except Exception as ex:
                print(ex, file=sys.stderr)

        return image_read

    def _get_key(self) -> Key:
        key_read = None
        while not key_read:
            try:
                key_file = input("Enter the path to the key file: ")
                if not os.path.isfile(key_file):
                    raise FileNotFoundError(f"Could not find file {key_file}")
                key_read = Key.import_key(key_file)
            except Exception as ex:
                print(ex, file=sys.stderr)
        return key_read

    def get_data(self) -> Tuple[np.ndarray, Key, Cipher]:
        key = self._get_key()
        image = self._get_image()
        return key, image, self.cipher



class CLIEncrypter:
    def __init__(self, text_encrypter: Cipher = VigenereCipher):
        self.cipher = text_encrypter

    def _get_text(self) -> str:
        # Strip the input to get rid of random spaces at beginning or end
        return input("Enter the text you would like to use: ").strip()

    def _get_text_key_str(self) -> KeyPart:
        user_input = input("Desired Key (Press Enter to Generate a Random One): ")
        if user_input:
            key_part = KeyPart(user_input)
        else:
            key_part = self.cipher.generate_key(RANDOM_STR_KEY_SIZE)
        return key_part

    def _get_text_key_matrix(self) -> KeyPart:
        raise NotImplementedError("Matrix Key Grabbing Not Yet Implemented")

    def _get_text_key(self) -> KeyPart:
        if(self.cipher.desired_key_type is np.ndarray):
            key_part = self._get_text_key_matrix()
        else:
            key_part = self._get_text_key_str()
        return key_part

    def _get_image(self, min_size: int = 0):
        image = None
        while image is None:
            user_input = input("Path to the image file (Press Enter to Generate a Random Image): ").strip()
            if not user_input:
                image = get_random_square_image(min_size)
                break
            else:
                try:
                    image = self._get_image_from_file(user_input, min_size)
                except Exception as ex:
                    print(ex, file=sys.stderr)
        return image

    def _get_image_from_file(self, image_file: str, min_size: int):
        if not os.path.isfile(image_file):
            raise FileNotFoundError("Could not find file {user_input}")

        # Always read as color image
        image_read = cv2.imread(image_file, cv2.IMREAD_COLOR)
        valid_size = valid_image_size(image_read, min_size)
        if(not valid_size):
            raise IOError(f"Image is not large enough. Select an image with AT LEAST {min_size} pixels.")

        return image_read

    def get_data(self) -> Union[str, np.ndarray, KeyPart, Cipher]:
        # Text Encryption
        text = self._get_text()
        text_key = self._get_text_key()
        encrypted_text = self.cipher.encrypt(text, text_key)

        # Image Steganography
        image_min_size = get_minimum_size(encrypted_text)
        image = self._get_image(image_min_size)

        return text, image, text_key, self.cipher


class IPythonNB:
    def __init__(self, cipher: Cipher = VigenereCipher):
        self.cipher = cipher
        self.encrypted_text_widget = None
        self.decrypted_text_widget = None

    def display_encryption(self):
        style={'description_width' : 'initial'}

        encryption_text = widgets.Text(
            placeholder='Enter Text Here',
            description='Text to Encrypt:',
            disabled=False,
            style=style
        )
        display(encryption_text)


        encryption_key = widgets.Text(
            placeholder='Enter Key Here',
            description='Encryption Key:',
            disabled=False,
            style=style
        )
        display(encryption_key)

        encryption_image = widgets.FileUpload(
            description='Upload Image',
            accept='image/*',
            multiple=False,
            style=style
        )
        display(encryption_image)

        submit_button = widgets.Button(
            description='Submit',
            disabled=False,
            button_style='success',
            icon='check'
        )
        display(submit_button)

        submit_button.on_click(
            lambda *args: self.encrypt(encryption_text.value, encryption_key.value, encryption_image.value)
        )

    def add_encryption_output(self, encrypted_text: str, image_path: str, key_path: str):
        self.encrypted_text_widget = widgets.Text(
            value=encrypted_text,
            disabled=True
        )
        display(self.encrypted_text_widget)

        local_image = FileLink(image_path, result_html_prefix="Click here to download image: ")
        display(local_image)

        local_key = FileLink(key_path, result_html_prefix="Click here to download key: ")
        display(local_key)

    def add_decryption_output(self, decrypted_text: str, image_path: str):
        self.decrypted_text_widget = widgets.Text(
            value=decrypted_text,
            disabled=True
        )
        display(self.decrypted_text_widget)

        local_image = FileLink(image_path, result_html_prefix="Click here to download image: ")
        display(local_image)

    def display_decryption(self):
        style={'description_width' : 'initial'}
        encrypted_image = widgets.FileUpload(
            description='Upload Image',
            accept='image/*',
            multiple=False,
            style=style
        )
        display(encrypted_image)

        encryption_key = widgets.FileUpload(
            description='Upload Key',
            accept='.key',
            multiple=False,
            style=style
        )
        display(encryption_key)

        submit_button = widgets.Button(
            description='Submit',
            disabled=False,
            button_style='success',
            icon='check'
        )
        display(submit_button)

        submit_button.on_click(
            lambda *args: self.decrypt(encryption_key.value, encrypted_image.value)
        )

    def encrypt(self, raw_text: str, text_key: str, image: dict):
        input_image_file = "ImageToEncrypt.png"
        key_file = "EncryptionKey.key"
        output_image_file = "EncryptedImage.png"

        image = image[list(image.keys())[0]]["content"]
        with open(input_image_file, "wb") as f:
            f.write(image)

        encrypted_text, encrypted_image, key = encrypt(raw_text, input_image_file, KeyPart(text_key), self.cipher)
        key.export_key(key_file)
        cv2.imwrite(output_image_file, encrypted_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])

        if self.encrypted_text_widget is None:
            self.add_encryption_output(encrypted_text, output_image_file, key_file)
        else:
            self.encrypted_text_widget.value = encrypted_text

    def decrypt(self, key: dict, image: dict):
        image_file = "ImageToDecrypt.png"
        output_image_file = "DecryptedImage.png"
        key_file = "DownloadedKey.key"

        image = image[list(image.keys())[0]]["content"]
        with open(image_file, "wb") as f:
            f.write(image)

        key = key[list(key.keys())[0]]["content"]
        with open(key_file, "wb") as f:
            f.write(key)

        decrypted_message, decrypted_image = decrypt(image_file, Key.import_key(key_file), self.cipher)
        cv2.imwrite(output_image_file, decrypted_image)

        if self.decrypted_text_widget is None:
            self.add_decryption_output(decrypted_message, output_image_file)
        else:
            self.decrypted_text_widget.value = decrypted_message

