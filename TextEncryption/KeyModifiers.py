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

        key_repeats = len_diff // msg_len
        partial_key_lengths = len_diff % msg_len

        additional_key_data = key_str * key_repeats + key_str[:partial_key_lengths]
        return Key(key_str + additional_key_data)


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

