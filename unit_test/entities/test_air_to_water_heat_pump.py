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

"""Test air to water heat pump."""
import unittest
from unittest.mock import patch

from omotes_simulator_core.entities.assets.air_to_water_heat_pump import (
    AirToWaterHeatPump,
)
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    PROPERTY_VOLUMEFLOW,
)
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class AirToWaterHeatPumpTest(unittest.TestCase):
    """Testcase for AirToWaterHeatPump class."""

    def setUp(self) -> None:
        """Set up test case."""
        # Create aan air to water heatpump cluster object
        self.air_to_water_hp = AirToWaterHeatPump(
            asset_name="air_to_water_hp",
            asset_id="air_to_water_hp_id",
            port_ids=["test1", "test2"],
            coefficient_of_performance=2,
        )

    def test_air_to_water_hp_create(self) -> None:
        """Evaluate the creation of a air_to_water_hp object."""
        # Arrange

        # Act

        # Assert
        self.assertIsInstance(self.air_to_water_hp, AirToWaterHeatPump)
        self.assertEqual(self.air_to_water_hp.name, "air_to_water_hp")
        self.assertEqual(self.air_to_water_hp.asset_id, "air_to_water_hp_id")
        self.assertEqual(self.air_to_water_hp.connected_ports, ["test1", "test2"])
        self.assertEqual(self.air_to_water_hp.coefficient_of_performance, 2)

    def test_air_to_water_hp_set_setpoints(self) -> None:
        """Test setting setpoints of a air to water heatpump."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }

        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_out=setpoints[PROPERTY_TEMPERATURE_OUT],
            temperature_in=setpoints[PROPERTY_TEMPERATURE_IN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
        )

        # Act
        self.air_to_water_hp.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(self.air_to_water_hp.temperature_out, 353.15)
        self.assertEqual(self.air_to_water_hp.temperature_in, 333.15)
        self.assertEqual(self.air_to_water_hp.controlled_mass_flow, mass_flow)
        self.assertEqual(
            self.air_to_water_hp.solver_asset.mass_flow_rate_set_point,  # type: ignore
            self.air_to_water_hp.controlled_mass_flow,
        )
        self.assertNotEqual(
            self.air_to_water_hp.solver_asset.pre_scribe_mass_flow,  # type: ignore
            setpoints[PROPERTY_SET_PRESSURE],
        )

    def test_air_to_water_hp_set_setpoints_missing_setpoint(self) -> None:
        """Test raise ValueError with missing setpoint."""
        # Arrange
        necessary_setpoints = set(
            [PROPERTY_HEAT_DEMAND, PROPERTY_TEMPERATURE_OUT, PROPERTY_TEMPERATURE_IN]
        )
        setpoints = {
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        with self.assertRaises(ValueError) as cm:
            self.air_to_water_hp.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The setpoints {necessary_setpoints.difference(set(setpoints))} are missing.",
        )

    def test_air_to_water_hp_set_setpoints_negative_mass_flow(self) -> None:
        """Test raise ValueError with negative mass flow."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_SET_PRESSURE: False,
        }

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_out=setpoints[PROPERTY_TEMPERATURE_OUT],
            temperature_in=setpoints[PROPERTY_TEMPERATURE_IN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
        )

        with self.assertRaises(ValueError) as cm:
            self.air_to_water_hp.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The mass flow rate {mass_flow} of the asset {self.air_to_water_hp.name}"
            + " is negative.",
        )

    def test_air_to_water_hp_set_setpoints_pressure_or_mass_flow_control(self) -> None:
        """Test setting pressure setpoint of an air to water heatpump."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_SET_PRESSURE: True,
        }

        # Act
        self.air_to_water_hp.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertNotEqual(
            self.air_to_water_hp.control_mass_flow, setpoints[PROPERTY_SET_PRESSURE]
        )
        self.assertNotEqual(
            self.air_to_water_hp.solver_asset.pre_scribe_mass_flow,  # type: ignore
            setpoints[PROPERTY_SET_PRESSURE],
        )

    def test_air_to_water_hp_set_pressure_supply(self) -> None:
        """Test setting pressure of an air to water heatpump."""
        # Arrange
        pressure_supply = 2e5  # [Pa]

        # Act
        self.air_to_water_hp.set_pressure_supply(pressure_supply=pressure_supply)

        # Assert
        self.assertEqual(self.air_to_water_hp.pressure_supply, pressure_supply)
        self.assertEqual(
            self.air_to_water_hp.solver_asset.set_pressure, pressure_supply  # type: ignore
        )

    def test_air_to_water_hp_set_pressure_supply_negative(self) -> None:
        """Test raise ValueError with negative pressure."""
        # Arrange
        pressure_supply = -2e5  # [Pa]

        # Act
        with self.assertRaises(ValueError) as cm:
            self.air_to_water_hp.set_pressure_supply(pressure_supply=pressure_supply)

        # Assert
        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args[0],
            f"The pressure {pressure_supply} of the asset {self.air_to_water_hp.name}"
            + " can not be negative.",
        )

    def test_air_to_water_hp_write_to_output(self) -> None:
        """Test writing the output of an air to water heatpump."""
        # Arrange
        with (
            patch.object(
                self.air_to_water_hp.solver_asset, "get_mass_flow_rate"
            ) as get_mass_flow_rate,
            patch.object(self.air_to_water_hp.solver_asset, "get_pressure") as get_pressure,
            patch.object(self.air_to_water_hp.solver_asset, "get_temperature") as get_temperature,
            patch.object(self.air_to_water_hp, "get_volume_flow_rate") as get_volume_flow_rate,
        ):
            get_mass_flow_rate.return_value = 1e6
            get_pressure.return_value = 2e5
            get_temperature.return_value = 333.15
            get_volume_flow_rate.return_value = 100.0

            # Act
            self.air_to_water_hp.write_standard_output()

        # Assert
        self.assertEqual(
            len(self.air_to_water_hp.outputs), len(self.air_to_water_hp.connected_ports)
        )
        self.assertEqual(len(self.air_to_water_hp.outputs[0]), 1)
        self.assertEqual(
            self.air_to_water_hp.outputs[0][0],
            {
                PROPERTY_TEMPERATURE: 333.15,
                PROPERTY_MASSFLOW: -1e6,
                PROPERTY_PRESSURE: 2e5,
                PROPERTY_VOLUMEFLOW: -100.0,
            },
        )

    def test_get_volume_flow_rate(self):
        """Test getting the volume flow rate of an air to water heatpump."""
        # Arrange
        with (
            patch.object(
                self.air_to_water_hp.solver_asset,
                "get_mass_flow_rate",
            ) as get_mass_flow_rate,
            patch.object(
                fluid_props,
                "get_density",
            ) as get_density,
        ):
            get_mass_flow_rate.return_value = 1000.0
            get_density.return_value = 1000.0

            # Act
            volume_flow_rate = self.air_to_water_hp.get_volume_flow_rate(i=0)
            # Assert
            self.assertEqual(volume_flow_rate, 1.0)

    def test_get_actual_heat_supplied(self):
        """Test getting the actual heat supplied by an air to water heatpump."""  # noqa: D202

        # Arrange
        def get_internal_energy(_, i: int):
            if i == 0:
                return 1.0e6
            if i == 1:
                return 2.0e6

        def get_mass_flow_rate(_, i: int):
            return 0.5

        with (
            patch(
                "omotes_simulator_core.solver.network.assets.base_asset."
                "BaseAsset.get_internal_energy",
                get_internal_energy,
            ),
            patch(
                "omotes_simulator_core.solver.network.assets.base_asset."
                "BaseAsset.get_mass_flow_rate",
                get_mass_flow_rate,
            ),
        ):
            # Act
            actual_heat_supplied = self.air_to_water_hp.get_actual_heat_supplied()
            # Assert
            self.assertEqual(actual_heat_supplied, 0.5 * 1e6)

    def test_get_electric_consumption(self):
        """Test getting the electric power consumed by the heatpump"""

        # Arrange
        def get_internal_energy(_, i: int):
            if i == 0:
                return 1.0e6
            if i == 1:
                return 2.0e6

        def get_mass_flow_rate(_, i: int):
            return 0.5

        with (
            patch(
                "omotes_simulator_core.solver.network.assets.base_asset."
                "BaseAsset.get_internal_energy",
                get_internal_energy,
            ),
            patch(
                "omotes_simulator_core.solver.network.assets.base_asset."
                "BaseAsset.get_mass_flow_rate",
                get_mass_flow_rate,
            ),
        ):
            # Act
            power_consumed = (
                abs(self.air_to_water_hp.get_actual_heat_supplied())
                / self.air_to_water_hp.coefficient_of_performance
            )
            actual_power_consumed = self.air_to_water_hp.get_electric_power_consumption()
            # Assert
            self.assertEqual(actual_power_consumed, power_consumed)


if __name__ == "__main__":
    test = AirToWaterHeatPumpTest()
    test.setUp()
