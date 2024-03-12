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
from simulator_core.solver.network.assets.base_node_item import BaseNodeItem


class MockBaseNodeItem(BaseNodeItem):
    """Mock BaseItem class for testing."""

    def get_equations(self) -> None:
        """Dummy implementation of the get_equations method for testing."""

    def connect_asset(self, asset: BaseNodeItem, connection_point: int) -> None:
        """Dummy implementation of the connect_asset method for testing."""

    def get_connected_assets(self) -> list[tuple[BaseItem, int]]:
        """Dummy implementation of the get_connected_assets method for testing."""
        return []


class BaseItemTest(unittest.TestCase):
    """Testcase for BaseNodeItem class."""

    def test_init(self) -> None:
        """Test the __init__ method of the BaseNodeItem class."""
        # arrange
        asset_name = uuid4()
        number_of_unknowns = 2

        # act
        asset = MockBaseNodeItem(name=asset_name, number_of_unknowns=number_of_unknowns)  # act

        # assert
        self.assertEqual(asset.name, asset_name)
        self.assertEqual(asset.number_of_unknowns, number_of_unknowns)
        self.assertEqual(asset.matrix_index, 0)
        self.assertEqual(asset.prev_sol, [0.0] * number_of_unknowns)

    def test_set_matrix_index(self) -> None:
        """Test the set_matrix_index method of the BaseNodeItem class."""
        # arrange
        asset_name = uuid4()
        number_of_unknowns = 2
        asset = MockBaseNodeItem(name=asset_name, number_of_unknowns=number_of_unknowns)

        # act
        asset.set_matrix_index(1)  # act

        # assert
        self.assertEqual(asset.matrix_index, 1)
