"""Module containing the Esdl to asset mapper class."""
from typing import Any

import esdl

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.demand_cluster import DemandCluster
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.pipe import Pipe
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlAssetMapper(EsdlMapperAbstract):
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    conversion_dict = {
        esdl.Producer: ProductionCluster,
        esdl.GenericProducer: ProductionCluster,
        esdl.Consumer: DemandCluster,
        esdl.HeatingDemand: DemandCluster,
        esdl.Pipe: Pipe,
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
        return self.conversion_dict[type(model.esdl_asset)](
            model.esdl_asset.name, model.esdl_asset.id
        )
