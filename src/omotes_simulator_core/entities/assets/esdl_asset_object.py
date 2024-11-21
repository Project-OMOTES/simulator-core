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

"""Module containing classes to be able to interact with esdl objects."""
import logging
from typing import Any, Tuple, Type

import pandas as pd
from esdl import esdl
from omotes_simulator_core.entities.utility.influxdb_reader import get_data_from_profile
from omotes_simulator_core.adapter.transforms.transform_utils import PortType, sort_ports, Port


logger = logging.getLogger(__name__)


class EsdlAssetObject:
    """
    Class to hold an esdl asset and convert it to local class objects.

    Conversion is done based on the classes in the CONVERSION_DICT.
    """

    esdl_asset: esdl.Asset

    def __init__(self, asset: esdl.Asset) -> None:
        """
        Constructor for EsdlAssetObject class.

        :param asset, esdl.Asset: PyEsdl Asset object
        """
        self.esdl_asset = asset

    def get_name(self) -> str:
        """Get the name of the asset."""
        return str(self.esdl_asset.name)

    def get_id(self) -> str:
        """Get the id of the asset."""
        return str(self.esdl_asset.id)

    def get_property(self, esdl_property_name: str, default_value: Any) -> Tuple[Any, bool]:
        """Get property value from the esdl_asset based on the 'ESDL' name.

        :param esdl_property_name: The name of the property in the ESDL asset.
        :param default_value: The default value to return if the property has no value.
        :return: Tuple with the value of the property and a boolean indicating whether the property
                was found in the esdl_asset.
        If the property is 0, then should it be False or true?
        """
        try:
            value = getattr(self.esdl_asset, esdl_property_name)
            if value == 0:
                return default_value, False
            return value, True

        except AttributeError:
            return default_value, False

    def get_profile(self) -> pd.DataFrame:
        """Get the profile of the asset."""
        for esdl_port in self.esdl_asset.port:
            if esdl_port.profile:
                return get_data_from_profile(esdl_port.profile[0])
        raise ValueError(f"No profile found for asset: {self.esdl_asset.name}")

    def get_supply_temperature(self, port_type: str) -> float:
        """Get the temperature of the port."""
        for esdl_port in self.esdl_asset.port:
            if isinstance(esdl_port, self.get_port_type(port_type)):
                return get_supply_temperature(esdl_port)
        raise ValueError(f"No port found with type: {port_type} for asset: {self.esdl_asset.name}")

    def get_return_temperature(self, port_type: str) -> float:
        """Get the temperature of the port."""
        for esdl_port in self.esdl_asset.port:
            if isinstance(esdl_port, self.get_port_type(port_type)):
                return get_return_temperature(esdl_port)
        raise ValueError(f"No port found with type: {port_type} for asset: {self.esdl_asset.name}")

    def get_port_ids(self) -> list[str]:
        """Returns a sorted list of the port ids of the asset."""
        list_of_ports = sort_ports(
            [
                Port(
                    port.id,
                    port.name,
                    PortType.IN if isinstance(port, esdl.InPort) else PortType.OUT,
                )
                for port in self.esdl_asset.port
            ]
        )
        return list_of_ports

    def get_port_type(self, port_type: str) -> Type[esdl.Port]:
        """Get the port type of the port."""
        if port_type == "In":
            return esdl.InPort  # type: ignore [no-any-return]
        elif port_type == "Out":
            return esdl.OutPort  # type: ignore [no-any-return]
        else:
            raise ValueError(f"Port type not recognized: {port_type}")

    def get_marginal_costs(self) -> float:
        """Get the marginal costs of the asset."""
        if self.esdl_asset.costInformation is None:
            logger.warning(
                f"No cost information found for asset, Marginal costs set to 0 for: "
                f"{self.esdl_asset.name}"
            )
            return 0
        if self.esdl_asset.costInformation.marginalCosts is None:
            logger.warning(
                f"No marginal costs found for asset, Marginal costs set to 0 for: "
                f"{self.esdl_asset.name}"
            )
            return 0
        return float(self.esdl_asset.costInformation.marginalCosts.value)


def get_return_temperature(esdl_port: esdl.Port) -> float:
    """Get the temperature of the port."""
    return float(esdl_port.carrier.returnTemperature) + 273.15


def get_supply_temperature(esdl_port: esdl.Port) -> float:
    """Get the temperature of the port."""
    return float(esdl_port.carrier.supplyTemperature) + 273.15
