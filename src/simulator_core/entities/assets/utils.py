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

"""Utility functions for assets."""
from enum import IntEnum
from typing import List

from numpy import log
from pandapipes import pandapipesNet

from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject


def heat_demand_and_temperature_to_mass_flow(
    thermal_demand: float,
    temperature_supply: float,
    temperature_return: float,
    pandapipes_net: pandapipesNet,
) -> float:
    """Calculate the mass flow rate that is required to meet the thermal demand.

    :param float thermal_demand: The thermal demand of the asset. The thermal demand should be
        supplied in Watts.
    :param float temperature_supply: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. The supply temperature is used to calculate
        the specific heat capacity of the fluid.
    :param float temeprature_return: The temperature that the asset receives from the
        "from_junction". The temperature should be supplied in Kelvin.
    :param pandapipesNet net: The pandapipes network used to calculate the specific heat capacity.
    """
    heat_capacity = pandapipes_net.fluid.get_heat_capacity(
        (temperature_return + temperature_supply) / 2
    )
    return thermal_demand / ((temperature_supply - temperature_return) * float(heat_capacity))


def mass_flow_and_temperature_to_heat_demand(
    temperature_supply: float,
    temperature_return: float,
    mass_flow: float,
    pandapipes_net: pandapipesNet,
) -> float:
    """Calculate the thermal demand that is met by the mass flow rate.

    :param float temperature_supply: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. The supply temperature is used to calculate
        the specific heat capacity of the fluid.
    :param float temeprature_return: The temperature that the asset receives from the
        "from_junction". The temperature should be supplied in Kelvin.
    :param float mass_flow: The mass flow rate that is used to meet the thermal demand. The mass
        flow rate should be supplied in kg/s.
    :param pandapipesNet net: The pandapipes network used to calculate the specific heat capacity.
    """
    heat_capacity = pandapipes_net.fluid.get_heat_capacity(
        (temperature_return + temperature_supply) / 2
    )
    return mass_flow * (temperature_supply - temperature_return) * float(heat_capacity)


def get_thermal_conductivity_table(esdl_asset: EsdlAssetObject) -> (List[float], List[float]):
    """Retrieve the thermal conductivity table of the asset.

    :param EsdlAssetObject esdl_asset: The asset of which the heat transfer table should be
        retrieved.
    :return: The diameters and thermal conductivities of the asset in a tuple with the diameters
        as the first element and the thermal conductivities as the second element. Each element
        represents a layer of the asset.
    """
    # create heat transfer table
    layer_thicknesses = []
    diameters = []
    heat_coef = []
    if esdl_asset.esdl_asset.material is not None:
        if hasattr(esdl_asset.esdl_asset.material, "component"):
            material_object = esdl_asset.esdl_asset.material.component
        elif hasattr(esdl_asset.esdl_asset.material, "reference"):
            material_object = esdl_asset.esdl_asset.material.reference.component
        else:
            raise NotImplementedError("Unknown material type or reference.")
        # Append initial internal diameter
        diameters.append(esdl_asset.esdl_asset.innerDiameter)
        # Loop over material object
        for layer in material_object:
            layer_thicknesses.append(layer.layerWidth * 2)
            diameters.append(sum(layer_thicknesses) + esdl_asset.esdl_asset.innerDiameter)
            heat_coef.append(layer.matter.thermalConductivity)
    return diameters, heat_coef


def calculate_inverse_heat_transfer_coefficient(
    inner_diameter: float, outer_diameter: float, thermal_conductivity: float
) -> float:
    """Calculate the inverse heat transfer coefficient of a pipe.

    :param thermal_conductivity: Thermal conductivity of the pipe material in W/(m K)
    :return: Inverse heat transfer coefficient in W/(m^2 K)
    """
    return (inner_diameter * log(outer_diameter / inner_diameter)) / (2 * thermal_conductivity)


class Port(IntEnum):
    """Simple enumeration class to set if it is In (from) or out(to) port of asset."""

    In = 0
    Out = 1
