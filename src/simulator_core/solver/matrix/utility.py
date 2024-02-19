"""module containing utility functions for the matrix."""


def relative_difference(value_1: float, value_2: float) -> float:
    """Calculates the relative difference between two points.

    :param value_1: first value to be used
    :param value_2: second value to be used
    :return: Relative difference, return 0 when the difference is 0.
    """
    diff = absolute_difference(value_1, value_2)
    if diff > 0.0:
        return diff / max(abs(value_1), abs(value_2))
    return 0.0


def absolute_difference(value_1: float, value_2: float) -> float:
    """Calculates the absolute difference between two points.

    :param value_1: first value to be used
    :param value_2: second value to be used
    :return: Absolute difference between value 1 and 2
    """
    return abs(value_1 - value_2)
