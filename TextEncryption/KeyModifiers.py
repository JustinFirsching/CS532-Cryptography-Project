from TextEncryption import Key, KeyModifier

class RepeatToMessageLengthModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key[str], message: str) -> Key:
        key_str = key.get_key()
        key_len = len(key_str)
        msg_len = len(message)
        len_diff = msg_len - key_len
        if len_diff <= 0:
            return Key(key_str[:msg_len])

        key_repeats = msg_len // key_len
        partial_key_lengths = msg_len % key_len
        return Key(key_str * key_repeats + key_str[:partial_key_lengths])


class PadXToMessageLengthModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key[str], message: str) -> Key:
        key_str = key.get_key()
        key_len = len(key_str)
        msg_len = len(message)
        len_diff = msg_len - key_len
        if len_diff <= 0:
            return Key(key[:msg_len])
        return Key(key + "x" * len_diff)


class LowercaseKeyModifier(KeyModifier):
    @staticmethod
    def modify_key(key: Key[str], message: str) -> Key:
        return Key(key.get_key().lower())


def apply_modifiers(key: Key, message: str, *modifiers: KeyModifier) -> Key:
    for modifier in modifiers:
        key = modifier.modify_key(key, message)
    return key

