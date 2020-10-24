from typing import Any, Tuple

import numpy as np

from CryptoSystem.Ciphers import Cipher
from CryptoSystem.Key import Key, KeyPart


def vector_to_image(one_d: np.ndarray, repeat_len: int) -> np.ndarray:
    if len(one_d.shape) == 1:
        vector = one_d.reshape(-1, 1)
    else:
        vector = one_d
    return vector.reshape(-1, 1, 1).repeat(repeat_len, axis=1).repeat(3, axis=2)


class ImageCipher(Cipher):
    desired_key_type = Tuple[np.ndarray, np.ndarray]
    key_flipper = np.vectorize(lambda current_val: int(f"{current_val:b}"[::-1], 2))

    @staticmethod
    def encrypt(image: np.ndarray, key: Key, iterations: int = 10) -> np.ndarray:
        row_key, col_key = map(lambda o: getattr(o, "key"), key.get_image_keys())
        reversed_row_key = ImageCipher.key_flipper(row_key)
        reversed_col_key = ImageCipher.key_flipper(col_key)
        rows, cols = image.shape[:2]

        new_image = np.copy(image)

        for _ in range(iterations):
            r = new_image[:, :, 0]
            g = new_image[:, :, 1]
            b = new_image[:, :, 2]

            row_r_mod = np.sum(r, axis=1) % 2
            row_g_mod = np.sum(g, axis=1) % 2
            row_b_mod = np.sum(b, axis=1) % 2

            for i in range(rows):
                r[i] = np.roll(r[i], (2 * int(row_r_mod[i] == 0) - 1) * row_key[i])
                g[i] = np.roll(g[i], (2 * int(row_g_mod[i] == 0) - 1) * row_key[i])
                b[i] = np.roll(b[i], (2 * int(row_b_mod[i] == 0) - 1) * row_key[i])

            col_r_mod = np.sum(r, axis=0) % 2
            col_g_mod = np.sum(g, axis=0) % 2
            col_b_mod = np.sum(b, axis=0) % 2

            for i in range(cols):
                r[:, i] = np.roll(r[:, i], (2 * int(col_r_mod[i] == 1) - 1) * col_key[i])
                g[:, i] = np.roll(g[:, i], (2 * int(col_g_mod[i] == 1) - 1) * col_key[i])
                b[:, i] = np.roll(b[:, i], (2 * int(col_b_mod[i] == 1) - 1) * col_key[i])

            new_image[:, :, 0] = r
            new_image[:, :, 1] = g
            new_image[:, :, 2] = b

            odd_row_size, even_row_size = r[1::2].shape[0], r[::2].shape[0]
            odd_col_size, even_col_size = r[:, 1::2].shape[1], r[:, ::2].shape[1]
            new_image[:, ::2] = np.bitwise_xor(new_image[:, ::2], vector_to_image(row_key, even_col_size))
            new_image[:, 1::2] = np.bitwise_xor(new_image[:, 1::2], vector_to_image(reversed_row_key, odd_col_size))
            new_image[1::2, :] = np.bitwise_xor(new_image[1::2, :], np.transpose(vector_to_image(col_key, odd_row_size), (1, 0, 2)))
            new_image[::2, :] = np.bitwise_xor(new_image[::2, :], np.transpose(vector_to_image(reversed_col_key, even_row_size), (1, 0, 2)))

        return new_image

    @staticmethod
    def decrypt(image: np.ndarray, key: Key, iterations: int = 10) -> np.ndarray:
        # This is the same as encrypting, just do it backwards
        row_key, col_key = map(lambda o: getattr(o, "key"), key.get_image_keys())
        reversed_row_key = ImageCipher.key_flipper(row_key)
        reversed_col_key = ImageCipher.key_flipper(col_key)
        rows, cols = image.shape[:2]

        new_image = np.copy(image)


        for _ in range(iterations):
            r = new_image[:, :, 0]
            g = new_image[:, :, 1]
            b = new_image[:, :, 2]

            odd_row_size, even_row_size = r[1::2].shape[0], r[::2].shape[0]
            odd_col_size, even_col_size = r[:, 1::2].shape[1], r[:, ::2].shape[1]
            new_image[:, ::2] = np.bitwise_xor(new_image[:, ::2], vector_to_image(row_key, even_col_size))
            new_image[:, 1::2] = np.bitwise_xor(new_image[:, 1::2], vector_to_image(reversed_row_key, odd_col_size))
            new_image[1::2, :] = np.bitwise_xor(new_image[1::2, :], np.transpose(vector_to_image(col_key, odd_row_size), (1, 0, 2)))
            new_image[::2, :] = np.bitwise_xor(new_image[::2, :], np.transpose(vector_to_image(reversed_col_key, even_row_size), (1, 0, 2)))

            col_r_mod = np.sum(r, axis=0) % 2
            col_g_mod = np.sum(g, axis=0) % 2
            col_b_mod = np.sum(b, axis=0) % 2

            for i in range(cols):
                r[:, i] = np.roll(r[:, i], (2 * int(col_r_mod[i] == 0) - 1) * col_key[i])
                g[:, i] = np.roll(g[:, i], (2 * int(col_g_mod[i] == 0) - 1) * col_key[i])
                b[:, i] = np.roll(b[:, i], (2 * int(col_b_mod[i] == 0) - 1) * col_key[i])

            row_r_mod = np.sum(r, axis=1) % 2
            row_g_mod = np.sum(g, axis=1) % 2
            row_b_mod = np.sum(b, axis=1) % 2

            for i in range(rows):
                r[i] = np.roll(r[i], (2 * int(row_r_mod[i] == 1) - 1) * row_key[i])
                g[i] = np.roll(g[i], (2 * int(row_g_mod[i] == 1) - 1) * row_key[i])
                b[i] = np.roll(b[i], (2 * int(row_b_mod[i] == 1) - 1) * row_key[i])

            new_image[:, :, 0] = r
            new_image[:, :, 1] = g
            new_image[:, :, 2] = b

        return new_image


    @staticmethod
    def generate_key_part(key_size: Tuple[int, int]) -> Tuple[KeyPart, KeyPart]:
        alpha = 10  # 2**alpha = maximum shift
        key1 = np.random.randint(0, 2 ** alpha, key_size[0], dtype=np.dtype(int))
        key2 = np.random.randint(0, 2 ** alpha, key_size[1], dtype=np.dtype(int))
        return KeyPart(key1), KeyPart(key2)

