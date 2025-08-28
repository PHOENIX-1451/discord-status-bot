
class AuthorisationMapping:

    # Characters to be used when generating a token
    VALID_CHARS = [
        # Uppercase characters
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",

        # Lowercase characters
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",

        # Integers
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",

        # Special characters
        "!", "@", "#", "$", "%", "^", "&", "*", "_", "-", "+", "="
    ]

    # Characters to be used when computing checksum
    CHECKSUM_CHARS = [
        # Uppercase characters
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",

        # Lowercase characters
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",

        # Integers
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]

    # Length of timestamp when encoded to base62
    TIME_ENCODING_LENGTH = 6