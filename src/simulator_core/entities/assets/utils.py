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

from pandapipes import pandapipesNet


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


def mass_flow_to_volume_flow(
        mass_flowrate: float,
        temperature_fluid: float,
        pandapipes_net: pandapipesNet,
) -> float:
    """Calculate the volume flowrate from mass flowrate.

    :param float mass_flowrate: the mass flowrate in kg/s
    :param float temperature_fluid: the fluid temperature in K
    :param pandapipesNet net: The pandapipes network used to calculate the specific density.

    :return float volume_flowrate: the volume flowrate in m3/h
    """
    density_fluid = pandapipes_net.fluid.get_density(temperature_fluid)
    volume_flowrate = mass_flowrate * 3600 / density_fluid

    return volume_flowrate


def volume_flow_to_mass_flow(
        volume_flowrate: float,
        temperature_fluid: float,
        pandapipes_net: pandapipesNet,
) -> float:
    """Calculate the mass flowrate from volume flowrate.

    :param float volume_flowrate: the volume flowrate in m3/h
    :param float temperature_fluid: the fluid temperature in K
    :param pandapipesNet net: The pandapipes network used to calculate the specific density.

    :return float mass_flowrate: the mass flowrate in kg/s
    """
    density_fluid = pandapipes_net.fluid.get_density(temperature_fluid)
    mass_flowrate = volume_flowrate / 3600 * density_fluid

    return mass_flowrate


class Port(IntEnum):
    """Simple enumeration class to set if it is In (from) or out(to) port of asset."""

    In = 0
    Out = 1
