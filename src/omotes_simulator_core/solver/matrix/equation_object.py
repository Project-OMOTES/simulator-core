#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Module containing class to store equations."""
import numpy as np


class EquationObject:
    """Class to store equation objects.

    Indices are the location in the matrix of the coefficients
    rhs is the rhs of the matrix.
    """

    indices: np.ndarray
    """Indices of the coefficients in the matrix."""

    coefficients: np.ndarray
    """Coefficients of the equation."""

    rhs: float
    """Right hand side of the equation."""

    def __init__(self) -> None:
        """Constructor of the EquationObject."""
        self.indices = np.array([], dtype=int)
        self.coefficients = np.array([], dtype=float)
        self.rhs = 0.0

    def __len__(self) -> int:
        """Return the number of coefficients in this equation."""
        return len(self.coefficients)

    def to_list(self, length: int) -> list[float]:
        """Method to change the equation object to list which can be stored in the matrix.

        The method creates a list with zero of the length given in the input.
        At the indices of the class the coefficients of the class are stored.
        :param int length: Length of the list to be returned
        :return: a list of the coefficient which can be used in the matrix.
        """
        if length < len(self.indices):
            raise IndexError(
                f"Length of {length} smaller than the available number "
                f"of coefficients {len(self.coefficients)}!"
            )

        coefficient_list: list[float] = [0.0] * length
        for col, coefficient in zip(self.indices, self.coefficients):
            coefficient_list[col] = coefficient
        return coefficient_list
