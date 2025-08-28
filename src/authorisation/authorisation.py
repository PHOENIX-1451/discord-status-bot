import time
import random as rnd
import re

from src.authorisation.authorisation_mapping import AuthorisationMapping
from src.singleton import SingletonMeta


class Authorisation(metaclass = SingletonMeta):

    @classmethod
    def rand_chars(cls, chars: list[str], length: int) -> str:
        # Variable to store sequence of random characters
        rand_chars = ""

        # Generate random characters
        for i in range(length):
            rand_chars += rnd.choice(chars)

        # Return sequence
        return rand_chars

    @classmethod
    def compute_checksum(cls, code: str) -> str:
        total = 0

        # Luhn's algorithm
        for i, char in enumerate(code):
            val = cls.char_value(char)
            total += val if i % 2 == 0 else val * 2

        # Return checksum
        return AuthorisationMapping.CHECKSUM_CHARS[total % len(AuthorisationMapping.CHECKSUM_CHARS)]

    @classmethod
    def char_value(cls, char: str) -> int:
        try:
            # Find and return index of specified character
            return AuthorisationMapping.VALID_CHARS.index(char)
        except ValueError:
            # Character not found
            return 0

    @classmethod
    def encode_timestamp(cls, timestamp: int, length: int) -> str:
        # Prevent errors
        if timestamp < 0: timestamp = 0
        encoded = ""

        # Encode timestamp
        temp_timestamp = timestamp
        for _ in range(length):
            encoded = AuthorisationMapping.CHECKSUM_CHARS[temp_timestamp % len(AuthorisationMapping.CHECKSUM_CHARS)] + encoded
            temp_timestamp //= len(AuthorisationMapping.CHECKSUM_CHARS)

        # Return encoded timestamp
        return encoded

    @classmethod
    def decode_timestamp(cls, encoded_timestamp: str) -> int:
        timestamp = 0

        # Decode timestamp
        for char in encoded_timestamp:
            try:
                char_index = AuthorisationMapping.CHECKSUM_CHARS.index(char)
            except ValueError:
                # Invalid character found
                return -1
            timestamp = timestamp * len(AuthorisationMapping.CHECKSUM_CHARS) + char_index
        return timestamp

    @classmethod
    def generate_authcode(cls, expiration: int) -> str:
        # Get current timestamp (UNIX)
        start_time = int(time.time())
        expiration_time = start_time + expiration
        # Length of encoded timestamp (future proofing)

        # Part 1: 5 random characters
        part1 = cls.rand_chars(AuthorisationMapping.VALID_CHARS, 5)
        # B / b
        b1 = cls.rand_chars(["B", "b"], 1)

        # Part 2: encoded time (+ filler if necessary)
        part2_length = rnd.randint(AuthorisationMapping.TIME_ENCODING_LENGTH, 8)
        encoded_time = cls.encode_timestamp(expiration_time, AuthorisationMapping.TIME_ENCODING_LENGTH)
        filler = cls.rand_chars(AuthorisationMapping.VALID_CHARS, part2_length - AuthorisationMapping.TIME_ENCODING_LENGTH)
        part2 = encoded_time + filler

        # O / o
        o1 = cls.rand_chars(["O", "o"], 1)
        # Part 3: Random characters of random length
        part3 = cls.rand_chars(AuthorisationMapping.VALID_CHARS, rnd.randint(3, 12))
        # B / b
        b2 = cls.rand_chars(["B", "b"], 1)
        # Part 4: 5 random characters
        part4 = cls.rand_chars(AuthorisationMapping.VALID_CHARS, 5)

        # Compute checksum
        encoded_string = part1 + b1 + part2 + o1 + part3 + b2 + part4
        checksum = cls.compute_checksum(encoded_string)

        # Return encoded token
        return encoded_string + checksum

    @classmethod
    def authenticate(cls, code: str) -> bool:
        # Calculate minimum length of part 2 (encoded timestamp + filler if necessary)
        min_part2_length = max(2, AuthorisationMapping.TIME_ENCODING_LENGTH)

        # Define RegEx pattern
        pattern = re.compile(
            r'^' +
            r'([A-Za-z0-9!@#$%^&*_\-+=]{5})' +
            r'([bB])' +
            rf'([A-Za-z0-9!@#$%^&*_\-+=]{{{min_part2_length},8}})' +
            r'([oO])' +
            r'([A-Za-z0-9!@#$%^&*_\-+=]{3,12})' +
            r'([bB])' +
            r'([A-Za-z0-9!@#$%^&*_\-+=]{5})' +
            r'([A-Za-z0-9])' +
            r'$'
        )

        # Check whether the provided code matches the pattern
        match = pattern.match(code)
        if not match:
            # Invalid code provided
            return False

        # Check individual groups
        part1, b1, part2, o, part3, b2, part4, given_checksum = match.groups()
        raw_code = part1 + b1 + part2 + o + part3 + b2 + part4
        # Compute checksum
        expected_checksum = cls.compute_checksum(raw_code)

        # Check whether the computed checksum matches the provided checksum
        if given_checksum != expected_checksum:
            # Invalid code provided
            return False

        # Check length of Part 2
        if len(part2) < AuthorisationMapping.TIME_ENCODING_LENGTH:
            # Invalid code provided
            return False

        # Timestamp validation
        encoded_expiration = part2[:AuthorisationMapping.TIME_ENCODING_LENGTH]
        expiration_time = cls.decode_timestamp(encoded_expiration)

        if expiration_time == -1:
            # Invalid code provided
            return False

        # Check whether token expired
        current_time = int(time.time())
        if current_time > expiration_time:
            # Invalid code provided
            return False

        # Valid token: Follows the pattern and has not yet expired
        return True