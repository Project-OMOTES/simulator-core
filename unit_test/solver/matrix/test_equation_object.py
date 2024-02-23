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

"""Test equation object."""
import unittest

import numpy as np

from simulator_core.solver.matrix.equation_object import EquationObject


class EquationObjectTest(unittest.TestCase):
    """Test the equation object."""

    def test_init(self) -> None:
        """Test the init of the equation object."""
        # arrange

        # act
        equation_object = EquationObject()  # act

        # assert
        self.assertEqual(equation_object.coefficients.size, 0)
        self.assertEqual(equation_object.indices.size, 0)
        self.assertEqual(equation_object.rhs, 0.0)

    def test_set_coefficient(self) -> None:
        """Test the set coefficient of the equation object."""
        # arrange
        equation_object = EquationObject()

        # act
        #  to discuss is this the preferred way of setting the coefs, or should
        #  we add it to the constructor?
        equation_object.coefficients = np.array([1.0])  # act

        # assert
        self.assertEqual(equation_object.coefficients.size, 1)
        self.assertEqual(equation_object.coefficients[0], 1.0)

    def test_to_list(self) -> None:
        """Test the to list of the equation object."""
        # arrange
        equation_object = EquationObject()
        equation_object.coefficients = np.array([1.0])
        equation_object.indices = np.array([1])

        # act
        result = equation_object.to_list(2)

        # assert
        self.assertEqual(result, [0.0, 1.0])

    def test_to_list_error(self) -> None:
        """Test the to list of the equation object."""
        # arrange
        equation_object = EquationObject()
        equation_object.coefficients = np.array([1.0, 2.0])
        equation_object.indices = np.array([1, 2])
        length = 1

        # act
        with self.assertRaises(IndexError) as cm:
            equation_object.to_list(length)

        # assert
        self.assertIsInstance(cm.exception, IndexError)
        self.assertEqual(
            str(cm.exception),
            (f"Length of {length} smaller than the available number "
             f"of coefficients {len(equation_object.coefficients)}!")
        )
