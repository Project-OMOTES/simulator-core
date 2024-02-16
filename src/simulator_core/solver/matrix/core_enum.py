from enum import IntEnum

NUMBER_CORE_QUANTITIES = 3


class IndexEnum(IntEnum):
    """Enum for the index of the matrix."""
    discharge = 0
    pressure = 1
    internal_energy = 2
