from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandapipes import (
    create_circ_pump_const_mass_flow,
    create_flow_control,
    create_junction,
    pandapipesNet,
)

from simulator_core.entities.assets.asset_abstract import AssetAbstract

DEFAULT_DIAMETER = 1.2  # [m]
DEFAULT_PRESSURE = 5.0  # [bar]
DEFAULT_NET_PRESSURE = 10.0  # [bar]
DEFAULT_TEMPERATURE = 300.0  # [K]
DEFAULT_TEMPERATURE_DIFFERENCE = 30.0  # [K]
DEFAULT_NODE_HEIGHT = 0.0  # [m]


class Junction:
    """Wrapper class for pandapipes junctions."""

    def __init__(
        self,
        pn_bar: float = 5.0,
        tfluid_k: float = 300.0,
        height_m: float = 0.0,
        geodata: List = None,
        name: str = None,
        in_service: bool = True,
        index: int = None,
    ):
        """Initialize a Junction object."""
        self.pn_bar = pn_bar
        self.tfluid_k = tfluid_k
        self.height_m = height_m
        self.geodata = geodata
        self.name = name
        self.in_service = in_service
        self.index = index

    def create(self, pandapipes_net: pandapipesNet) -> None:
        """Register the junction in the pandapipes network."""
        self.index = create_junction(
            net=pandapipes_net,
            pn_bar=self.pn_bar,
            tfluid_k=self.tfluid_k,
            height_m=self.height_m,
            geodata=self.geodata,
            name=self.name,
            in_service=self.in_service,
        )


class ControlValve:
    """Wrapper class for pandapipes control valves."""

    def __init__(
        self,
        from_junction: int,
        to_junction: int,
        controlled_mdot_kg_per_s: float,
        diameter_m: float,
        control_active: bool = False,
        in_service: bool = True,
        name: str = None,
        index: int = None,
    ):
        """Initialize a ControlValve object."""
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.controlled_mdot_kg_per_s = controlled_mdot_kg_per_s
        self.diameter_m = diameter_m
        self.control_active = control_active
        self.in_service = in_service
        self.name = name
        self.index = index

    def create(self, pandapipes_net: pandapipesNet) -> None:
        """Register the control valve in the pandapipes network."""
        self.index = create_flow_control(
            net=pandapipes_net,
            from_junction=self.from_junction,
            to_junction=self.to_junction,
            controlled_mdot_kg_per_s=self.controlled_mdot_kg_per_s,
            diameter_m=self.diameter_m,
            control_active=self.control_active,
            in_service=self.in_service,
            name=self.name,
        )


class CirculationPumpConstantMass:
    """Wrapper class for pandapipes circulation pumps with constant mass flow."""

    def __init__(
        self,
        from_junction: int,
        to_junction: int,
        p_to_junction: float,
        mdot_kg_per_s: float,
        t_to_junction: float,
        in_service: bool = True,
        name: str = None,
        index: int = None,
    ):
        """Initialize a CirculationPumpConstantMass object."""
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.p_to_junction = p_to_junction
        self.mdot_kg_per_s = mdot_kg_per_s
        self.t_to_junction = t_to_junction
        self.in_service = in_service
        self.name = name
        self.index = index

    def create(self, pandapipes_net: pandapipesNet) -> None:
        self.index = create_circ_pump_const_mass_flow(
            net=pandapipes_net,
            return_junction=self.from_junction,
            flow_junction=self.to_junction,
            p_flow_bar=self.p_to_junction,
            mdot_flow_kg_per_s=self.mdot_kg_per_s,
            t_flow_k=self.t_to_junction,
            in_service=self.in_service,
            name=self.name,
            index=self.index,
        )


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
        thermal_production_required: float,
        temperature_supply: float,
        temperature_return: float = np.NaN,
        height_m: float = DEFAULT_NODE_HEIGHT,
        internal_diameter: float = DEFAULT_DIAMETER,
        pressure_supply: float = DEFAULT_PRESSURE,
        control_mass_flow: bool = False,
    ):
        """Initialize a ProductionCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param int from_junction: The junction where the asset starts.
        :param int to_junction: The junction where the asset ends.
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
        # Objects of the asset
        self._intermediate_junction = None
        self._circ_pump = None
        self._flow_control = None

        # Output of the asset
        # TODO: we need to discuss output!
        self.from_junction_temperature = None
        self.to_junction_temperature = None
        self.from_junction_pressure = None
        self.to_junction_pressure = None
        self.mass_flow = None
        self.thermal_production = None

    # TODO: How do we carry the pandapipes net?
    def create(self, pandapipes_net: pandapipesNet) -> None:
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
            pn_bar=self.pressure_supply,
            tfluid_k=self.temperature_supply,
            height_m=self.height_m,
            name=f"intermediate_junction_{self.asset_name}",
            geodata=list(
                pandapipes_net.junction_geodata.iloc[
                    [self.from_junction, self.to_junction]
                ].values.mean(axis=0)
            ),
        )
        self._intermediate_junction.create(pandapipes_net)
        # Create the pump to supply pressure and or massflow
        self._circ_pump = CirculationPumpConstantMass(
            from_junction=self.from_junction,
            to_junction=self._intermediate_junction.index,
            p_to_junction=self.pressure_supply,
            mdot_kg_per_s=heat_demand_and_temperature_to_mass_flow(
                thermal_demand=self.thermal_production_required,
                temperature_supply=self.temperature_supply,
                temperature_return=self.temperature_return,
                net=pandapipes_net,
            ),
            t_to_junction=self.temperature_supply,
            name=f"circ_pump_{self.asset_name}",
            in_service=True,
        )
        self._circ_pump.create(pandapipes_net)
        # Create the control valve
        self._flow_control = ControlValve(
            from_junction=self._intermediate_junction.index,
            to_junction=self.to_junction,
            controlled_mdot_kg_per_s=heat_demand_and_temperature_to_mass_flow(
                thermal_demand=self.thermal_production_required,
                temperature_supply=self.temperature_supply,
                temperature_return=self.temperature_return,
                net=pandapipes_net,
            ),
            diameter_m=self.internal_diameter,
            control_active=self.control_mass_flow,
            in_service=True,
            name=f"flow_control_{self.asset_name}",
        )
        self._flow_control.create(pandapipes_net)

    def get_output(self, pandapipes_net: pandapipesNet) -> pd.DataFrame:
        """Get the output of the asset."""
        (
            self.from_junction_pressure,
            self.from_junction_temperature,
        ) = pandapipes_net.res_junction.loc[self.from_junction, ["p_bar", "t_k"]]
        (self.to_junction_pressure, self.to_junction_temperature) = pandapipes_net.res_junction.loc[
            self.to_junction, ["p_bar", "t_k"]
        ]
        self.mass_flow = pandapipes_net.res_flow_control.loc[
            self._flow_control.index, "mdot_from_kg_per_s"
        ]
        self.thermal_production = (
            self.mass_flow
            * (self.to_junction_temperature - self.from_junction_temperature)
            * pandapipes_net.fluid.get_heat_capacity(self.from_junction_temperature)
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
