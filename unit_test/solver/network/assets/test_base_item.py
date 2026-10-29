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
from unittest.mock import patch
from uuid import uuid4

import numpy as np

from omotes_simulator_core.solver.matrix.equation_object import EquationObject
from omotes_simulator_core.solver.matrix.index_core_quantity import (
    CoreQuantity,
    NUMBER_OF_CORE_QUANTITIES,
)
from omotes_simulator_core.solver.network.assets.base_item import BaseItem


class MockBaseItem(BaseItem):
    """Mock BaseItem class for testing."""

    def get_equations(self) -> list[EquationObject]:
        """Dummy implementation of the get_equations method for testing."""
        return []

    def disconnect_node(self, connection_point: int) -> None:
        """Dummy implementation of the disconnect_node method for testing."""


class BaseItemTest(unittest.TestCase):
    """Testcase for BaseItem class."""

    def test_init(self) -> None:
        """Test the __init__ method of the BaseItem class."""
        # arrange
        asset_name = str(uuid4())
        number_of_unknowns = 2
        number_of_connection_points = 2

        # act
        asset = MockBaseItem(
            name=asset_name,
            _id=str(uuid4()),
            number_of_unknowns=number_of_unknowns,
            number_connection_points=number_of_connection_points,
        )  # act

        # assert
        self.assertEqual(asset.name, asset_name)
        self.assertEqual(asset.number_of_unknowns, number_of_unknowns)
        self.assertEqual(asset.matrix_index, 0)

        np.testing.assert_array_equal(asset.prev_sol, np.zeros(number_of_unknowns))

    def test_set_matrix_index(self) -> None:
        """Test the set_matrix_index method of the BaseItem class."""
        # arrange
        asset_name = str(uuid4())
        number_of_unknowns = 2
        number_of_connection_points = 2
        asset = MockBaseItem(
            name=asset_name,
            _id=asset_name,
            number_of_unknowns=number_of_unknowns,
            number_connection_points=number_of_connection_points,
        )

        # act
        asset.set_matrix_index(1)  # act

        # assert
        self.assertEqual(asset.matrix_index, 1)

    def test_get_index_matrix(self) -> None:
        asset = MockBaseItem(12, "asset", "asset", 4)
        other = MockBaseItem(12, "other", "other", 4)
        for base in (0, 17, 40):
            asset.set_matrix_index(base)
            for core_quantity, offset in (
                (CoreQuantity.MASS_FLOW_RATE, 0),
                (CoreQuantity.PRESSURE, 1),
                (CoreQuantity.INTERNAL_ENERGY, 2),
            ):
                for connection in (-1, 0, 1, 2, 3, 5):
                    for relative in (True, False):
                        with self.subTest(
                            base=base,
                            core_quantity=core_quantity,
                            connection=connection,
                            relative=relative,
                        ):
                            expected = offset + 3 * connection + (0 if relative else base)
                            self.assertEqual(
                                asset.get_index_matrix(core_quantity, connection, relative),
                                expected,
                            )
                            self.assertEqual(
                                asset.get_index_matrix(
                                    core_quantity=core_quantity,
                                    connection_point=connection,
                                    use_relative_indexing=relative,
                                ),
                                expected,
                            )
            self.assertEqual(other.get_index_matrix(CoreQuantity.PRESSURE, 0, False), 1)
        asset.matrix_index = 23
        self.assertEqual(asset.get_index_matrix(CoreQuantity.PRESSURE, 1, False), 27)

    def test_get_index_matrix_uses_current_quantity_layout(self) -> None:
        asset = MockBaseItem(12, "asset", "asset", 4)
        with patch(
            "omotes_simulator_core.solver.matrix.index_core_quantity.NUMBER_OF_CORE_QUANTITIES", 5
        ):
            self.assertEqual(asset.get_index_matrix(CoreQuantity.PRESSURE, 2, True), 11)
