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

"""Define default values and names for assets."""

# Default values
DEFAULT_DIAMETER = 1.2  # [m]
DEFAULT_PRESSURE = 5.0  # [bar]
DEFAULT_PRESSURE_DIFFERENCE = 0.5  # [bar]
DEFAULT_TEMPERATURE = 300.0  # [K]
DEFAULT_TEMPERATURE_DIFFERENCE = 30.0  # [K]
DEFAULT_NODE_HEIGHT = 0.0  # [m]
DEFAULT_MASS_FLOW_RATE = 1.0  # [kg/s]

# Default names
PROPERTY_HEAT_DEMAND = "heat_demand"
PROPERTY_TEMPERATURE_SUPPLY = "temperature_supply"
PROPERTY_TEMPERATURE_RETURN = "temperature_return"
PROPERTY_PRESSURE_SUPPLY = "pressure_supply"
PROPERTY_PRESSURE_RETURN = "pressure_return"
PROPERTY_MASSFLOW = "mass_flow"
PROPERTY_VOLUMEFLOW = "volume_flow"
PROPERTY_THERMAL_POWER = "thermal_power"
