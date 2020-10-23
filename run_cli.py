import sys

from enum import Enum

from cv2 import cv2

from CryptoSystem.ui import CLIEncrypter, CLIDecrypter
from CryptoSystem.Strategy import encrypt, decrypt

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


def main():
    loop = True
    while(loop):
        method = get_targeted_event()
        if method is Capability.ENCRYPT:
            text, image_data, text_key, cipher = CLIEncrypter().get_data()
            encrypted_message, encrypted_image, key = encrypt(text, image_data, text_key, cipher)
            key.export_key("EncryptionKey.key")
            cv2.imwrite("EncryptedImage.png", encrypted_image)
            print(f"Encrypted Message: {encrypted_message}")
            print(f"Encrypted image saved to EncryptedImage.png")
            print(f"Encryption key saved to EncryptionKey.key")
        else:
            image_data, key, cipher = CLIDecrypter().get_data()
            decrypted_message, decrypted_image = decrypt(key, image_data, cipher)
            cv2.imwrite("DecryptedImage.png", decrypted_image)
            print(f"Decrypted Message: {decrypted_message}")
            print("Image saved to DecryptedImage.png")

        loop_input = input("Do you want to run again? [y/N] ")
        loop = loop_input.lower() in ["y", "yes"]


if __name__ == "__main__":
    main()
