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

"""Test HeatPump entities."""
import unittest
from unittest.mock import patch

from omotes_simulator_core.entities.assets.asset_defaults import (
    PRIMARY,
    PROPERTY_ELECTRICITY_CONSUMPTION,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HEAT_POWER_PRIMARY,
    PROPERTY_HEAT_POWER_SECONDARY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    SECONDARY,
)
from omotes_simulator_core.entities.assets.heat_pump import HeatPump


class HeatPumpTest(unittest.TestCase):
    """Testcase for HeatPump class."""

    def setUp(self) -> None:
        """Define the variables used in the tests."""
        self.temperature_in_primary: float = 273.15 + 10.0
        self.temperature_out_primary: float = 273.15 + 20.0
        self.temperature_in_secondary: float = 273.15 + 15.0
        self.temperature_out_secondary: float = 273.15 + 25.0
        self.mass_flow_primary: float = 1.0
        self.mass_flow_secondary: float = 1.5
        self.coefficient_of_performance: float = 5.0
        self.control_mass_flow_secondary: bool = False

        self.heat_pump = HeatPump(
            asset_name="heat_pump",
            asset_id="heat_pump_id",
            coefficient_of_performance=self.coefficient_of_performance,
            connected_ports=["primary_in", "primary_out", "secondary_in", "secondary_out"],
        )

        # Set properties of the solver asset
        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=0, use_relative_indexing=False
            )
        ] = 5.0
        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=0, use_relative_indexing=False
            )
        ] = 2.0

        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=1, use_relative_indexing=False
            )
        ] = 10.0

        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=2, use_relative_indexing=False
            )
        ] = 15.0
        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="mass_flow_rate", connection_point=2, use_relative_indexing=False
            )
        ] = 1.0

        self.heat_pump.solver_asset.prev_sol[
            self.heat_pump.solver_asset.get_index_matrix(
                property_name="internal_energy", connection_point=3, use_relative_indexing=False
            )
        ] = 20.0

    def test_set_setpoints_secondary(self):
        setpoints = {
            SECONDARY + PROPERTY_TEMPERATURE_IN: 273.15 + 15.0,
            SECONDARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 25.0,
            SECONDARY + PROPERTY_HEAT_DEMAND: 310,
            PROPERTY_SET_PRESSURE: 1.5,
        }

        with patch(
            "omotes_simulator_core.entities.assets.heat_pump."
            "heat_demand_and_temperature_to_mass_flow",
            return_value=321.0,
        ) as mock_calc:
            self.heat_pump._set_setpoints_secondary(setpoints)

            # Self attributes
            self.assertEqual(self.heat_pump.temperature_in_secondary, 273.15 + 15.0)
            self.assertEqual(self.heat_pump.temperature_out_secondary, 273.15 + 25.0)
            self.assertEqual(self.heat_pump.mass_flow_secondary, 321.0)
            # self.assertEqual(self.heat_pump.control_mass_flow_secondary, 1.5)

            # Solver asset attributes
            self.assertEqual(self.heat_pump.solver_asset.temperature_in_secondary, 273.15 + 15.0)
            self.assertEqual(self.heat_pump.solver_asset.temperature_out_secondary, 273.15 + 25.0)
            self.assertEqual(self.heat_pump.solver_asset.mass_flow_rate_secondary, 321.0)
            # self.assertEqual(self.heat_pump.solver_asset.pre_scribe_mass_flow_secondary, 1.5)

            mock_calc.assert_called_once_with(
                thermal_demand=310, temperature_in=273.15 + 15.0, temperature_out=273.15 + 25.0
            )

    def test_set_setpoints_secondary_missing_key(self):
        base_setpoints = {
            PROPERTY_TEMPERATURE_IN: 273.15 + 15.0,
            PROPERTY_TEMPERATURE_OUT: 273.15 + 25.0,
            PROPERTY_HEAT_DEMAND: 310,
            PROPERTY_SET_PRESSURE: 1.5,
        }

        for missing_key in base_setpoints.keys():
            with self.subTest(missing_key=missing_key):
                setpoints = dict(base_setpoints)
                setpoints.pop(missing_key)
                with self.assertRaises(ValueError) as cm:
                    self.heat_pump._set_setpoints_secondary(setpoints)
                self.assertIn(missing_key, str(cm.exception))

    def test_set_setpoints_primary(self):
        setpoints = {
            PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 10.0,
            PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 20.0,
            PRIMARY + PROPERTY_HEAT_DEMAND: 300,
        }

        with patch(
            "omotes_simulator_core.entities.assets.heat_pump."
            "heat_demand_and_temperature_to_mass_flow",
            return_value=125,
        ) as mock_calc:
            self.heat_pump._set_setpoints_primary(setpoints)

            # Self attributes
            self.assertEqual(self.heat_pump.temperature_in_primary, 273.15 + 10.0)
            self.assertEqual(self.heat_pump.temperature_out_primary, 273.15 + 20.0)
            self.assertEqual(self.heat_pump.mass_flow_initialization_primary, 125)

            # Solver asset attributes
            self.assertEqual(self.heat_pump.solver_asset.temperature_in_primary, 273.15 + 10.0)
            self.assertEqual(self.heat_pump.solver_asset.temperature_out_primary, 273.15 + 20.0)
            self.assertEqual(self.heat_pump.solver_asset.mass_flow_initialization_primary, 125)

            mock_calc.assert_called_once_with(
                thermal_demand=300, temperature_in=273.15 + 10.0, temperature_out=273.15 + 20.0
            )

    def test_set_setpoints_primary_missing_key(self):
        base_setpoints = {
            PRIMARY + PROPERTY_TEMPERATURE_IN: 273.15 + 10.0,
            PRIMARY + PROPERTY_TEMPERATURE_OUT: 273.15 + 20.0,
            PRIMARY + PROPERTY_HEAT_DEMAND: 300,
            # PROPERTY_TEMPERATURE_IN: 273.15 + 10.0,
            # PROPERTY_TEMPERATURE_OUT: 273.15 + 20.0,
            # PROPERTY_HEAT_DEMAND: 300,
        }

        for missing_key in base_setpoints.keys():
            with self.subTest(missing_key=missing_key):
                setpoints = dict(base_setpoints)
                setpoints.pop(missing_key)
                with self.assertRaises(ValueError) as cm:
                    self.heat_pump._set_setpoints_primary(setpoints)
                self.assertIn(missing_key, str(cm.exception))

    def test_set_setpoints_calls_both_primary_and_secondary(self):
        setpoints = {
            PROPERTY_TEMPERATURE_IN: 300.0,
            PROPERTY_TEMPERATURE_OUT: 290.0,
            PROPERTY_HEAT_DEMAND: 1500,
            PROPERTY_SET_PRESSURE: 1.5,
        }

        with patch.object(self.heat_pump, "_set_setpoints_primary") as mock_primary, patch.object(
            self.heat_pump, "_set_setpoints_secondary"
        ) as mock_secondary:
            self.heat_pump.set_setpoints(setpoints)

            mock_primary.assert_called_once_with(setpoints_primary=setpoints)
            mock_secondary.assert_called_once_with(setpoints_secondary=setpoints)
