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

"""Module containing the Esdl to Producer asset mapper class."""

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlAssetProducerMapper(EsdlMapperAbstract):
    """Class to map an ESDL asset to a producer entity class."""

    def to_esdl(self, entity: ProductionCluster) -> EsdlAssetObject:
        """Map a Producer entity to an EsdlAsset."""
        raise NotImplementedError("EsdlAssetProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
        """Method to map an ESDL asset to a producer entity class.

        :param EsdlAssetObject esdl_asset: Object to be converted to a producer entity.
        :return: Producer object.
        """
        producer_entity = ProductionCluster(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
        )

        return producer_entity
