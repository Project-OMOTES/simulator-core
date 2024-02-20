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

"""Test Junction entities."""
import unittest
from unittest.mock import Mock
from uuid import uuid4

from simulator_core.solver.matrix.core_enum import NUMBER_CORE_QUANTITIES, IndexEnum
from simulator_core.solver.network.assets.Node import Node
from simulator_core.solver.network.assets.ProductionAsset import ProductionAsset


class ProductionAssetTest(unittest.TestCase):
    """Testcase for ProductionAsset class."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a ProductionAsset object
        self.asset = ProductionAsset(
            name=uuid4(),
        )
        # Create supply, connection_point:0 and return node, connection_point:1
        self.supply_node = Node(name=uuid4())
        self.return_node = Node(name=uuid4())
        # Connect the nodes to the asset
        self.asset.connect_node(node=self.supply_node, connection_point=0)
        self.asset.connect_node(node=self.return_node, connection_point=1)

    # TODO: Implement verification of the equation types.
    def test_production_asset_get_equations(self) -> None:
        """Evaluate the get_equations method."""
        # Arrange
        # Act
        equations = self.asset.get_equations()
        # Assert
        assert len(equations) == self.asset.number_of_unknowns

    # TODO: Verify why the coefficients are calculated with -1.0 + 2 * connection_point?
    def test_pre_scribe_mass_flow(self) -> None:
        """Test the pre_scribe_mass_flow attribute."""
        # Arrange
        self.asset.pre_scribe_mass_flow = True
        self.asset.mass_flow_rate_set_point = 20.0

        # Act
        equation_object = self.asset.add_pre_scribe_equation(connection_point=1)

        # Assert
        assert self.asset.pre_scribe_mass_flow is True
        assert self.asset.mass_flow_rate_set_point == 20.0
        assert equation_object.rhs == 20.0
