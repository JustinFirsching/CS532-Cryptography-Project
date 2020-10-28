from typing import Union, Tuple

import numpy as np
from cv2 import cv2
from CryptoSystem.Ciphers import Cipher
from CryptoSystem.Ciphers.Image import ImageCipher
from CryptoSystem.Exceptions import ImageTooSmallException
from CryptoSystem.Key import Key, KeyPart
from CryptoSystem.Steganography import extract_message, get_minimum_size, embed_message


def encrypt(text: str, image: Union[str, np.ndarray], text_key: KeyPart, cipher: Cipher) -> Tuple[str, np.ndarray, Key]:
    """
    raises: ImageTooSmallException
    """
    # Text Encryption
    encrypted_text = cipher.encrypt(text, text_key)

    # Image Steganography
    if type(image) is str:
        image = cv2.imread(image, cv2.IMREAD_ANYCOLOR)

    if(get_minimum_size(encrypted_text) > image.size):
        raise ImageTooSmallException()

    embedded_message = embed_message(encrypted_text, image)

    rows, cols = embedded_message.shape[:2]
    row_key, col_key = ImageCipher.generate_key_part((rows, cols))
    key = Key(text_key, row_key, col_key)
    encrypted_image = ImageCipher.encrypt(embedded_message, key)

    return (encrypted_text, encrypted_image, key)

def decrypt(image: Union[str, np.ndarray], key: Key, cipher: Cipher) -> Tuple[str, np.ndarray]:
    if type(image) is str:
        image = cv2.imread(image, cv2.IMREAD_ANYCOLOR)

    decrypted_image = ImageCipher.decrypt(image, key)
    cv2.imwrite("DecryptedImage.png", decrypted_image)
    # Steganography Extraction
    encrypted_message = extract_message(decrypted_image)
    # Decrypted Message
    decrypted_message = cipher.decrypt(encrypted_message, key)
    return (decrypted_message, decrypted_image)

