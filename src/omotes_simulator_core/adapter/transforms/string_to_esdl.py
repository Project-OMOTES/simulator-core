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
"""Module containing class to convert a string to asdl class type and vica-versa."""
from enum import Enum
from typing import Type

import esdl


class OmotesAssetLabels(str, Enum):
    """Enum class containing the omotes asset labels."""

    ASSET = "asset"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    GEOTHERMAL = "geothermal"
    CONVERSION = "conversion"
    PIPE = "pipe"
    TRANSPORT = "transport"
    JOINT = "joint"
    STORAGE = "storage"
    HEAT_PUMP = "heat_pump"
    HEAT_EXCHANGER = "heat_exchanger"


class StringEsdlAssetMapper:
    """Mapper class to convert strings to an esdl class type and vica-versa.

    Please note that the str_to_type_dict needs to have unique keys and values.
    Also note that fo the esdl class only the derived classes should be listed.
    Otherwise asset might be selected twice, since a HeatingDemand is also and Consumer.
    """

    def __init__(self) -> None:
        """Initialize the maps from string to esdl type and vica-versa."""
        # Label to type map, where the first entry of each type list is the most generic or
        # representative type.
        self.label_to_type_map: dict[OmotesAssetLabels, list[Type[esdl.Asset]]] = {
            OmotesAssetLabels.ASSET: [esdl.Asset],
            OmotesAssetLabels.PRODUCER: [
                esdl.GenericProducer,
                esdl.HeatProducer,
                # esdl.Producer, # Same as above, avoid selecting twice
            ],
            OmotesAssetLabels.CONSUMER: [
                esdl.GenericConsumer,
                esdl.HeatingDemand,
                # esdl.Consumer, # Same as above, avoid selecting twice
            ],
            OmotesAssetLabels.GEOTHERMAL: [esdl.GeothermalSource],
            OmotesAssetLabels.CONVERSION: [esdl.Conversion],
            OmotesAssetLabels.PIPE: [esdl.Pipe],
            OmotesAssetLabels.TRANSPORT: [esdl.Transport],
            OmotesAssetLabels.JOINT: [esdl.Joint],
            OmotesAssetLabels.STORAGE: [esdl.ATES],
            OmotesAssetLabels.HEAT_PUMP: [esdl.HeatPump],
            OmotesAssetLabels.HEAT_EXCHANGER: [esdl.HeatExchange],
        }

        self.type_to_label_map: dict[Type[esdl.Asset], OmotesAssetLabels] = {
            asset_type: label
            for label, asset_types in self.label_to_type_map.items()
            for asset_type in asset_types
        }

    def to_esdl(self, entity: OmotesAssetLabels) -> list[type]:
        """Method to convert an OmotesAssetLabels to one or more esdl class types.

        :param OmotesAssetLabels entity: Enum to be converted to an esdl class type object.
        :return: ESDL class described in the enum.
        """
        if entity not in self.label_to_type_map:
            raise NotImplementedError(entity + " not implemented in StringESDLAssetMapper class")
        return self.label_to_type_map[entity]

    def to_entity(self, entity: type) -> str:
        """Method to convert esdl type class to a string.

        The dict values are converted to a list to find the index in the list.
        Then the list of keys is created and the value at the index found is returned.
        :param type entity: ESDl object clas to be converted to a string
        :return: str belonging to the entity.
        """
        if entity not in self.type_to_label_map:
            raise NotImplementedError(
                str(entity) + " not implemented in StringESDLAssetMapper class"
            )
        return self.type_to_label_map[entity]
