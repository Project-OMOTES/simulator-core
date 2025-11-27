#  Copyright (c) 2025. Deltares & TNO
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

"""Test Ideal Buffer."""
import unittest

import numpy as np

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_TEMPERATURE,
    PROPERTY_FILL_LEVEL,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.ideal_heat_storage import ChargeState, IdealHeatStorage
from omotes_simulator_core.entities.assets.utils import heat_demand_and_temperature_to_mass_flow
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


class HeatBufferTest(unittest.TestCase):
    """Testcase for HeatBuffer class."""

    def setUp(self) -> None:
        """Set up test case."""
        # Create a heat buffer object
        self.heat_buffer = IdealHeatStorage(
            asset_name="heat_buffer",
            asset_id="heat_buffer_id",
            port_ids=["test1", "test2"],
            volume=10.0,  # m3
            initial_fill_level=0.5,  # 50%
        )

    def test_create_heat_buffer(self):
        """Test creation of HeatBuffer."""
        self.assertEqual(self.heat_buffer.name, "heat_buffer")
        self.assertEqual(self.heat_buffer.asset_id, "heat_buffer_id")
        self.assertEqual(self.heat_buffer.max_volume, 10.0)
        self.assertEqual(self.heat_buffer.fill_level, 0.5)
        self.assertEqual(self.heat_buffer.current_volume_hot, 5.0)
        self.assertEqual(self.heat_buffer.temperature_connection_0, DEFAULT_TEMPERATURE)
        self.assertEqual(self.heat_buffer.temperature_connection_1, DEFAULT_TEMPERATURE)

    def test_heatbuffer_set_setpoints_clipped_discharging_volumetric_flowrate(self) -> None:
        """Test setting setpoints of a HeatBuffer when discharging clipped."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
        }
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Act
        max_volumetric_flow_rate = (
            self.heat_buffer.max_volume * self.heat_buffer.fill_level
        ) / self.heat_buffer.accumulation_time
        max_mass_flow_rate = max_volumetric_flow_rate * fluid_props.get_density(
            self.heat_buffer.temperature_connection_0
        )

        # Assert
        self.assertEqual(self.heat_buffer.temperature_connection_0, 333.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_0, 333.15)  # type: ignore
        self.assertEqual(self.heat_buffer.temperature_connection_1, 353.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_1, 353.15)  # type: ignore
        self.assertEqual(
            self.heat_buffer.solver_asset.inlet_massflow, max_mass_flow_rate  # type: ignore
        )
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.DISCHARGING)

    def test_heatbuffer_set_setpoints_clipped_charging_volumetric_flowrate(self) -> None:
        """Test setting setpoints of a HeatBuffer when charging clipped."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
        }
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Act
        max_volumetric_flow_rate = (
            self.heat_buffer.max_volume * (1 - self.heat_buffer.fill_level)
        ) / self.heat_buffer.accumulation_time
        max_mass_flow_rate = max_volumetric_flow_rate * fluid_props.get_density(
            self.heat_buffer.temperature_connection_0
        )

        # Assert
        self.assertEqual(self.heat_buffer.temperature_connection_0, 333.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_0, 333.15)  # type: ignore
        self.assertEqual(self.heat_buffer.temperature_connection_1, 353.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_1, 353.15)  # type: ignore
        self.assertEqual(
            self.heat_buffer.solver_asset.inlet_massflow, -1.0 * max_mass_flow_rate  # type: ignore
        )
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.CHARGING)

    def test_heatbuffer_set_setpoints_discharging(self) -> None:
        """Test setting setpoints of a HeatBuffer."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
        }
        self.heat_buffer.max_volume = 100.0  # m3
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_out=setpoints[PROPERTY_TEMPERATURE_OUT],
            temperature_in=setpoints[PROPERTY_TEMPERATURE_IN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
        )

        # Assert
        self.assertEqual(self.heat_buffer.temperature_connection_0, 333.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_0, 333.15)  # type: ignore
        self.assertEqual(self.heat_buffer.temperature_connection_1, 353.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_1, 353.15)  # type: ignore
        self.assertEqual(self.heat_buffer.solver_asset.inlet_massflow, mass_flow)  # type: ignore
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.DISCHARGING)

    def test_heatbuffer_set_setpoints_charging(self) -> None:
        """Test setting setpoints of a HeatBuffer."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
        }
        self.heat_buffer.max_volume = 100.0  # m3
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Act
        mass_flow = heat_demand_and_temperature_to_mass_flow(
            temperature_out=setpoints[PROPERTY_TEMPERATURE_OUT],
            temperature_in=setpoints[PROPERTY_TEMPERATURE_IN],
            thermal_demand=setpoints[PROPERTY_HEAT_DEMAND],
        )

        # Assert
        self.assertEqual(self.heat_buffer.temperature_connection_0, 333.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_0, 333.15)  # type: ignore
        self.assertEqual(self.heat_buffer.temperature_connection_1, 353.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_1, 353.15)  # type: ignore
        self.assertEqual(self.heat_buffer.solver_asset.inlet_massflow, mass_flow)  # type: ignore
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.CHARGING)

    def test_idle_set_setpoints(self) -> None:
        """Test setting setpoints of a HeatBuffer to idle."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 0.0,
            PROPERTY_TEMPERATURE_OUT: 353.15,
            PROPERTY_TEMPERATURE_IN: 333.15,
        }
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(self.heat_buffer.temperature_connection_0, 333.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_0, 333.15)  # type: ignore
        self.assertEqual(self.heat_buffer.temperature_connection_1, 353.15)
        self.assertEqual(self.heat_buffer.solver_asset.temperature_connection_1, 353.15)  # type: ignore
        self.assertEqual(self.heat_buffer.solver_asset.inlet_massflow, 0.0)  # type: ignore
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.IDLE)

    def test_heatbuffer_set_setpoints_missing_setpoint(self) -> None:
        """Test setting setpoints of a HeatBuffer with missing setpoint."""
        # Arrange
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: 353.15,
        }

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.heat_buffer.set_setpoints(setpoints=setpoints)
        self.assertEqual(
            str(context.exception),
            "The setpoints {'temperature_in'} are missing.",
        )

    def test_set_temperature_setpoints_charging(self) -> None:
        """Test setting temperature setpoints of a HeatBuffer when charging."""
        # Arrange
        self.heat_buffer.first_time_step = False
        setpoints = {
            PROPERTY_HEAT_DEMAND: -1e6,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_TEMPERATURE_OUT: 353.15,
        }

        # Act
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.CHARGING)
        self.assertEqual(
            self.heat_buffer.temperature_connection_0,
            self.heat_buffer.solver_asset.get_temperature(0),  # type: ignore
        )
        self.assertEqual(
            self.heat_buffer.temperature_connection_1,
            self.heat_buffer.buffer_temperature_cold,  # type: ignore
        )

    def test_set_temperature_setpoints_discharging(self) -> None:
        """Test setting temperature setpoints of a HeatBuffer when discharging."""
        # Arrange
        self.heat_buffer.first_time_step = False
        setpoints = {
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_TEMPERATURE_OUT: 353.15,
        }

        # Act
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(
            self.heat_buffer.temperature_connection_0,
            self.heat_buffer.buffer_temperature_hot,  # type: ignore
        )
        self.assertEqual(
            self.heat_buffer.temperature_connection_1,
            self.heat_buffer.solver_asset.temperature_connection_1,  # type: ignore
        )
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.DISCHARGING)

    def test_set_temperature_setpoints_idle(self) -> None:
        """Test setting temperature setpoints of a HeatBuffer when idle."""
        # Arrange
        self.heat_buffer.first_time_step = False
        setpoints = {
            PROPERTY_HEAT_DEMAND: 0.0,
            PROPERTY_TEMPERATURE_IN: 333.15,
            PROPERTY_TEMPERATURE_OUT: 353.15,
        }
        self.heat_buffer.buffer_temperature_hot = setpoints[PROPERTY_TEMPERATURE_IN]
        self.heat_buffer.buffer_temperature_cold = setpoints[PROPERTY_TEMPERATURE_OUT]

        # Act
        self.heat_buffer.set_setpoints(setpoints=setpoints)

        # Assert
        self.assertEqual(
            self.heat_buffer.temperature_connection_0,
            self.heat_buffer.solver_asset.temperature_connection_0,  # type: ignore
        )
        self.assertEqual(
            self.heat_buffer.temperature_connection_1,
            self.heat_buffer.solver_asset.temperature_connection_1,  # type: ignore
        )
        self.assertEqual(self.heat_buffer.charge_state, ChargeState.IDLE)

    def test_get_state(self) -> None:
        """Test getting state of a HeatBuffer."""
        # Arrange
        self.heat_buffer.fill_level = 0.75

        # Act
        state = self.heat_buffer.get_state()

        # Assert
        self.assertEqual(state[PROPERTY_FILL_LEVEL], 0.75)

    def test_postprocess(self) -> None:
        """Test postprocessing of a HeatBuffer."""
        # Arrange
        inflow_temperature = 293.15  # K
        outflow_temperature = 273.15  # K
        mass_flow = 2.0  # kg/s

        self.heat_buffer.max_volume = 100.0  # m3
        self.heat_buffer.fill_level = 0.5
        self.heat_buffer.current_volume_hot = (
            self.heat_buffer.max_volume * self.heat_buffer.fill_level
        )
        self.heat_buffer.time_step = 3600.0  # 1 hour
        self.heat_buffer.buffer_temperature_hot = inflow_temperature
        self.heat_buffer.buffer_temperature_cold = outflow_temperature

        self.heat_buffer.solver_asset.prev_sol = np.array(
            [
                -mass_flow,
                1e5,
                fluid_props.get_ie(inflow_temperature),
                +mass_flow,
                1e5,
                fluid_props.get_ie(outflow_temperature),
            ]
        )

        # Act
        self.heat_buffer.postprocess()

        # Assert
        self.assertAlmostEqual(
            self.heat_buffer.buffer_temperature_hot, inflow_temperature, places=2
        )
        self.assertAlmostEqual(
            self.heat_buffer.buffer_temperature_cold, outflow_temperature, places=2
        )
        self.assertAlmostEqual(
            self.heat_buffer.fill_level,
            0.572,
            places=3,
        )
        self.assertAlmostEqual(
            self.heat_buffer.current_volume_hot,
            57.2,
            places=1,
        )
