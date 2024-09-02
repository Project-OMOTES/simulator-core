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
from typing import Any, Type
import esdl
from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.demand_cluster import DemandCluster
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.pipe import Pipe
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.entities.assets.ates_cluster import AtesCluster
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract, Entity


class EsdlAssetProductionMapper(EsdlMapperAbstract):
    """Class to map PyEsdl Producer to Producer entity."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Maps Producer asset to esdl asset."""
        raise NotImplementedError("EsdlAssetProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ProductionCluster:
        """Method to map an esdl asset to a producer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """

        producer = ProductionCluster(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
        )
        return producer


class EsdlAssetConsumerMapper(EsdlMapperAbstract):
    """Class to map PyEsdl Consumer to Consumer entity."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Maps Producer asset to esdl asset."""
        raise NotImplementedError("EsdlAssetProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ProductionCluster:
        """Method to map an esdl asset to a producer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """

        consumer = DemandCluster(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
        )
        return consumer


class EsdlAssetPipeMapper(EsdlMapperAbstract):
    """Class to map PyEsdl Pipe to Pipe entity."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Maps Pipe asset to esdl asset."""
        raise NotImplementedError("EsdlAssetPipeMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> Pipe:
        """Method to map an esdl asset to a pipe entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        pipe = Pipe(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
        )
        return pipe


class EsdlAssetAtesMapper(EsdlMapperAbstract):
    """Class to map PyEsdl ATES to ATES entity."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Maps ATES asset to esdl asset."""
        raise NotImplementedError("EsdlAssetAtesMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AtesCluster:
        """Method to map an esdl asset to a ATES entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        ates = AtesCluster(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
        )
        return ates


class EsdlAssetMapper:
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    conversion_dict: dict[esdl.EnergyAsset, Type[EsdlMapperAbstract]] = {
        esdl.Producer: EsdlAssetProductionMapper,
        esdl.GenericProducer: EsdlAssetProductionMapper,
        esdl.Consumer: EsdlAssetConsumerMapper,
        esdl.HeatingDemand: EsdlAssetConsumerMapper,
        esdl.Pipe: EsdlAssetPipeMapper,
        esdl.ATES: EsdlAssetAtesMapper,
    }

    def to_esdl(self, entity: AssetAbstract) -> Any:
        """Maps entity object to PyEsdl objects."""
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    def to_entity(self, model: EsdlAssetObject) -> AssetAbstract:
        """Method to map an esdl asset to an asset entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        if not type(model.esdl_asset) in self.conversion_dict:
            raise NotImplementedError(str(model.esdl_asset) + " not implemented in conversion")
        return self.conversion_dict[type(model.esdl_asset)]().to_entity(model)
