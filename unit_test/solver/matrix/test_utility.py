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

"""Test matrix utility functions."""
import unittest
from simulator_core.solver.matrix.utility import relative_difference, absolute_difference


class MatrixUtilityTest(unittest.TestCase):
    """Test the matrix utility functions."""

    def test_relative_difference(self):
        """Test the relative difference function."""
        # arrange
        value_1 = 1.0
        value_2 = 2.0

        # act
        result = relative_difference(value_1, value_2)

        # assert
        self.assertEqual(result, 0.5)

    def test_relative_difference_flippes(self):
        """Test the relative difference function."""
        # arrange
        value_1 = 2.0
        value_2 = 1.0

        # act
        result = relative_difference(value_1, value_2)

        # assert
        self.assertEqual(result, 0.5)

    def test_relative_difference_zero(self):
        """Test the relative difference function with zero."""
        # arrange
        value_1 = 1.0
        value_2 = 1.0

        # act
        result = relative_difference(value_1, value_2)

        # assert
        self.assertEqual(result, 0.0)

    def test_relative_difference_negative(self):
        """Test the relative difference function with zero."""
        # arrange
        value_1 = 1.0
        value_2 = -2.0

        # act
        result = relative_difference(value_1, value_2)

        # assert
        self.assertEqual(result, 1.5)

    def test_absolute_difference(self):
        """Test the absolute difference function."""
        # arrange
        value_1 = 1.0
        value_2 = 2.0

        # act
        result = absolute_difference(value_1, value_2)

        # assert
        self.assertEqual(result, 1.0)
