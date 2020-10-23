from copy import deepcopy

from CryptoSystem.Key import Key, KeyPart, KeyModifier

class RepeatToMessageLengthModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key, message: str):
        text_key_part = key.get_text_key()
        # Only do anything if our text key is a string
        if(text_key_part.key_type is str):
            text_key_raw = text_key_part.key
            key_len = len(text_key_raw)
            msg_len = len(message)
            len_diff = msg_len - key_len

            # If we have at least as much key as we have message
            if len_diff <= 0:
                # Performing a quick trim to make sure we have exactly
                # as much key as we have message
                new_text_key = text_key_raw[:msg_len]
            # If we don't have enough key
            else:
                key_repeats = msg_len // key_len
                partial_key_lengths = msg_len % key_len
                new_text_key = text_key_raw * key_repeats + text_key_raw[:partial_key_lengths]
            new_key_part = KeyPart(new_text_key)
            key.set_text_key(new_key_part)


class PadXToMessageLengthModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key, message: str):
        text_key_part = key.get_text_key()
        if(text_key_part.key_type is str):
            text_key_raw = text_key_part.key
            key_len = len(text_key_raw)
            msg_len = len(message)
            len_diff = msg_len - key_len

            # If we have at least as much key as we have message
            if len_diff <= 0:
                # Performing a quick trim to make sure we have exactly
                # as much key as we have message
                new_text_key = text_key_raw[:msg_len]
            # If we don't have enough key
            else:
                new_text_key = text_key_raw + "x" * len_diff
            new_key_part = KeyPart(new_text_key)
            key.set_text_key(new_key_part)


class LowercaseKeyModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key, message: str):
        text_key_part = key.get_text_key()
        if(text_key_part.key is str):
            text_key_raw = text_key_part.key
            new_key_part = KeyPart(text_key_raw.lower())
            key.set_text_key(new_key_part)


def apply_modifiers(key: Key, message: str, *modifiers: KeyModifier) -> Key:
    key_copy = deepcopy(key)
    for modifier in modifiers:
        modifier.modify_key(key_copy, message)
    return key_copy

