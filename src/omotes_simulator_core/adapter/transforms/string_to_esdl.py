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
import esdl

from omotes_simulator_core.adapter.transforms.transform_utils import reverse_dict
from typing import List


class StringEsdlAssetMapper:
    """Mapper class to convert strings to an esdl class type and vica-versa.

    Please note that the str_to_type_dict needs to have unique keys and values.
    Also note that fo the esdl class only the derived classes should be listed.
    Otherwise asset might be selected twice, since a HeatingDemand is also and Consumer.
    """

    type_to_str_dict = {
        esdl.Asset: "asset",
        esdl.GenericProducer: "producer",
        esdl.GenericConsumer: "consumer",
        esdl.HeatingDemand: "consumer",
        esdl.GeothermalSource: "geothermal",
        esdl.Conversion: "conversion",
        esdl.Pipe: "pipe",
        esdl.Transport: "transport",
        esdl.Joint: "junction",
        esdl.ATES: "storage",
    }

    str_to_type_dict = reverse_dict(original_dict=type_to_str_dict)

    def to_esdl(self, entity: str) -> List[type]:
        """Method to convert a string to esdl class type.

        :param str entity: String to be converted to an esdl class type object.
        :return: ESDL class described in the string.
        """
        if entity not in self.str_to_type_dict:
            raise NotImplementedError(entity + " not implemented in StringESDLAssetMapper class")
        return self.str_to_type_dict[entity]

    def to_entity(self, entity: type) -> str:
        """Method to convert esdl type class to a string.

        The dict values are converted to a list to find the index in the list.
        Then the list of keys is created and the value at the index found is returned.
        :param type entity: ESDl object clas to be converted to a string
        :return: str belonging to the entity.
        """
        if entity not in self.type_to_str_dict:
            raise NotImplementedError(
                str(entity) + " not implemented in StringESDLAssetMapper class"
            )
        return self.type_to_str_dict[entity]
