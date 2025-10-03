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

import numpy as np

from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props


def heat_demand_and_temperature_to_mass_flow(
    thermal_demand: float, temperature_in: float, temperature_out: float
) -> float:
    """Calculate the mass flow rate that is required to meet the thermal demand.

    :param float thermal_demand: The thermal demand of the asset. The thermal demand should be
        supplied in Watts.
    :param float temperature_out: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. This temperature is used to calculate
        the specific heat capacity of the fluid.
    :param float temperature_in: The temperature that the asset receives from the
        "from_junction". The temperature should be supplied in Kelvin.
    """
    heat_capacity = fluid_props.get_heat_capacity((temperature_in + temperature_out) / 2)
    return thermal_demand / ((temperature_out - temperature_in) * float(heat_capacity))


def mass_flow_and_temperature_to_heat_demand(
    temperature_out: float,
    temperature_in: float,
    mass_flow: float,
) -> float:
    """Calculate the thermal demand that is met by the mass flow rate.

    :param float temperature_out: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. The temperature supplied is used to calculate
        the specific heat capacity of the fluid.
    :param float temperature_in: The temperature that the asset receives from the
        "from_junction". The temperature should be supplied in Kelvin.
    :param float mass_flow: The mass flow rate that is used to meet the thermal demand. The mass
        flow rate should be supplied in kg/s.
    """
    internal_energy1 = fluid_props.get_ie(temperature_in)
    internal_energy2 = fluid_props.get_ie(temperature_out)
    return mass_flow * (internal_energy1 - internal_energy2)


def get_thermal_conductivity_table(esdl_asset: EsdlAssetObject) -> tuple[list[float], list[float]]:
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
    inner_diameter: np.ndarray, outer_diameter: np.ndarray, thermal_conductivity: np.ndarray
) -> np.ndarray:
    """Calculate the inverse heat transfer coefficient of a pipe.

    :param inner_diameter: Inner diameter of the pipe in m
    :param outer_diameter: Outer diameter of the pipe in m
    :param thermal_conductivity: Thermal conductivity of the pipe material in W/(m K)
    :return: Inverse heat transfer coefficient in W/(m^2 K)
    """
    return np.array(
        (inner_diameter * np.log(outer_diameter / inner_diameter)) / (2.0 * thermal_conductivity)
    )


class Port(IntEnum):
    """Simple enumeration class to set if it is In (from) or out(to) port of asset."""

    In = 0
    Out = 1


def sign_output(port_number: int) -> int:
    """Give the multiplication factor to correct the output.

    The mass flow rate on the in ports is negative, while it should be positive. This
    function returns the multiplication factor to correct the output. It is either -1 for odd ports
    or 1 for even ports. This assumes that the even ports are in ports and the odd ports are out
    ports.

    :param int port_number: The port number of the asset.
    :return: The multiplication factor for the output.
    """
    return -1 + 2 * (port_number % 2)


def celcius_to_kelvin(temperature: float) -> float:
    """Convert Celcius to Kelvin.

    :param temperature: temperature in C
    :return: temperature in K
    """
    return temperature + 273.15


def kelvin_to_celcius(temperature: float) -> float:
    """Convert Kelvin to Celcius.

    :param temperature: temperature in K
    :return: temperature in C
    """
    return temperature - 273.15
