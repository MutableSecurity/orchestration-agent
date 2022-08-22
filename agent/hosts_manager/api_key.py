import random


def generate_random_key(alphabet: str, length: int) -> str:
    return "".join(
        random.choice(alphabet) for _ in range(length)  # noqa: S311
    )


def has_key_valid_format(key: str, alphabet: str, length: int) -> bool:
    if len(key) != length:
        return False

    for char in key:
        if char not in alphabet:
            return False

    return True
