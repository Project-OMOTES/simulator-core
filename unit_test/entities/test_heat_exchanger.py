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

"""Test HeatExchanger entities."""
import unittest

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_POWER_PRIMARY,
    PROPERTY_HEAT_POWER_SECONDARY,
)
from omotes_simulator_core.entities.assets.heat_exchanger import HeatExchanger


class HeatExchangerTest(unittest.TestCase):
    """Testcase for HeatExchanger class."""

    def setUp(self) -> None:
        """Define the variables used in the tests."""
        self.temperature_in_primary: float = 273.15 + 10.0
        self.temperature_out_primary: float = 273.15 + 20.0
        self.temperature_in_secondary: float = 273.15 + 15.0
        self.temperature_out_secondary: float = 273.15 + 25.0
        self.mass_flow_primary: float = 1.0
        self.mass_flow_secondary: float = 1.5
        self.heat_transfer_efficiency: float = 1 / 5.0
        self.control_mass_flow_secondary: bool = False

        self.heat_exchanger = HeatExchanger(
            asset_name="heat_exchanger",
            asset_id="heat_exchanger_id",
            heat_transfer_efficiency=self.heat_transfer_efficiency,
            connected_ports=["primary_in", "primary_out", "secondary_in", "secondary_out"],
        )

        # Set properties of the solver asset
        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = 5.0
        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 2.0

        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = 10.0

        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = 15.0
        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 1.0

        self.heat_exchanger.solver_asset.prev_sol[
            self.heat_exchanger.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = 20.0

    def test_write_to_output(self):
        """Test the write_to_output method."""
        # Arrange
        self.heat_exchanger.write_standard_output()

        # Act
        self.heat_exchanger.write_to_output()

        # Assert
        self.assertEqual(self.heat_exchanger.outputs[1][-1][PROPERTY_HEAT_POWER_PRIMARY], 10.0)
        self.assertEqual(self.heat_exchanger.outputs[0][-1][PROPERTY_HEAT_POWER_SECONDARY], 5.0)
