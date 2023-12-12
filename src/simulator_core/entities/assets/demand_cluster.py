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

"""ProductionCluster class."""

from typing import Dict

from pandapipes import pandapipesNet
from pandas import DataFrame

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_DIAMETER,
    DEFAULT_NODE_HEIGHT,
    DEFAULT_SUPPLY_TEMPERATURE,
    DEFAULT_RETURN_TEMPERATURE,
    DEFAULT_PRESSURE,
)
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.heatexchanger import HeatExchanger
from simulator_core.entities.assets.valve import ControlValve
from typing import Optional


class DemandCluster(AssetAbstract):
    """A DemandCluster represents an asset that consumes heat."""

    def __init__(
            self,
            asset_name: str,
            asset_id: str,
            pandapipe_net: pandapipesNet
    ):
        """Initialize a DemandCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, pandapipe_net=pandapipe_net)

        self.setpoints = dict()
        self.parameters = dict()
        self.states = dict()

        self.parameters['height'] = DEFAULT_NODE_HEIGHT
        self.parameters['internal_diameter'] = DEFAULT_DIAMETER
        self.parameters['temperature_supply_desired'] = DEFAULT_SUPPLY_TEMPERATURE
        self.parameters['temperature_return_target'] = DEFAULT_RETURN_TEMPERATURE

        self.setpoints['thermal_power_allocation'] = 0

        self.states['temperature_input'] = DEFAULT_SUPPLY_TEMPERATURE
        self.states['temperature_output'] = DEFAULT_RETURN_TEMPERATURE
        self.states['mass_flowrate'] = 0
        self.states['volume_flowrate'] = 0
        self.states['thermal_power'] = 0

        # Objects of the asset
        self._initialized = False
        self._intermediate_junction: Optional[Junction] = None
        self._flow_control = None
        self._heat_exchanger = None
        self._simulated = False
        self._from_junction = None
        self._to_junction = None
        # Output list
        self.output: list = []

    def create(self) -> None:
        """Create a representation of the asset in pandapipes.

        The DemandCluster asset contains multiple pandapipes components.

        The component model contains the following components:
        - A flow control valve to set the mass flow rate of the system.
        - A heat exchanger to set the power consumption of the demand
        - An intermediate junction to link both components.
        :param pandapipesNet pandapipes_net: pandapipes network object
        """
        if not self._initialized:
            # Create intermediate junction
            self._intermediate_junction = Junction(
                pandapipes_net=self.pandapipes_net,
                pn_bar=DEFAULT_PRESSURE,
                tfluid_k=self.parameters['temperature_supply_desired'],
                height_m=self.parameters['height'],
                name=f"intermediate_junction_{self.name}",
            )
            # Create the control valve
            self._flow_control = ControlValve(
                pandapipes_net=self.pandapipes_net,
                controlled_mdot_kg_per_s=self.states['mass_flowrate'],
                diameter_m=self.parameters['internal_diameter'],
                control_active=True,
                in_service=True,
                name=f"flow_control_{self.name}",
            )
            self._flow_control.from_junction = self._from_junction
            self._flow_control.to_junction = self._intermediate_junction
            self._flow_control.create()

            # Create the heat exchanger
            self._heat_exchanger = HeatExchanger(
                pandapipes_net=self.pandapipes_net,
                diameter_m=self.parameters['internal_diameter'],
                heat_flux_w=self.setpoints['thermal_power_allocation'],
                name=f"heat_exchanger_{self.name}",
                in_service=True,
            )
            self._heat_exchanger.from_junction = self._intermediate_junction
            self._heat_exchanger.to_junction = self._to_junction
            self._heat_exchanger.create()

            self._initialized = True

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        # update setpoints to object properties
        for key in setpoints:
            self.setpoints[key] = setpoints[key]

        # get heat capacity of water
        if self.simulation_performed():
            temp_supply = self.states['temperature_input']
            Cp = net.fluid.get_heat_capacity(temp_supply)
            dT = temp_supply - self.parameters['temperature_return_target']
        else:
            temp_supply = self.parameters['temperature_supply_desired']
            Cp = net.fluid.get_heat_capacity(temp_supply)
            dT = temp_supply - self.parameters['temperature_return_target']
            self.states['mass_flowrate'] = self.setpoints['thermal_power_allocation'] / (Cp * dT)

        if self._flow_control.control_active is True:
            # if pump is active, set flowrate to meet Target Temperature
            self._heat_exchanger.qext_w = self.setpoints['thermal_power_allocation']

            demand_flow = self.setpoints['thermal_power_allocation'] / (Cp * dT)
            self.pandapipes_net.flow_control.controlled_mdot_kg_per_s[self._flow_control.index] \
                = demand_flow
        else:
            # if pump is disabled, set thermal power to meet Target Temperature
            demand_power = self.states['mass_flowrate'] * Cp * dT
            self.pandapipes_net.heat_exchanger.qext_w[self._heat_exchanger.index] = demand_power

    def get_setpoints(self) -> Dict:
        """Placeholder to get the setpoint attributes of an asset.

        :return Dict: The setpoints of the asset. The keys of the dictionary are the names of the
            setpoints and the values are the values.
        """
        return self.setpoints

    def set_parameters(self, parameters: Dict) -> None:
        """Placeholder to set the parameters of an asset prior to a simulation.

        :param Dict parameters: The parameters that should be set for the asset.
            The keys of the dictionary are the names of the parameters and the values are the values
        """
        # update parameters to object properties
        for key in parameters:
            self.parameters[key] = parameters[key]

    def get_parameters(self) -> Dict:
        """Placeholder to get the parameters attributes of an asset.

        :return Dict: The parameters of the asset. The keys of the dictionary are the names of the
            parameters and the values are the values.
        """
        return self.parameters

    def update_states(self):
        """Placeholder to update states attributes of an asset.

        if simulation has been performed, the states properties is updated from pandapipe_net
        """
        if self.simulation_performed():
            water_density = net.fluid.get_density(
                self.pandapipes_net.res_heat_exchanger['t_from_k'][self._heat_exchanger.index])
            water_heat_capacity = net.fluid.get_heat_capacity(
                self.pandapipes_net.res_heat_exchanger['t_from_k']
                [self._heat_exchanger.index])
            dT = self.pandapipes_net.res_heat_exchanger['t_from_k']
            [self._heat_exchanger.index] - \
                self.pandapipes_net.res_heat_exchanger['t_to_k']
            [self._heat_exchanger.index]

        self.states['temperature_input'] = self.pandapipes_net.res_flow_control[
            't_from_k'][self._flow_control.index]
        self.states['temperature_output'] = self.pandapipes_net.res_heat_exchanger[
            't_to_k'][self._heat_exchanger.index]
        self.states['mass_flowrate'] = self.pandapipes_net.res_heat_exchanger[
            'mdot_from_kg_per_s'][self._heat_exchanger.index]
        self.states['volume_flowrate'] = self.states['mass_flowrate'] * 3600 / water_density
        self.states['thermal_power'] = self.states['mass_flowrate'] * water_heat_capacity * dT
        self.states['pressure_input'] = self.pandapipes_net.res_flow_control['p_from_bar'][
            self._flow_control.index]
        self.states['pressure_output'] = self.pandapipes_net.res_heat_exchanger[
            'p_to_bar'][self._heat_exchanger.index]


def get_results(self) -> Dict:
    """Placeholder to get the results attributes of an asset.

    :return Dict: The results of the asset. The keys of the dictionary are the names of the
        results and the values are the values.
    """
    results = self.states  # currenty publish states as results

    return results


def simulation_performed(self) -> bool:
    """Check if the simulation has been performed.

    :return bool simulation_performed: True if the simulation has been performed,
        False otherwise.
    """
    return self._simulated


def add_physical_data(self, data: Dict[str, float]) -> None:
    """Method to add physical data to the asset.

    :param dict data:dictionary containing the data to be added the asset. The key is the name
                    of the property, the value of the dict is the value of the property.
    :return:
    """
    pass


def write_to_output(self) -> None:
    """Placeholder to write the asset to the output.

    The output list is a list of dictionaries, where each dictionary
    represents the output of its asset for a specific timestep.
    """
    pass


def get_timeseries(self) -> DataFrame:
    """Get timeseries as a dataframe from a pandapipes asset.

    The header is a tuple of the asset id and the property name.
    """
    pass


if __name__ == "__main__":
    # Check functionality of the DemandCluster
    # Create a simple pandapipes network with a demand cluster
    import pandapipes as pp

    using_demand_cluster = True

    net = pp.create_empty_network(fluid="water")

    j0 = Junction(pandapipes_net=net, pn_bar=DEFAULT_PRESSURE, tfluid_k=DEFAULT_SUPPLY_TEMPERATURE,
                  name="junction out producer")
    j1 = Junction(pandapipes_net=net, pn_bar=DEFAULT_PRESSURE, tfluid_k=DEFAULT_SUPPLY_TEMPERATURE,
                  name="junction in demand")
    j2 = Junction(pandapipes_net=net, pn_bar=DEFAULT_PRESSURE, tfluid_k=DEFAULT_RETURN_TEMPERATURE,
                  name="junction out demand")
    j3 = Junction(pandapipes_net=net, pn_bar=DEFAULT_PRESSURE, tfluid_k=DEFAULT_RETURN_TEMPERATURE,
                  name="junction in producer")

    # Create Pipe
    pp.create_pipe_from_parameters(net,
                                   from_junction=j0.index,
                                   to_junction=j1.index,
                                   length_km=1,
                                   sections=10,
                                   alpha_w_per_m2k=0.02,
                                   diameter_m=DEFAULT_DIAMETER,
                                   name='Pipe Supply')

    pp.create_pipe_from_parameters(net,
                                   from_junction=j2.index,
                                   to_junction=j3.index,
                                   length_km=1,
                                   sections=10,
                                   alpha_w_per_m2k=0.02,
                                   diameter_m=DEFAULT_DIAMETER,
                                   name='Pipe Return')

    # Create Producer
    intermediate_junction = Junction(pandapipes_net=net,
                                     pn_bar=DEFAULT_PRESSURE,
                                     tfluid_k=DEFAULT_SUPPLY_TEMPERATURE,
                                     name='intermediate junction ' + 'ProductionCluster1')

    pp.create_flow_control(net,
                           from_junction=intermediate_junction.index,
                           to_junction=j0.index,
                           controlled_mdot_kg_per_s=0,
                           diameter_m=0.5,
                           control_active=True,
                           name='flow control valve ' + 'ProductionCluster1')

    pp.create_circ_pump_const_mass_flow(net,
                                        return_junction=j3.index,
                                        flow_junction=intermediate_junction.index,
                                        p_flow_bar=DEFAULT_PRESSURE,
                                        mdot_flow_kg_per_s=0,
                                        t_flow_k=DEFAULT_SUPPLY_TEMPERATURE,
                                        name='ProductionCluster1',
                                        type='auto')

    if using_demand_cluster is False:
        # Create Demand
        intermediate_junction = Junction(pandapipes_net=net,
                                         pn_bar=DEFAULT_PRESSURE,
                                         tfluid_k=DEFAULT_SUPPLY_TEMPERATURE,
                                         name='intermediate junction ' + 'DemandCluster1')

        pp.create_flow_control(net,
                               from_junction=j1.index,
                               to_junction=intermediate_junction.index,
                               controlled_mdot_kg_per_s=0,
                               diameter_m=DEFAULT_DIAMETER,
                               control_active=True,
                               name='flow control valve ' + 'DemandCluster1')

        pp.create_heat_exchanger(net,
                                 from_junction=intermediate_junction.index,
                                 to_junction=j2.index,
                                 diameter_m=DEFAULT_DIAMETER,
                                 qext_w=0,
                                 name='DemandCluster1')
    else:
        demand_cluster = DemandCluster('DemandCluster1', 'demand_1', net)
        demand_cluster._from_junction = j1
        demand_cluster._to_junction = j2
        demand_cluster.create()

    # Set input
    dT = DEFAULT_SUPPLY_TEMPERATURE - DEFAULT_RETURN_TEMPERATURE
    Cp = net.fluid.get_heat_capacity(DEFAULT_SUPPLY_TEMPERATURE)
    demand_power = 1e7
    demand_flow = demand_power / (Cp * dT)
    supply_flow = demand_flow

    if using_demand_cluster is False:
        # demand
        net.heat_exchanger.qext_w[0] = demand_power
        flow_control_index = net.flow_control.index[
            net.flow_control.name.str.contains(net.heat_exchanger.name[0])].tolist()
        net.flow_control.controlled_mdot_kg_per_s[flow_control_index] = demand_flow
        net.flow_control.control_active[flow_control_index] = False
    else:
        demand_cluster._flow_control.control_active = False
        net.flow_control.control_active[demand_cluster._flow_control.index] = False
        demand_setpoints = dict()
        demand_setpoints['thermal_power_allocation'] = demand_power
        demand_cluster.set_setpoints(demand_setpoints)

    # producer
    net.circ_pump_mass.mdot_flow_kg_per_s[0] = supply_flow
    flow_control_index = net.flow_control.index[net.flow_control.name.str.contains(
        net.circ_pump_mass.name[0])].tolist()
    net.flow_control.controlled_mdot_kg_per_s[flow_control_index] = supply_flow
    net.flow_control.control_active[flow_control_index] = False

    pp.pipeflow(net, mode='all')

    if using_demand_cluster is False:
        pass
    else:
        demand_cluster._simulated = True
        demand_cluster.update_states()
        results = demand_cluster.get_results()
        print(results)

    print(net.res_pipe)
