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

import unittest
import esdl
import uuid
import sys
import numpy as np
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from omotes_simulator_core.adapter.transforms.mappers import (
    EsdlControllerMapper,
    EsdlEnergySystemMapper,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.heat_network import HeatNetwork
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.simulation.networksimulation import NetworkSimulation
from omotes_simulator_core.solver.utils.fluid_properties import FluidProperties


class HeatDemandTest(unittest.TestCase):
    """Integration test for heat demand."""

    # Possible extra functions here: setUp (for setting up the tests).

    def test_heat_demand(self):
        """
        This test checks the physics of the heat demand and supply system. It
        fist gets the supplied demand profiles from the esdl and then, for each
        time step, gets the cp, mass flow and temperatures. These values are used
        to calculate the heat flow at each demand point and then compare to the
        edl input.
        """

        # Arrange
        esdl_file_path = Path(__file__).parent / ".." / ".." / "testdata" / "test1.esdl"
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        network = HeatNetwork(EsdlEnergySystemMapper(esdl_object).to_entity)
        controller = EsdlControllerMapper().to_entity(esdl_object)
        network_simulation = NetworkSimulation(network, controller)
        config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                        name="test run",
                                        timestep=3600,
                                        start=datetime.strptime("2019-01-01T00:00:00",
                                                                "%Y-%m-%dT%H:%M:%S"),
                                        stop=datetime.strptime("2019-01-01T06:00:00",
                                                                "%Y-%m-%dT%H:%M:%S"))
        # Act
        callback = Mock()
        app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
        result = app.execute(callback)

        energy_system = esdl_object.energy_system_handler.energy_system

        # Collect demands
        demands = []
        for element in energy_system.eAllContents():
            if isinstance(element, esdl.HeatingDemand):
                demands.append(element)

        # Collect id of in and out ports of each demand.
        in_out_demand_dict = dict()
        for demand in demands:
            demand_id = demand.id
            in_out_demand_dict[demand_id] = dict()
            for port in demand.port:
                if isinstance(port, esdl.InPort):
                    in_out_demand_dict[demand_id]["InPort"] = port.id
                elif isinstance(port, esdl.OutPort):
                    in_out_demand_dict[demand_id]["OutPort"] = port.id

        # Run through results to get the temperature and mass vaules over time.
        m_dot_in_out_demand = dict()
        temp_in_out_demand = dict()
        cp_in_out_demand = dict()
        q_dot_demand = dict()
        fluid_props = FluidProperties()


        for demand in demands:
            demand_id = demand.id
            in_port_id = in_out_demand_dict[demand_id]["InPort"]  
            out_port_id = in_out_demand_dict[demand_id]["OutPort"]
                        
            m_dot_in_out_demand[demand_id] = dict()
            temp_in_out_demand[demand_id] = dict()
            cp_in_out_demand[demand_id] = dict()

            m_dot_in_list = result[(in_port_id, 'mass_flow')]
            m_dot_out_list = result[(out_port_id, 'mass_flow')]
            m_dot_in_out_demand[demand_id]["In"] = m_dot_in_list
            m_dot_in_out_demand[demand_id]["Out"] = m_dot_out_list

            temp_in_list = result[(in_port_id, 'temperature')]
            temp_out_list = result[(out_port_id, 'temperature')]
            temp_in_out_demand[demand_id]["In"] = temp_in_list
            temp_in_out_demand[demand_id]["Out"] = temp_out_list
            cp_in = [] 
            cp_out = []
            for temp_in, temp_out in zip(temp_in_list, temp_out_list):
                cp_in.append(fluid_props.get_heat_capacity(temp_in))
                cp_out.append(fluid_props.get_heat_capacity(temp_out))
            cp_in_out_demand[demand_id]["In"] = cp_in
            cp_in_out_demand[demand_id]["Out"] = cp_out

            cp = (np.array(cp_in) + np.array(cp_out)) / 2
            q_dot_in = np.array(m_dot_in_list) * cp * np.array(temp_in_list)
            q_dot_out = np.array(m_dot_out_list) * cp * np.array(temp_out_list)
            delta_q_dot = q_dot_out - q_dot_in
            q_dot_demand[demand_id] = delta_q_dot

        print(q_dot_demand)

       
        
        # Use the previous dics to compute Qdot at each demand.
        
        # Extract the values as an array and multiply them all together to get Qdot.

        # Figure out how to get the demand profiles from the esdl. Maybe ask Ryvo.

        # Attest
        # Compare the consumed Qdot with the profile supplied by the esdl.

        pass

if __name__ == "__main__":
    test_object = HeatDemandTest()
    test_object.test_heat_demand()