"""Fully correct parse_numbers fixture for the heavy base."""


def parse_numbers(text: str) -> list[int]:
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    tokens = [token.strip() for token in text.split(",")]
    if not tokens or any(not token for token in tokens):
        raise ValueError("input must contain comma-separated integers")
    values: list[int] = []
    for token in tokens:
        try:
            values.append(int(token))
        except ValueError:
            raise ValueError("each token must be an integer") from None
    return values
