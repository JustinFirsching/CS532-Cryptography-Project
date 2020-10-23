from typing import Any, Tuple

import numpy as np

from CryptoSystem.Ciphers import Cipher
from CryptoSystem.Key import Key, KeyPart


class ImageCipher(Cipher):
    desired_key_type = Tuple[np.ndarray, np.ndarray]
    key_flipper = np.vectorize(lambda current_val: int(f"{current_val:b}"[::-1], 2))

    @staticmethod
    def encrypt(image: np.ndarray, key: Key) -> np.ndarray:
        row_key, col_key = map(lambda o: getattr(o, "key"), key.get_image_keys())
        reversed_row_key = ImageCipher.key_flipper(row_key)
        reversed_col_key = ImageCipher.key_flipper(col_key)
        rows, cols = image.shape[:2]

        r = image[:, :, 0]
        g = image[:, :, 1]
        b = image[:, :, 2]

        for _ in range(10):
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

            odd_row_size, even_row_size = r[1::2].shape[0], r[::2].shape[0]
            odd_col_size, even_col_size = r[:, 1::2].shape[1], r[:, ::2].shape[1]
            r[:, ::2] = np.bitwise_xor(r[:, ::2], row_key.reshape(-1, 1).repeat(even_col_size, axis=1))
            r[:, 1::2] = np.bitwise_xor(r[:, 1::2], reversed_row_key.reshape(-1, 1).repeat(odd_col_size, axis=1))
            r[1::2, :] = np.bitwise_xor(r[1::2, :], col_key.reshape(-1, 1).repeat(odd_row_size, axis=1).T)
            r[::2, :] = np.bitwise_xor(r[::2, :], reversed_col_key.reshape(-1, 1).repeat(even_row_size, axis=1).T)

        new_image = np.zeros_like(image)
        new_image[:, :, 0] = r
        new_image[:, :, 1] = g
        new_image[:, :, 2] = b
        return new_image

    @staticmethod
    def decrypt(image: np.ndarray, key: Key) -> np.ndarray:
        # This is the same as encrypting, just do it backwards
        row_key, col_key = map(lambda o: getattr(o, "key"), key.get_image_keys())
        reversed_row_key = ImageCipher.key_flipper(row_key)
        reversed_col_key = ImageCipher.key_flipper(col_key)
        rows, cols = image.shape[:2]

        r = image[:, :, 0]
        g = image[:, :, 1]
        b = image[:, :, 2]

        for _ in range(10):
            odd_row_size, even_row_size = r[1::2].shape[0], r[::2].shape[0]
            odd_col_size, even_col_size = r[:, 1::2].shape[1], r[:, ::2].shape[1]
            r[:, ::2] = np.bitwise_xor(r[:, ::2], row_key.reshape(-1, 1).repeat(even_col_size, axis=1))
            r[:, 1::2] = np.bitwise_xor(r[:, 1::2], reversed_row_key.reshape(-1, 1).repeat(odd_col_size, axis=1))
            r[1::2, :] = np.bitwise_xor(r[1::2, :], col_key.reshape(-1, 1).repeat(odd_row_size, axis=1).T)
            r[::2, :] = np.bitwise_xor(r[::2, :], reversed_col_key.reshape(-1, 1).repeat(even_row_size, axis=1).T)

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

        new_image = np.zeros_like(image)
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

