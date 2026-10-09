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

"""Integration tests for an ATES asset in a heat network.

The tests run a single time step with a hand-made controller input, so the behaviour of the ATES
asset can be checked for a charging and for a discharging time step without depending on the
controller allocation logic.
"""
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import cast

from omotes_simulator_core.adapter.transforms.mappers import EsdlEnergySystemMapper
from omotes_simulator_core.entities.assets.asset_defaults import (
    PROPERTY_HEAT_DEMAND,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster
from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file

# Asset ids of testdata/test_ates_2.esdl
ATES_ID = "4d6dfb40-ea51-4176-a27e-4ee60cad4034"
PRODUCER_ID = "0375b489-b57b-439d-9ce9-db2dc9d0bbb9"
CONSUMER_IDS = [
    "cc61c52a-29a6-45d3-81e8-ce18ba12f319",  # Pijnacker
    "8805731a-8780-47b4-8204-76ba074564bc",  # Delfgauw
    "156c4afb-4106-4286-8f41-fbf8edc6e5ce",  # Nootdorp
]

# Carrier temperatures of testdata/test_ates_2.esdl
SUPPLY_TEMPERATURE = 273.15 + 80.0
RETURN_TEMPERATURE = 273.15 + 40.0

CONSUMER_POWER = 1e6  # W per consumer
ATES_POWER = 2e6  # W
TIME_STEP = 3600.0  # s
MAX_ITERATIONS = 20
NUMBER_OF_TIME_STEPS = 5


class AtesNetworkTest(unittest.TestCase):
    """Test the ATES asset in a network for a charging and a discharging time step."""

    def setUp(self) -> None:
        """Create the heat network of the ATES test case."""
        esdl_file_path = str(Path(__file__).parent / ".." / ".." / "testdata" / "test_ates.esdl")
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)
        self.ates = cast(AtesCluster, self.network.get_asset_by_id(ATES_ID))
        self.producer = cast(ProductionCluster, self.network.get_asset_by_id(PRODUCER_ID))
        self.time = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    def _get_controller_input(self, ates_power: float) -> dict:
        """Create the controller input for a time step.

        The setpoints follow the convention of the controller: a positive heat demand is heat
        flowing from the network into the asset and a negative heat demand is heat flowing from
        the asset into the network. The temperature setpoints of a storage are swapped between
        charging and discharging, just like the controller does.

        :param float ates_power: The power of the ATES, positive for charging and negative for
            discharging [W].
        :return: dict with the setpoints per asset id.
        """
        controller_input: dict = {}
        for consumer_id in CONSUMER_IDS:
            controller_input[consumer_id] = {
                PROPERTY_HEAT_DEMAND: CONSUMER_POWER,
                PROPERTY_TEMPERATURE_IN: SUPPLY_TEMPERATURE,
                PROPERTY_TEMPERATURE_OUT: RETURN_TEMPERATURE,
            }
        if ates_power >= 0:
            # Charging, the controller swaps the inflow and outflow temperature setpoints.
            controller_input[ATES_ID] = {
                PROPERTY_HEAT_DEMAND: ates_power,
                PROPERTY_TEMPERATURE_IN: SUPPLY_TEMPERATURE,
                PROPERTY_TEMPERATURE_OUT: RETURN_TEMPERATURE,
                PROPERTY_SET_PRESSURE: False,
            }
        else:
            controller_input[ATES_ID] = {
                PROPERTY_HEAT_DEMAND: ates_power,
                PROPERTY_TEMPERATURE_IN: RETURN_TEMPERATURE,
                PROPERTY_TEMPERATURE_OUT: SUPPLY_TEMPERATURE,
                PROPERTY_SET_PRESSURE: False,
            }
        # The producer supplies the consumers and the charging of the ATES, or is relieved by the
        # discharging of the ATES. Supplying heat to the network is negative.
        controller_input[PRODUCER_ID] = {
            PROPERTY_HEAT_DEMAND: -1 * (len(CONSUMER_IDS) * CONSUMER_POWER + ates_power),
            PROPERTY_TEMPERATURE_IN: RETURN_TEMPERATURE,
            PROPERTY_TEMPERATURE_OUT: SUPPLY_TEMPERATURE,
            PROPERTY_SET_PRESSURE: True,
        }
        return controller_input

    def _run_time_step(self, ates_power: float) -> None:
        """Run a single time step with the given ATES power.

        :param float ates_power: The power of the ATES, positive for charging and negative for
            discharging [W].
        """
        controller_input = self._get_controller_input(ates_power)
        for _ in range(MAX_ITERATIONS):
            self.network.run_time_step(
                time=self.time, time_step=TIME_STEP, controller_input=controller_input
            )
            if self.network.check_convergence():
                break
        self.network.post_process_assets()
        self.network.store_output()
        self.time = self.time + timedelta(seconds=TIME_STEP)

    def _assert_charging(self) -> None:
        """Assert that the solved time step charges the ATES."""
        # The ATES is charging, so the flow is from connection point 0 to connection point 1.
        self.assertGreater(self.ates.mass_flowrate, 0.0)
        self.assertLess(self.ates.solver_asset.get_mass_flow_rate(0), 0.0)
        self.assertGreater(self.ates.solver_asset.get_mass_flow_rate(1), 0.0)
        # Water from the supply side of the network flows into the ATES at connection point 0.
        self.assertGreater(self.ates.solver_asset.get_temperature(0), RETURN_TEMPERATURE)
        # The water leaving the ATES at connection point 1 has the cold well temperature.
        self.assertAlmostEqual(
            self.ates.solver_asset.get_temperature(1),
            self.ates.cold_well_temperature,
            delta=1.0,
        )
        # The ATES takes heat from the network.
        self.assertGreater(self.ates.get_heat_supplied(), 0.0)

    def _assert_discharging(self) -> None:
        """Assert that the solved time step discharges the ATES."""
        # The ATES is discharging, so the flow is from connection point 1 to connection point 0.
        self.assertLess(self.ates.mass_flowrate, 0.0)
        self.assertGreater(self.ates.solver_asset.get_mass_flow_rate(0), 0.0)
        self.assertLess(self.ates.solver_asset.get_mass_flow_rate(1), 0.0)
        # The water leaving the ATES at connection point 0 has the hot well temperature.
        self.assertAlmostEqual(
            self.ates.solver_asset.get_temperature(0),
            self.ates.hot_well_temperature,
            delta=1.0,
        )
        # Water from the return side of the network flows into the ATES at connection point 1.
        self.assertLess(self.ates.solver_asset.get_temperature(1), SUPPLY_TEMPERATURE)
        # The ATES delivers heat to the network.
        self.assertLess(self.ates.get_heat_supplied(), 0.0)

    def _assert_producer_supplies_network(self) -> None:
        """Assert that the producer supplies the network and is not reversed."""
        # The producer takes in water at connection point 0 and delivers water at connection
        # point 1.
        self.assertLess(self.producer.solver_asset.get_mass_flow_rate(0), 0.0)
        self.assertGreater(self.producer.solver_asset.get_mass_flow_rate(1), 0.0)

    def test_charging_ates(self) -> None:
        """Test a time step in which the ATES is charged."""
        # Act
        self._run_time_step(ATES_POWER)

        # Assert
        self._assert_charging()
        self._assert_producer_supplies_network()

    def test_discharging_ates(self) -> None:
        """Test a time step in which the ATES is discharged."""
        # Act
        self._run_time_step(-1 * ATES_POWER)

        # Assert
        self._assert_discharging()
        self._assert_producer_supplies_network()

    def test_charging_and_discharging_ates_multiple_time_steps(self) -> None:
        """Test consecutive time steps of charging followed by discharging of the ATES.

        After the first time step the ATES takes the temperature of its inflowing connection point
        from the solved network state, so these time steps cover the coupling between the solver
        and the aquifer model.
        """
        for time_step in range(NUMBER_OF_TIME_STEPS):
            with self.subTest(mode="charging", time_step=time_step):
                # Act
                self._run_time_step(ATES_POWER)

                # Assert
                self._assert_charging()
                self._assert_producer_supplies_network()

        for time_step in range(NUMBER_OF_TIME_STEPS):
            with self.subTest(mode="discharging", time_step=time_step):
                # Act
                self._run_time_step(-1 * ATES_POWER)

                # Assert
                self._assert_discharging()
                self._assert_producer_supplies_network()
