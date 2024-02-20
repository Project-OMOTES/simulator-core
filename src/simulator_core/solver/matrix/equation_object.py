"""Module containing class to store equations."""
import numpy as np


class EquationObject:
    """Class to store equation objects.

    Indices are the location in the matrix of the coefficients
    rhs is the rhs of the matrix.
    """

    def __init__(self) -> None:
        """Constructor of the EquationObject."""
        self.indices = np.array([], dtype=int)
        self.coefficients = np.array([], dtype=float)
        self.rhs = 0.0

    def to_list(self, length: int) -> list[float]:
        """Method to change the equation object to list which can be stored in the matrix.

        The method creates a list with zero of the length given in the input.
        At the indices of the class the coefficients of the class are stored.
        :param int length: Length of the list to be returned
        :return: a list of the coefficient which can be used in the matrix.
        """
        coefficient_list: list[float] = [0.0] * length
        for col, coefficient in zip(self.indices, self.coefficients):
            coefficient_list[col] = coefficient
        return coefficient_list
