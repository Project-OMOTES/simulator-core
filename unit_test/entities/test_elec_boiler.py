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

"""Test ElecBoiler entities."""
import unittest
from unittest.mock import patch

from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_ELECTRICITY_CONSUMPTION,
    PROPERTY_HEAT_SUPPLIED,
    PROPERTY_HEAT_SUPPLY_SET_POINT,
)
from omotes_simulator_core.entities.assets.elec_boiler import ElecBoiler


class ElecBoilerTest(unittest.TestCase):
    """Testcase for ElecBoiler class."""

    def setUp(self) -> None:
        """Set up test case."""
        self.elec_boiler = ElecBoiler(
            asset_name="elec_boiler",
            asset_id="elec_boiler_id",
            port_ids=["test1", "test2"],
            efficiency=0.8,
        )

    def test_elec_boiler_create(self) -> None:
        """Evaluate the creation of an electric boiler object."""
        self.assertIsInstance(self.elec_boiler, ElecBoiler)
        self.assertEqual(self.elec_boiler.name, "elec_boiler")
        self.assertEqual(self.elec_boiler.asset_id, "elec_boiler_id")
        self.assertEqual(self.elec_boiler.connected_ports, ["test1", "test2"])
        self.assertEqual(self.elec_boiler.efficiency, 0.8)

    def test_elec_boiler_invalid_efficiency_defaults_to_one(self) -> None:
        """Test invalid efficiency values are reset to 1.0."""
        elec_boiler_zero = ElecBoiler(
            asset_name="elec_boiler_zero",
            asset_id="elec_boiler_zero_id",
            port_ids=["test1", "test2"],
            efficiency=0.0,
        )
        elec_boiler_above_one = ElecBoiler(
            asset_name="elec_boiler_above_one",
            asset_id="elec_boiler_above_one_id",
            port_ids=["test1", "test2"],
            efficiency=1.2,
        )

        self.assertEqual(elec_boiler_zero.efficiency, 1.0)
        self.assertEqual(elec_boiler_above_one.efficiency, 1.0)

    def test_get_electric_power_consumption(self) -> None:
        """Test getting electric power consumption of an electric boiler."""
        with patch.object(self.elec_boiler, "get_actual_heat_supplied", return_value=-2000.0):
            power_consumption = self.elec_boiler.get_electric_power_consumption()

        expected_power_consumption = abs(-2000.0) / 0.8
        self.assertEqual(power_consumption, expected_power_consumption)

    def test_write_to_output(self) -> None:
        """Test writing output of an electric boiler."""
        with (
            patch.object(self.elec_boiler.solver_asset, "get_mass_flow_rate") as get_mass_flow_rate,
            patch.object(self.elec_boiler.solver_asset, "get_pressure") as get_pressure,
            patch.object(self.elec_boiler.solver_asset, "get_temperature") as get_temperature,
            patch.object(self.elec_boiler, "get_volume_flow_rate") as get_volume_flow_rate,
        ):
            get_mass_flow_rate.return_value = 1e6
            get_pressure.return_value = 2e5
            get_temperature.return_value = 333.15
            get_volume_flow_rate.return_value = 100.0

            self.elec_boiler.write_standard_output()

        self.elec_boiler.heat_demand_set_point = -4000.0
        with (
            patch.object(self.elec_boiler, "get_actual_heat_supplied", return_value=3500.0),
            patch.object(self.elec_boiler, "get_electric_power_consumption", return_value=4375.0),
        ):
            self.elec_boiler.write_to_output()

        self.assertEqual(self.elec_boiler.outputs[1][-1][PROPERTY_HEAT_SUPPLY_SET_POINT], -4000.0)
        self.assertEqual(self.elec_boiler.outputs[1][-1][PROPERTY_HEAT_SUPPLIED], 3500.0)
        self.assertEqual(
            self.elec_boiler.outputs[1][-1][PROPERTY_ELECTRICITY_CONSUMPTION],
            4375.0,
        )
