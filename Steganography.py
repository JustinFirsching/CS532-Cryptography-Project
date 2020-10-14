from copy import deepcopy
from math import ceil, sqrt
from typing import Tuple

import numpy as np
import cv2


_COUNT_SIZE = 24

def get_minimum_size(message: str) -> int:
    """
    We have three color channels to embed the entire message in at 8 bits per
    character, while accounting for _COUNT_SIZE bits to indiciate the message
    length
    """
    return ceil((len(message) * 8 + _COUNT_SIZE) / 3)

def get_square_dimensions(size_needed: int) -> Tuple[int, int]:
    dims = ceil(sqrt(size_needed))
    return (dims, dims)

def get_random_image(height: int, width: int) -> np.ndarray:
    return np.random.normal(128, 16, (height, width, 3)).astype(np.uint8)

def valid_image_size(image: np.ndarray, needed_size: int) -> bool:
    return np.prod(image.shape) >= needed_size

def message_to_bits(message: str, sep: str = '') -> str:
    return sep.join(f"{ord(m):08b}" for m in message)

def embed_message(message: str, image: np.ndarray) -> np.ndarray:
    output = deepcopy(image)
    embed_message_in_place(message, output)
    return output

def embed_message_in_place(message: str, image: np.ndarray):
    message_bits = message_to_bits(message)
    message_to_embed = f"{len(message_bits):0{_COUNT_SIZE}b}{message_bits}"
    current_bit_idx = 0
    pass
    for i in range(image.shape[0]):
        row = image[i]
        for j in range(image.shape[1]):
            pixel = row[j]
            for k in range(image.shape[2]):
                channel = pixel[k]
                image[i, j, k] = channel & ~1 | int(message_to_embed[current_bit_idx])
                current_bit_idx += 1

                # This means the message is completely embedded
                if current_bit_idx == len(message_to_embed):
                    return

def extract_message(image: np.ndarray) -> str:
    values = image.reshape(np.prod(image.shape))
    counting_bits = [v & 1 for v in values[:_COUNT_SIZE]]
    bits_to_extract = int(''.join(map(str, counting_bits)), 2)
    message_bits = [v & 1 for v in values[_COUNT_SIZE:bits_to_extract + _COUNT_SIZE]]
    characters = [chr(int(''.join(map(str, message_bits[c: c+8])), 2)) for c in range(0, len(message_bits), 8)]
    return "".join(characters)

