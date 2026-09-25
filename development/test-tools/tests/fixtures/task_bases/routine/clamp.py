"""Routine clamp fixture with exactly one deliberate above-high defect."""


def clamp(value: int, low: int, high: int) -> int:
    if low > high:
        raise ValueError("low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return value
    return value
