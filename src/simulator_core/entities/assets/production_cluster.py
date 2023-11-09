"""ProductionCluster class."""
from typing import Dict
from warnings import warn

import numpy as np
import pandas as pd
from pandapipes import pandapipesNet

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_DIAMETER,
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.pump import CirculationPumpConstantMass
from simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
    mass_flow_and_temperature_to_heat_demand,
)
from simulator_core.entities.assets.valve import ControlValve


class ProductionCluster:
    """A ProductionCluster represents an asset that produces heat."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        asset_name: str,
        asset_id: str,
        from_junction: Junction,
        to_junction: Junction,
        thermal_production_required: float,
        temperature_supply: float,
        temperature_return: float = np.NaN,
        height_m: float = DEFAULT_NODE_HEIGHT,
        internal_diameter: float = DEFAULT_DIAMETER,
        pressure_supply: float = DEFAULT_PRESSURE,
        control_mass_flow: bool = False,
    ):
        """Initialize a ProductionCluster object.

        :param pandapipesNet pandapipes_net: The pandapipes network in which the
            asset is created.
        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param Junction from_junction: The junction where the asset starts.
        :param Junction to_junction: The junction where the asset ends.
        :param float thermal_production_required: The thermal allocation of the asset.
            The thermal allocation should be supplied in Watts.
        :param float temperature_supply: The temperature that the asset
            delivers to the "to_junction". The temperature should be
            supplied in Kelvin.
        :param float temeprature_return: The temperature that the asset
            receives from the "from_junction". The temperature should be
            supplied in Kelvin. If the value is not supplied it defaults to
            "temperature_supply" - DEFAULT_TEMPERATURE_DIFFERENCE.
        :param float height_m: The height of the junctions. The height should
            be supplied in meters, it defaults to DEFAULT_NODE_HEIGHT.
        :param float internal_diameter: The internal diameter of the pipe.
            The internal diameter should be supplied in meters, it defaults to
            DEFAULT_DIAMETER.
        :param float pressure_supply: The pressure that the asset delivers
            to the "to_junction". The pressure should be supplied in bar, it
            defaults to DEFAULT_PRESSURE.
        :param bool control_mass_flow: If True, the mass flow rate of the asset
            is controlled by the "Control Valve". If False, the mass flow rate
            of the asset is floating.
        """
        # Define the pandapipes network
        self.pandapipes_net = pandapipes_net
        # Define the asset properties
        self.asset_name = asset_name
        self.asset_id = asset_id
        # TODO: Do we need to carry the junction ids?
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.internal_diameter = internal_diameter
        self.height_m = height_m
        # DemandCluster thermal and mass flow specifications
        self.thermal_production_required = thermal_production_required
        self.temperature_supply = temperature_supply
        self.temperature_return = (
            temperature_supply - DEFAULT_TEMPERATURE_DIFFERENCE
            if np.isnan(temperature_return)
            else temperature_return
        )
        # DemandCluster pressure specifications
        self.pressure_supply = pressure_supply
        self.control_mass_flow = control_mass_flow
        self._controlled_mass_flow = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=self.thermal_production_required,
            temperature_supply=self.temperature_supply,
            temperature_return=self.temperature_return,
            pandapipes_net=self.pandapipes_net,
        )
        # Objects of the asset
        self._initialized = False
        self._create()

        # Output list
        self.output = []

    def _create(self) -> None:
        """Create a representation of the asset in pandapipes.

        The ProductionCluster asset contains multiple pandapipes components.

        The component model contains the following components:
        - A flow control valve to set the mass flow rate of the system.
        - A circulation pump to set the pressure and the temperature of the
        system.
        - An intermediate junction to link both components.
        """
        if not self._initialized:
            self._initialized = True
            # Create intermediate junction
            self._intermediate_junction = Junction(
                pandapipes_net=self.pandapipes_net,
                pn_bar=self.pressure_supply,
                tfluid_k=self.temperature_supply,
                height_m=self.height_m,
                name=f"intermediate_junction_{self.asset_name}",
            )
            # Create the pump to supply pressure and or massflow
            self._circ_pump = CirculationPumpConstantMass(
                pandapipes_net=self.pandapipes_net,
                from_junction=self.from_junction,
                to_junction=self._intermediate_junction,
                p_to_junction=self.pressure_supply,
                mdot_kg_per_s=self._controlled_mass_flow,
                t_to_junction=self.temperature_supply,
                name=f"circ_pump_{self.asset_name}",
                in_service=True,
            )
            # Create the control valve
            self._flow_control = ControlValve(
                pandapipes_net=self.pandapipes_net,
                from_junction=self._intermediate_junction,
                to_junction=self.to_junction,
                controlled_mdot_kg_per_s=self._controlled_mass_flow,
                diameter_m=self.internal_diameter,
                control_active=self.control_mass_flow,
                in_service=True,
                name=f"flow_control_{self.asset_name}",
            )

    def _set_supply_temperature(self, temperature_supply: float) -> None:
        """Set the supply temperature of the asset.

        :param float temperature_supply: The supply temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the temperature of the circulation pump mass flow
        self.temperature_supply = temperature_supply
        # Retrieve the value array of the temperature
        self.pandapipes_net["circ_pump_mass"]["t_flow_k"][
            self._circ_pump.index
        ] = self.temperature_supply

    def _set_return_temperature(self, temperature_return: float) -> None:
        """Set the return temperature of the asset.

        :param float temperature_return: The return temperature of the asset.
            The temperature should be supplied in Kelvin.
        """
        # Set the return temperature of the asset
        self.temperature_return = temperature_return

    def _set_heat_demand(self, heat_demand: float) -> None:
        """Set the heat demand of the asset.

        :param float heat_demand: The heat demand of the asset.
            The heat demand should be supplied in Watts.
        """
        # Calculate the mass flow rate
        self._controlled_mass_flow = heat_demand_and_temperature_to_mass_flow(
            thermal_demand=heat_demand,
            temperature_supply=self.temperature_supply,
            temperature_return=self.temperature_return,
            pandapipes_net=self.pandapipes_net,
        )
        # Check if the mass flow rate is positive
        if self._controlled_mass_flow < 0:
            raise ValueError(
                f"The mass flow rate {self._controlled_mass_flow} of the asset {self.asset_name}"
                + " is negative."
            )
        else:
            # Set the mass flow rate of the circulation pump
            self.pandapipes_net["circ_pump_mass"]["mdot_flow_kg_per_s"][
                self._circ_pump.index
            ] = self._controlled_mass_flow
            # Set the mass flow rate of the control valve
            self.pandapipes_net["flow_control"]["controlled_mdot_kg_per_s"][
                self._flow_control.index
            ] = self._controlled_mass_flow

    def set_setpoints(self, setpoints: Dict) -> None:
        """Set the setpoints of the asset.

        :param Dict setpoints: The setpoints of the asset in a dictionary,
            as "property_name": value pairs.

        """
        # Default keys required
        necessary_setpoints = set(
            [PROPERTY_TEMPERATURE_SUPPLY, PROPERTY_TEMPERATURE_RETURN, PROPERTY_HEAT_DEMAND]
        )
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if necessary_setpoints.issubset(setpoints_set):
            # Set the setpoints
            self._set_supply_temperature(setpoints[PROPERTY_TEMPERATURE_SUPPLY])
            self._set_return_temperature(setpoints[PROPERTY_TEMPERATURE_RETURN])
            self._set_heat_demand(setpoints[PROPERTY_HEAT_DEMAND])
            # Raise warning if there are more setpoints
            if len(setpoints_set.difference(necessary_setpoints)) > 0:
                warn(
                    f"The setpoints {setpoints_set.difference(necessary_setpoints)}"
                    + f" are not required for the asset {self.asset_name}."
                )
        else:
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

    def simulation_performed(self) -> bool:
        """Check if the simulation has been performed.

        :return bool simulation_performed: True if the simulation has been performed,
            otherwise a ValueError is raised.
        """
        if self.pandapipes_net.res_circ_pump_mass is AttributeError:
            # TODO: Implement specific error
            raise ValueError(f"The pandapipes network {self.pandapipes_net} has no results.")
        else:
            # Retrieve the setpoints
            return True

    def get_setpoints(self) -> Dict:
        """Get the setpoints of the asset.

        :return Dict setpoints: The setpoints of the asset in a dictionary,
            as "property_name": value pairs.
        """
        # Return the setpoints
        temp_supply = self.pandapipes_net.res_junction["t_k"][self.to_junction.index]
        temp_return = self.pandapipes_net.res_junction["t_k"][self.from_junction.index]
        mass_flow = self.pandapipes_net.res_circ_pump_mass["mdot_flow_kg_per_s"][
            self._circ_pump.index
        ]
        heat_demand = mass_flow_and_temperature_to_heat_demand(
            temperature_supply=temp_supply,
            temperature_return=temp_return,
            mass_flow=mass_flow,
            pandapipes_net=self.pandapipes_net,
        )
        return {
            PROPERTY_TEMPERATURE_SUPPLY: temp_supply,
            PROPERTY_TEMPERATURE_RETURN: temp_return,
            PROPERTY_HEAT_DEMAND: heat_demand,
        }

    def update(self) -> None:
        """Update the asset properties to the results from the previous (timestep) simulation.

        Sets the values of the supply temperature, return temperature and heat demand
        to the values of the previous simulation. In addition, the mass flow rate is set
        to the value of the previous simulation.
        """
        if self.simulation_performed():
            # Retrieve the setpoints (Ts, Tr, Qh)
            setpoints = self.get_setpoints()
            # Set the setpoints (Ts, Tr, Qh)
            self.set_setpoints(setpoints)
            # Set massflow
            self._controlled_mass_flow = self.pandapipes_net.res_circ_pump_mass[
                "mdot_flow_kg_per_s"
            ][self._circ_pump.index]

    def write_to_output(self) -> None:
        """Write the output of the asset to the output list.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.

        The output of the asset is a dictionary with the following keys:
        - PROPERTY_HEAT_DEMAND: The heat demand of the asset.
        - PROPERTY_TEMPERATURE_SUPPLY: The supply temperature of the asset.
        - PROPERTY_TEMPERATURE_RETURN: The return temperature of the asset.
        - PROPERTY_PRESSURE_SUPPLY: The supply pressure of the asset.
        - PROPERTY_PRESSURE_RETURN: The return pressure of the asset.
        - PROPERTY_MASSFLOW: The mass flow rate of the asset.
        """
        # Retrieve the general model setpoints (Ts, Tr, Qh)
        setpoints = self.get_setpoints()
        # Retrieve the mass flow (mdot)
        setpoints[PROPERTY_MASSFLOW] = self.pandapipes_net.res_circ_pump_mass["mdot_flow_kg_per_s"][
            self._circ_pump.index
        ]
        # Retrieve the pressure (Ps, Pr)
        setpoints[PROPERTY_PRESSURE_SUPPLY] = self.pandapipes_net.res_junction["p_bar"][
            self.to_junction.index
        ]
        setpoints[PROPERTY_PRESSURE_RETURN] = self.pandapipes_net.res_junction["p_bar"][
            self.from_junction.index
        ]
        # Append dict to output list
        self.output.append(setpoints)


if __name__ == "__main__":
    # Check functionality of the ProductinCluster
    # Create a simple pandapipes network woith a production cluster
    # and a demand cluster.
    import pandapipes as pp

    # Create a pandapipes network
    net = pp.create_empty_network(fluid="water")
    # Demand properties
    Qh_demand1 = 1 * 10e6  # [W]
    mass_flow_demand1 = heat_demand_and_temperature_to_mass_flow(
        thermal_demand=Qh_demand1,
        temperature_supply=DEFAULT_TEMPERATURE,
        temperature_return=DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE,
        pandapipes_net=net,
    )
    # Create junctions
    junc_list = [
        Junction(
            pandapipes_net=net,
            pn_bar=5.0,
            tfluid_k=300.0,
            height_m=0.0,
            geodata=geo_sub,
            name="junc0_demand_cluster01",
        )
        for junc_idx, geo_sub in enumerate([[0, 0], [4, 0], [0, 1], [4, 1], [0, 2], [4, 2]])
    ]
    # Create pipes
    pipe_list = pp.create_pipes_from_parameters(
        net,
        from_junctions=[0, 2, 1, 3],
        to_junctions=[2, 4, 3, 5],
        length_km=[1, 1, 1, 1],
        diameter_m=DEFAULT_DIAMETER,
        sections=1,
        name=["pipe_junc0_junc2", "pipe_junc2_junc4", "pipe_junc1_junc3", "pipe_junc3_junc5"],
    )
    # Create source
    sub_junc_list = pp.create_junctions(
        net,
        2,
        pn_bar=5.0,
        tfluid_k=300.0,
        height_m=0.0,
        name=["junc01_demand_cluster01", "junc02_demand_cluster01"],
        geodata=[[2, 1], [3, 1]],
    )
    pp.create_flow_control(
        net,
        from_junction=2,
        to_junction=sub_junc_list[0],
        controlled_mdot_kg_per_s=-mass_flow_demand1,
        diameter_m=DEFAULT_DIAMETER,
        control_active=False,
        in_service=True,
    )
    pp.create_heat_exchanger(
        net,
        from_junction=sub_junc_list[0],
        to_junction=sub_junc_list[1],
        diameter_m=DEFAULT_DIAMETER,
        qext_w=Qh_demand1,
        name="heat_exchanger_demand_cluster01",
    )
    pp.create_pipe_from_parameters(
        net,
        from_junction=sub_junc_list[1],
        to_junction=3,
        length_km=1e-3,
        diameter_m=DEFAULT_DIAMETER,
        name="demand_cluster01",
    )
    # Create production cluster
    production_list = [[junc_list[1], junc_list[0]], [junc_list[5], junc_list[4]]]
    production_cluster_list = []
    for id, sub_list in enumerate(production_list):
        # Set mass flow
        if id == 0:
            control_mass_flow = True
        else:
            control_mass_flow = False
        # Create cluster
        production_cluster_list.append(
            ProductionCluster(
                pandapipes_net=net,
                asset_name=f"ProductionCluster{id}",
                asset_id=f"ProductionCluster{id}",
                from_junction=sub_list[0],
                to_junction=sub_list[1],
                thermal_production_required=-Qh_demand1 / 2.0,
                temperature_supply=DEFAULT_TEMPERATURE,
                internal_diameter=DEFAULT_DIAMETER,
                pressure_supply=5.0,
                control_mass_flow=control_mass_flow,
                height_m=0.0,
            )
        )
    # Solve the network
    pp.pipeflow(net)
    production_cluster_list[0].get_output()
    # Check pipe flow
    output_pipes = pd.merge(net.pipe["name"], net.res_pipe, left_index=True, right_index=True)[
        ["name", "t_from_k", "t_to_k", "mdot_from_kg_per_s", "v_mean_m_per_s"]
    ].round(2)
    print(output_pipes)
    # Check Energy
    output_heat_exchangers = pd.merge(
        net.heat_exchanger["name"], net.res_heat_exchanger, left_index=True, right_index=True
    )
    output_heat_exchangers["qext_w"] = (
        (output_heat_exchangers["t_to_k"] - output_heat_exchangers["t_from_k"])
        * output_heat_exchangers["mdot_to_kg_per_s"]
        * net.fluid.get_heat_capacity(output_heat_exchangers["t_from_k"])
    )
    output_heat_exchangers = output_heat_exchangers.round(2)
    print(output_heat_exchangers)
    # Check circ_pump_pressure
    output_circ_pump_pressure = pd.merge(
        net.circ_pump_mass["name"],
        net.res_circ_pump_mass,
        left_index=True,
        right_index=True,
    ).round(2)
    output_circ_pump_pressure["qext_w"] = (
        (net.res_junction.iloc[3]["t_k"] - net.res_junction.iloc[0]["t_k"])
        * net.res_circ_pump_mass.iloc[0]["mdot_flow_kg_per_s"]
        * net.fluid.get_heat_capacity(net.res_junction.iloc[0]["t_k"])
    )
    # Combine junctions
    output_junctions = pd.merge(
        net.junction["name"], net.res_junction, left_index=True, right_index=True
    ).round(2)
    print(output_junctions)
    # Check sum of qext_w
    print(
        f"Percentage error of heat: {(output_heat_exchangers['qext_w'].sum() + output_circ_pump_pressure['qext_w'].sum())/Qh_demand1*100:.2f} %"
    )
    test = 0
