#  Copyright (c) 2026. Deltares & TNO
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

"""Test GasHeater entities."""
import unittest
from unittest.mock import patch

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_GAS_ENERGY_CONTENT,
    PROPERTY_GAS_CONSUMPTION,
    PROPERTY_HEAT_SUPPLIED,
    PROPERTY_HEAT_SUPPLY_SET_POINT,
)
from omotes_simulator_core.entities.assets.gas_heater import GasHeater


class GasHeaterTest(unittest.TestCase):
    """Testcase for GasHeater class."""

    def setUp(self) -> None:
        """Set up test case."""
        self.gas_heater = GasHeater(
            asset_name="gas_heater",
            asset_id="gas_heater_id",
            port_ids=["test1", "test2"],
            efficiency=0.9,
        )

    def test_gas_heater_create(self) -> None:
        """Evaluate the creation of a gas heater object."""
        self.assertIsInstance(self.gas_heater, GasHeater)
        self.assertEqual(self.gas_heater.name, "gas_heater")
        self.assertEqual(self.gas_heater.asset_id, "gas_heater_id")
        self.assertEqual(self.gas_heater.connected_ports, ["test1", "test2"])
        self.assertEqual(self.gas_heater.efficiency, 0.9)

    def test_gas_heater_invalid_efficiency_defaults_to_one(self) -> None:
        """Test invalid efficiency values are reset to 1.0."""
        gas_heater_zero = GasHeater(
            asset_name="gas_heater_zero",
            asset_id="gas_heater_zero_id",
            port_ids=["test1", "test2"],
            efficiency=0.0,
        )
        gas_heater_above_one = GasHeater(
            asset_name="gas_heater_above_one",
            asset_id="gas_heater_above_one_id",
            port_ids=["test1", "test2"],
            efficiency=1.1,
        )

        self.assertEqual(gas_heater_zero.efficiency, 1.0)
        self.assertEqual(gas_heater_above_one.efficiency, 1.0)

    def test_get_gas_consumption(self) -> None:
        """Test getting gas consumption of a gas heater."""
        with patch.object(self.gas_heater, "get_actual_heat_supplied", return_value=-1.0e6):
            gas_consumption = self.gas_heater.get_gas_consumption()

        expected_gas_consumption = abs(-1.0e6) / DEFAULT_GAS_ENERGY_CONTENT / 0.9
        self.assertEqual(gas_consumption, expected_gas_consumption)

    def test_write_to_output(self) -> None:
        """Test writing output of a gas heater."""
        with (
            patch.object(self.gas_heater.solver_asset, "get_mass_flow_rate") as get_mass_flow_rate,
            patch.object(self.gas_heater.solver_asset, "get_pressure") as get_pressure,
            patch.object(self.gas_heater.solver_asset, "get_temperature") as get_temperature,
            patch.object(self.gas_heater, "get_volume_flow_rate") as get_volume_flow_rate,
        ):
            get_mass_flow_rate.return_value = 1e6
            get_pressure.return_value = 2e5
            get_temperature.return_value = 333.15
            get_volume_flow_rate.return_value = 100.0

            self.gas_heater.write_standard_output()

        self.gas_heater.heat_demand_set_point = -2.5e6
        with (
            patch.object(self.gas_heater, "get_actual_heat_supplied", return_value=2.0e6),
            patch.object(self.gas_heater, "get_gas_consumption", return_value=0.1),
        ):
            self.gas_heater.write_to_output()

        self.assertEqual(
            self.gas_heater.outputs[1][-1][PROPERTY_HEAT_SUPPLY_SET_POINT],
            -2.5e6,
        )
        self.assertEqual(self.gas_heater.outputs[1][-1][PROPERTY_HEAT_SUPPLIED], 2.0e6)
        self.assertEqual(self.gas_heater.outputs[1][-1][PROPERTY_GAS_CONSUMPTION], 0.1)
