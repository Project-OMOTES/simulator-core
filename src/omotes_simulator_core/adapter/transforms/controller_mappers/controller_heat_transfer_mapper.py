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
from omotes_simulator_core.entities.assets.asset_defaults import (
    HeatExchangerDefaults,
    HeatPumpDefaults,
)
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.controller_heat_transfer import (
    ControllerHeatTransferAsset,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class ControllerHeatPumpMapper(EsdlMapperAbstract):
    """Class to map an EsdlAsset to a ControllerHeatTransferAsset."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerHeatTransferAsset:
        """Method to map an EsdlAsset to a ControllerHeatTransferAsset.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        coefficient_of_performance = esdl_asset.get_property(
            esdl_property_name="COP", default_value=HeatPumpDefaults.coefficient_of_performance
        )
        contr_heat_transfer = ControllerHeatTransferAsset(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            factor=coefficient_of_performance,
        )
        return contr_heat_transfer


class ControllerHeatExchangeMapper(EsdlMapperAbstract):
    """Class to map an EsdlAsset to a ControllerHeatTransferAsset."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerHeatTransferAsset:
        """Method to map an EsdlAsset to a ControllerHeatTransferAsset.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        coefficient_of_performance = esdl_asset.get_property(
            esdl_property_name="Efficiency",
            default_value=HeatExchangerDefaults.heat_transfer_efficiency,
        )
        contr_heat_transfer = ControllerHeatTransferAsset(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            factor=coefficient_of_performance,
        )
        return contr_heat_transfer
