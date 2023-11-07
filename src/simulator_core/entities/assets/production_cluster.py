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


class ProductionCluster(AssetAbstract):
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
        ) = self.pandapipes_net.res_junction.loc[self.from_junction, ["p_bar", "t_k"]]
        (
            self.to_junction_pressure,
            self.to_junction_temperature,
        ) = self.pandapipes_net.res_junction.loc[self.to_junction, ["p_bar", "t_k"]]
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
