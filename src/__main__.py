import sys

from enum import Enum
from TextEncryption import Cipher
from TextEncryption import Key


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
    pass

def get_text() -> str:
    pass

def get_key(cipher: Cipher) -> Key:
    pass

def run_encryption():
    pass

def run_decryption():
    pass

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


main()
