from pandapipes import (
    create_circ_pump_const_pressure,
    create_ext_grid,
    create_flow_control,
    create_heat_exchanger,
    create_junction,
    create_pipe_from_parameters,
    create_pressure_control,
    pandapipesNet,
)

from simulator_core.entities.assets.asset_abstract import AssetAbstract

DEFAULT_DIAMETER = 1.2  # [m]
DEFAULT_PRESSURE = 5.0  # [bar]
DEFAULT_NET_PRESSURE = 10.0  # [bar]
DEFAULT_TEMPERATURE = 300.0  # [K]
DEFAULT_TEMPERATURE_DIFFERENCE = 30.0  # [K]
DEFAULT_NODE_HEIGHT = 0.0  # [m]


def heat_demand_and_temperature_to_mass_flow(
    thermal_demand: float, temperature_supply: float, temperature_return: float, net: pandapipesNet
) -> float:
    """Calculate the mass flow rate that is required to meet the thermal demand.

    :param float thermal_demand: The thermal demand of the asset. The thermal demand should be supplied in Watts.
    :param float temperature_supply: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. The supply temperature is used to calculate the specific heat
        capacity of the fluid.
    :param float temeprature_return: The temperature that the asset receives from the "from_junction".
        The temperature should be supplied in Kelvin.
    :param pandapipesNet net: The pandapipes network used to calculate the specific heat capacity.
    """
    return thermal_demand / (
        (temperature_supply - temperature_return)
        * float(net.fluid.get_heat_capacity(temperature_supply))
    )


class ProductionCluster:
    """
    A ProductionCluster represents an asset that produces heat.
    """

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        from_junction: int,
        to_junction: int,
        thermal_allocation: float,
        temperature_supply: float,
        temperature_return: float = None,
        height_m: float = DEFAULT_NODE_HEIGHT,
        internal_diameter: float = DEFAULT_DIAMETER,
        pressure_allocation: float = DEFAULT_PRESSURE,
        net_pressure: float = DEFAULT_NET_PRESSURE,
        set_pressure: bool = False,
    ):
        """Initialize a ProductionCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param int from_junction: The junction where the asset starts.
        :param int to_junction: The junction where the asset ends.
        :param float thermal_allocation: The thermal allocation of the asset.
            The thermal allocation should be supplied in Watts.
        :param float temperature_supply: The temperature that the asset delivers to the "to_junction".
            The temperature should be supplied in Kelvin.
        :param float temeprature_return: The temperature that the asset receives from the "from_junction".
            The temperature should be supplied in Kelvin. If the value is not supplied it defaults to
            "temperature_supply" - DEFAULT_TEMPERATURE_DIFFERENCE.
        :param float height_m: The height of the junctions. The height should be supplied in meters,
            it defaults to DEFAULT_NODE_HEIGHT.
        :param float internal_diameter: The internal diameter of the pipe.
            The internal diameter should be supplied in meters, it defaults to DEFAULT_DIAMETER.
        :param float pressure_allocation: The pressure that the asset delivers to the "to_junction". The pressure
            should be supplied in bar, it defaults to DEFAULT_PRESSURE.
        :param float net_pressure: The net pressure that the asset delivers to the "to_junction". The net pressure
            should be supplied in bar, it defaults to DEFAULT_NET_PRESSURE.
        :param bool set_pressure: If True, a pandapipes "Circulation Pump Pressure" is used to set the pressure
            of the system. If False, a pandapipes "Control Valve" is used to set the mass flow rate of the system.
        """
        # Define the asset properties
        self.asset_name = asset_name
        self.asset_id = asset_id
        # TODO: Do we need to carry the junction ids?
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.internal_diameter = internal_diameter
        self.height_m = height_m
        # DemandCluster thermal and mass flow specifications
        self.thermal_allocation = thermal_allocation
        self.temperature_supply = temperature_supply
        self.temperature_return = (
            temperature_supply - DEFAULT_TEMPERATURE_DIFFERENCE
            if temperature_return is None
            else temperature_return
        )
        # DemandCluster pressure specifications
        self.pressure_allocation = pressure_allocation
        self.net_pressure = net_pressure
        self.set_pressure = set_pressure
        # Object references
        self.pandapipes_objects = []

    def _productioncluster_mass_flow(self, pandapipes_net: pandapipesNet) -> pandapipesNet:
        """Create a mass flow representation of the production cluster.

        The mass flow representation of the production cluster consists of a heat exchanger, a pipe and a control valve.
        The heat exchanger is used to set the thermal allocation of the production cluster. The pipe is used to connect
        the from_junction to the heat exchanger. The pipe is required to allow for the computation of the mixing
        temperature of the from_junction. The control valve is used to set the mass flow rate of the production cluster.
        """
        # Create the temperature setpoint with a derived mass flow
        pipe_to_hx = create_junction(
            pandapipes_net,
            pn_bar=DEFAULT_NET_PRESSURE,
            tfluid_k=DEFAULT_TEMPERATURE,
            height_m=self.height_m,
            name=f"{self.asset_name}_intermediate_junction",
            index=None,
            in_service=not self.set_pressure,
            geodata=None,
        )
        hx_to_valve = create_junction(
            pandapipes_net,
            pn_bar=DEFAULT_NET_PRESSURE,
            tfluid_k=DEFAULT_TEMPERATURE,
            height_m=self.height_m,
            name=f"{self.asset_name}_intermediate_junction",
            index=None,
            in_service=not self.set_pressure,
            geodata=None,
        )
        # Create the heat exchanger
        create_heat_exchanger(
            pandapipes_net,
            from_junction=pipe_to_hx,
            to_junction=hx_to_valve,
            diameter_m=self.internal_diameter,
            qext_w=self.thermal_allocation,
            in_service=not self.set_pressure,
            name=f"{self.asset_name}_heat_exchanger",
        )
        # Createa a pipe that is connected to the heat exchanger. A small resistance element is needed
        # as otherwise the heat exchanger imposes the temperature at a node, which disables the mixing
        # behavior of the node.
        create_pipe_from_parameters(
            pandapipes_net,
            from_junction=self.from_junction,
            to_junction=pipe_to_hx,
            length_km=1e-3,
            diameter_m=self.internal_diameter,
            sections=1,
            name=f"{self.asset_name}_intermediate_pipe",
            in_service=not self.set_pressure,
        )
        # Create the control valve that sets the mass flow
        create_flow_control(
            pandapipes_net,
            from_junction=hx_to_valve,
            to_junction=self.to_junction,
            controlled_mdot_kg_per_s=heat_demand_and_temperature_to_mass_flow(
                thermal_demand=self.thermal_allocation,
                temperature_supply=self.temperature_supply,
                temperature_return=self.temperature_return,
                net=pandapipes_net,
            ),
            diameter_m=self.internal_diameter,
            control_active=True,
            name=f"{self.asset_name}_flow_control",
            in_service=not self.set_pressure,
        )
        return pandapipes_net

    # TODO: How do we carry the pandapipes net?
    def register_pandapipes(self, pandapipes_net: pandapipesNet) -> pandapipesNet:
        """Create a representation of the asset in pandapipes.

        The ProductionCluster asset contains multiple pandapipes components. It can operate in either a "pressure" or
        "temperature" mode.

        In the "pressure" mode the components are:
        1) A "Circulation Pump Pressure" that sets the pressure of the system. The circulation pump can be used to
        increase the temperature over the component, which effectively increases the thermal allocation of the asset.

        In the "temperature" mode the components are:
        1) A "Heat Exchanger" that feeds the required thermal allocation into the system.
        2) A "Pipe" that connects to "Heat Exchanger" and the external system through an intermediate node.
        3) A "Control Valve" that sets the mass flow rate of the system.
        """
        # Create the mass flow representation of the production cluster
        pandapipes_net = self._productioncluster_mass_flow(pandapipes_net)
        # Create the pressure control valve to define the pressure
        create_circ_pump_const_pressure(
            pandapipes_net,
            return_junction=self.from_junction,
            flow_junction=self.to_junction,
            p_flow_bar=self.net_pressure,
            plift_bar=self.pressure_allocation,
            t_flow_k=self.temperature_supply,
            type="auto",
            name=f"{self.asset_name}_circ_pump",
        )
        return pandapipes_net


if __name__ == "__main__":
    # Check functionality of the ProductionCluster
    # Create a simple pandapipes network with a production cluster
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
        net=net,
    )
    # Create 4 junctions
    junc_list = pp.create_junctions(net, 4, pn_bar=5.0, tfluid_k=300.0, geodata=None, height_m=0.0)
    # Create 2 pipes
    pipe_list = pp.create_pipes_from_parameters(
        net,
        from_junctions=junc_list.reshape([2, 2])[:, 0].tolist(),
        to_junctions=junc_list.reshape([2, 2])[:, 1].tolist(),
        length_km=[1, 2],
        diameter_m=DEFAULT_DIAMETER,
        sections=1,
    )
    # Create demand cluster
    # Create demand cluster: DemandCluster 1
    sub_junc_list = pp.create_junctions(
        net, 2, pn_bar=5.0, tfluid_k=300.0, geodata=None, height_m=0.0
    )
    pp.create_flow_control(
        net,
        from_junction=junc_list[1],
        to_junction=sub_junc_list[0],
        controlled_mdot_kg_per_s=mass_flow_demand1,
        diameter_m=DEFAULT_DIAMETER,
        control_active=True,
        in_service=True,
    )
    pp.create_heat_exchanger(
        net,
        from_junction=sub_junc_list[0],
        to_junction=sub_junc_list[1],
        diameter_m=DEFAULT_DIAMETER,
        qext_w=Qh_demand1,
    )
    pp.create_pipe_from_parameters(
        net,
        from_junction=sub_junc_list[1],
        to_junction=junc_list[2],
        length_km=1e-3,
        diameter_m=DEFAULT_DIAMETER,
    )
    # Create production cluster
    production_cluster = ProductionCluster(
        asset_name="ProductionCluster1",
        asset_id="ProductionCluster1",
        from_junction=junc_list[-1],
        to_junction=junc_list[0],
        thermal_allocation=Qh_demand1,
        temperature_supply=DEFAULT_TEMPERATURE,
        internal_diameter=DEFAULT_DIAMETER,
        pressure_allocation=5.0,
        net_pressure=10.0,
        set_pressure=True,
        height_m=0.0,
    )
    production_cluster.register_pandapipes(net)
    # Solve the network
    pp.pipeflow(net, mode="all")
