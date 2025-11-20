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
from typing import Any

import pandas as pd
from esdl import esdl

from omotes_simulator_core.adapter.transforms.transform_utils import Port, PortType, sort_ports
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolationMethod,
    ProfileSamplingMethod,
)
from omotes_simulator_core.entities.utility.influxdb_reader import get_data_from_profile

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

    def get_strategy_priority(self) -> int | None:
        """Get the control strategy priority value."""
        if hasattr(self.esdl_asset.controlStrategy, "priority"):
            return int(self.esdl_asset.controlStrategy.priority)
        else:
            return 1

    def get_state(self) -> str:
        """Get state of the asset.

        The options for the asset's state are ENABLED, DISABLED and OPTIONAL. The simulator
        will only use assets that have an ENABLED state.
        """
        return str(self.esdl_asset.state)

    def get_property(self, esdl_property_name: str, default_value: Any) -> Any:
        """Get property value from the esdl_asset based on the 'ESDL' name.

        :param esdl_property_name: The name of the property in the ESDL asset.
        :param default_value: The default value to return if the property has no value.
        :return: Value of the property from the ESDL or the default value if not found.
        """
        # ESDL .eIsSet can be used to check if the property is set.
        if not self.esdl_asset.eIsSet(esdl_property_name):
            # Send message to logger
            logger.warning(
                f"Property {esdl_property_name} is not set for: {self.esdl_asset.name}."
                + f"Returning default value: {default_value}.",
                extra={"esdl_object_id": self.get_id()},
            )
            return default_value
        else:
            return getattr(self.esdl_asset, esdl_property_name, default_value)

    def get_profile(self) -> pd.DataFrame:
        """Get the profile of the asset."""
        for esdl_port in self.esdl_asset.port:
            if esdl_port.profile:
                return get_data_from_profile(esdl_port.profile[0])
        logger.error(
            f"No profile found for asset: {self.esdl_asset.name}",
            extra={"esdl_object_id": self.get_id()},
        )
        raise ValueError(f"No profile found for asset: {self.esdl_asset.name}")

    def get_sampling_method(self) -> ProfileSamplingMethod:
        """Get the interpolation method of the asset."""
        # TODO: Get sampling method from ESDL properties if available
        return ProfileSamplingMethod.DEFAULT

    def get_interpolation_method(self) -> ProfileInterpolationMethod:
        """Get the interpolation method of the asset."""
        # TODO: Get interpolation method from ESDL properties if available
        return ProfileInterpolationMethod.DEFAULT

    # make a function to check temperature for both in and out ports
    def get_temperature(self, port_type: str, temp_type: str) -> float:
        """Get the temperature of the port."""
        for esdl_port in self.esdl_asset.port:
            if isinstance(esdl_port, self.get_port_type(port_type)):
                if temp_type == "Supply":
                    return float(esdl_port.carrier.supplyTemperature) + 273.15
                elif temp_type == "Return":
                    return float(esdl_port.carrier.returnTemperature) + 273.15
        logger.error(
            f"No port found with temperature type: {temp_type} for asset: {self.esdl_asset.name}",
            extra={"esdl_object_id": self.get_id()},
        )
        raise ValueError(
            f"No port found with temperature type: {temp_type} for asset: {self.esdl_asset.name}"
        )

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

    def get_port_type(self, port_type: str) -> type[esdl.Port]:
        """Get the port type of the port."""
        if port_type == "In":
            return esdl.InPort  # type: ignore [no-any-return]
        elif port_type == "Out":
            return esdl.OutPort  # type: ignore [no-any-return]
        else:
            logger.error(
                f"Port type not recognized: {port_type} for asset: {self.esdl_asset.name}",
                extra={"esdl_object_id": self.get_id()},
            )
            raise ValueError(f"Port type not recognized: {port_type}")

    def get_marginal_costs(self) -> float:
        """Get the marginal costs of the asset."""
        if self.esdl_asset.costInformation is None:
            logger.warning(
                f"No cost information found for asset, Marginal costs set to 0 for: "
                f"{self.esdl_asset.name}",
                extra={"esdl_object_id": self.get_id()},
            )
            return 0
        if self.esdl_asset.costInformation.marginalCosts is None:
            logger.warning(
                f"No marginal costs found for asset, Marginal costs set to 0 for: "
                f"{self.esdl_asset.name}",
                extra={"esdl_object_id": self.get_id()},
            )
            return 0
        return float(self.esdl_asset.costInformation.marginalCosts.value)

    def get_number_of_ports(self) -> int:
        """Get the number of ports of the asset."""
        number_of_ports = len(self.esdl_asset.port)

        return number_of_ports

    def get_connected_assets(self, port_id: str) -> list[str]:
        """Get the connected assets of the asset."""
        connected_assets = []
        for esdl_port in self.esdl_asset.port:
            if esdl_port.id == port_id:
                for connection in esdl_port.connectedTo:
                    connected_assets.append(connection.energyasset.id)
                return connected_assets
        raise ValueError(f"No port found with id: {port_id} for asset: {self.esdl_asset.name}")

    def is_heat_transfer_asset(self) -> bool:
        """Check if the asset is a heat exchange asset."""
        return isinstance(self.esdl_asset, esdl.HeatPump) or isinstance(
            self.esdl_asset, esdl.HeatExchange
        )


def get_return_temperature(esdl_port: esdl.Port) -> float:
    """Get the temperature of the port."""
    return float(esdl_port.carrier.returnTemperature) + 273.15


def get_supply_temperature(esdl_port: esdl.Port) -> float:
    """Get the temperature of the port."""
    return float(esdl_port.carrier.supplyTemperature) + 273.15
