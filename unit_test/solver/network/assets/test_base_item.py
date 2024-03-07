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

"""Test BaseItem asset of the solver class."""
import unittest
from uuid import uuid4

from simulator_core.solver.network.assets.base_item import BaseItem


class MockBaseItem(BaseItem):
    """Mock BaseItem class for testing."""

    def get_equations(self) -> None:
        """Dummy implementation of the get_equations method for testing."""

    def disconnect_node(self, connection_point: int) -> None:
        """Dummy implementation of the disconnect_node method for testing."""


class BaseItemTest(unittest.TestCase):
    """Testcase for BaseItem class."""

    def test_init(self) -> None:
        """Test the __init__ method of the BaseItem class."""
        # arrange
        asset_name = uuid4()
        number_of_unknowns = 2
        number_of_connection_points = 2

        # act
        asset = MockBaseItem(
            name=asset_name,
            number_of_unknowns=number_of_unknowns,
            number_connection_points=number_of_connection_points,
        )  # act

        # assert
        self.assertEqual(asset.name, asset_name)
        self.assertEqual(asset.number_of_unknowns, number_of_unknowns)
        self.assertEqual(asset.matrix_index, 0)
        self.assertEqual(asset.prev_sol, [0.0] * number_of_unknowns)

    def test_set_matrix_index(self) -> None:
        """Test the set_matrix_index method of the BaseItem class."""
        # arrange
        asset_name = uuid4()
        number_of_unknowns = 2
        number_of_connection_points = 2
        asset = MockBaseItem(
            name=asset_name,
            number_of_unknowns=number_of_unknowns,
            number_connection_points=number_of_connection_points,
        )

        # act
        asset.set_matrix_index(1)  # act

        # assert
        self.assertEqual(asset.matrix_index, 1)
