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

"""Module containing the Esdl to asset mapper class."""
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class ControllerProducerMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a producer entity class."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerProducer:
        """Method to map an esdl asset to a producer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        power = esdl_asset.get_property(esdl_property_name="power", default_value=0)
        marginal_costs = esdl_asset.get_marginal_costs()
        temperature_in = esdl_asset.get_temperature("In", "Return")
        temperature_out = esdl_asset.get_temperature("Out", "Supply")
        strategy_priority = esdl_asset.get_strategy_priority()
        contr_producer = ControllerProducer(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            power=power,
            marginal_costs=marginal_costs,
            priority=strategy_priority,
        )
        return contr_producer
