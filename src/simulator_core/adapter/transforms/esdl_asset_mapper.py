"""Module containing the Esdl to asset mapper class."""
from simulator_core.entities import EsdlAssetObject
from simulator_core.entities.assets import ProductionCluster, DemandCluster, Pipe, AssetAbstract
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
import esdl

from typing import Any


class EsdlAssetMapper(EsdlMapperAbstract):
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    conversion_dict = {
        esdl.Producer: ProductionCluster,
        esdl.GenericProducer: ProductionCluster,
        esdl.Consumer: DemandCluster,
        esdl.HeatingDemand: DemandCluster,
        esdl.Pipe: Pipe
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
            raise NotImplementedError(str(model.esdl_asset) + ' not implemented in conversion')
        return self.conversion_dict[type(model.esdl_asset)](model.esdl_asset.name,
                                                            model.esdl_asset.id)
