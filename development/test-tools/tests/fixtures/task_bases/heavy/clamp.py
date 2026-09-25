"""Fully correct clamp fixture for the heavy base."""


def clamp(value: int, low: int, high: int) -> int:
    if low > high:
        raise ValueError("low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value
