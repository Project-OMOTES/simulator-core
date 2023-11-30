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
from dataclasses import dataclass

from esdl import esdl

from simulator_core.adapter.transforms.string_to_esdl import StringEsdlAssetMapper

logger = logging.getLogger(__name__)


@dataclass
class EsdlKey:
    """Class to hold the name and default value of an esdl key.

    :param name: str the name of the key
    :param default: any the default value of the key
    """

    name: str
    default: any


ASSET_DICT = {
    "producer": {},
    "consumer": {},
    "pipe": {
        "length": EsdlKey(name="length", default=0.0),
        "roughness": EsdlKey(name="roughness", default=0.0),
        "inner diameter": EsdlKey(name="innerDiameter", default=0.0),
        "outer diameter": EsdlKey(name="outerDiameter", default=0.0),
        "material": EsdlKey(name="material", default=""),
    },
}


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
        self.asset_specific_parameters = self.get_property_dict_for_asset()

    def get_property_dict_for_asset(self) -> dict:
        """
        Get the properties of the ESDL asset required for the simulation.

        :return: dict of properties
        """
        # Retrieve the entinty type of the asset
        asset_type_string = StringEsdlAssetMapper().to_entity(type(self.esdl_asset))
        return ASSET_DICT[asset_type_string]

    def get_asset_parameters(self) -> dict:
        """
        Get the parameters of the asset.

        :return: dict of parameters
        """
        parameters = {}
        for parameter_key, esdl_key in self.asset_specific_parameters.items():
            try:
                parameters[parameter_key] = getattr(self.esdl_asset, esdl_key.name)
            except AttributeError:
                logger.warning(f"Attribute {esdl_key.name} not found in {self.esdl_asset}.")
                logger.warning(f"Default value of {esdl_key.default} used for {esdl_key.name}.")
                parameters[parameter_key] = esdl_key.default
        return parameters
