import numpy as np
import pandas as pd
from pandapipes import pandapipesNet

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.junction import Junction
from simulator_core.entities.assets.pump import CirculationPumpConstantMass
from simulator_core.entities.assets.utils import \
    heat_demand_and_temperature_to_mass_flow
from simulator_core.entities.assets.valve import ControlValve

# TODO: Move this to a config file; but where?

DEFAULT_DIAMETER = 1.2  # [m]
DEFAULT_PRESSURE = 5.0  # [bar]
DEFAULT_NET_PRESSURE = 10.0  # [bar]
DEFAULT_TEMPERATURE = 300.0  # [K]
DEFAULT_TEMPERATURE_DIFFERENCE = 30.0  # [K]
DEFAULT_NODE_HEIGHT = 0.0  # [m]


class ProductionCluster:
    """
    A ProductionCluster represents an asset that produces heat.
    """

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

        # Output of the asset
        # TODO: we need to discuss output!
        self.from_junction_temperature = np.NaN
        self.to_junction_temperature = np.NaN
        self.from_junction_pressure = np.NaN
        self.to_junction_pressure = np.NaN
        self.mass_flow = np.NaN
        self.thermal_production = np.NaN

    # TODO: How do we carry the pandapipes net?
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


    def get_output(self) -> pd.DataFrame:
        """Get the output of the asset."""
        (
            self.from_junction_pressure,
            self.from_junction_temperature,
        ) = self.pandapipes_net.res_junction.loc[self.from_junction.index, ["p_bar", "t_k"]]
        (
            self.to_junction_pressure,
            self.to_junction_temperature,
        ) = self.pandapipes_net.res_junction.loc[self.to_junction.index, ["p_bar", "t_k"]]
        self.mass_flow = self.pandapipes_net.res_flow_control.loc[
            self._flow_control.index, "mdot_from_kg_per_s"
        ]
        self.thermal_production = (
            self.mass_flow
            * (self.to_junction_temperature - self.from_junction_temperature)
            * self.pandapipes_net.fluid.get_heat_capacity(self.from_junction_temperature)
        )
        # Create output dataframe
        output = pd.DataFrame(
            {
                "from_junction_temperature (K)": self.from_junction_temperature,
                "from_junction_pressure (K)": self.from_junction_pressure,
                "to_junction_pressure (bar)": self.to_junction_pressure,
                "to_junction_temperature (bar)": self.to_junction_temperature,
                "mass_flow (kg/s)": self.mass_flow,
                "thermal_production (W)": self.thermal_production,
            },
            index=[self.asset_name],
        )
        return output

if __name__ == "__main__":
    # Check functionality of the ProductinCluster
    # Create a simple pandapipes network woith a production cluster
    # and a demand cluster.
    import pandapipes as pp
    import pandas as pd

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
    junc_list = [Junction(
        pandapipes_net=net,
        pn_bar=5.0,
        tfluid_k=300.0,
        height_m=0.0,
        geodata=geo_sub,
        name="junc0_demand_cluster01",
    ) for junc_idx, geo_sub in enumerate([[0, 0], [4, 0], [0, 1], [4, 1], [0, 2], [4, 2]])]
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
