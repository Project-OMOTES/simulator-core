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
from typing import Any, Tuple

import pandas as pd
from esdl import esdl
from simulator_core.entities.utility.influxdb_reader import get_data_from_profile

logger = logging.getLogger(__name__)


class EsdlAssetObject:
    """
    Class to hold an esdl asset and convert it to local class objects.

    Conversion is done based on the classes in the conversion_dict.
    """

    esdl_asset: esdl.Asset

    def __init__(self, asset: esdl.Asset) -> None:
        """
        Constructor for EsdlAssetObject class.

        :param asset, esdl.Asset: PyEsdl Asset object
        """
        self.esdl_asset = asset

    def get_property(self, esdl_property_name: str, default_value: Any) -> Tuple[Any, bool]:
        """Get property value from the esdl_asset based on the "ESDL" name.

        :return: Tuple with the value of the property and a boolean indicating whether the property
        was found in the esdl_asset.
        """
        try:
            return getattr(self.esdl_asset, esdl_property_name), True
        except AttributeError:
            return default_value, False

    def get_profile(self) -> pd.DataFrame:
        """Get the profile of the asset."""
        for esdl_port in self.esdl_asset.port:
            if esdl_port.profile:
                return get_data_from_profile(esdl_port.profile[0])
        raise ValueError("No profile found for asset: " + self.esdl_asset.name)
