from math import ceil, sqrt
from typing import Tuple

import numpy as np

def get_minimum_size(message: str) -> int:
    # message length * 8 bits per character / 3 color channels to embed in, rounded up
    return ceil(len(message) * 8 / 3)


def get_square_dimensions(message: str) -> Tuple[int, int]:
    dimensions_product = get_minimum_size(message)
    dims = ceil(sqrt(dimensions_product))
    return (dims, dims)


def get_random_image(height: int, width: int) -> np.ndarray:
    return np.random.randint(0, 255, (height, width, 3))

