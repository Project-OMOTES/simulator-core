"""Module with classes to convert esdl objects."""
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
from simulator_core.entities.assets import AssetAbstract, ProductionCluster
from simulator_core.entities import HeatNetwork, NetworkController, EsdlObject, EsdlAssetObject
from typing import Any


class EsdlEnergySystemMapper(EsdlMapperAbstract):
    """Creates a Heatnetwork entity object based on a PyESDL EnergySystem object."""

    def to_esdl(self, entity: HeatNetwork) -> EsdlObject:
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")

    def to_entity(self, model: EsdlObject) -> HeatNetwork:
        """
        Method to convert esdl to Heatnetwork object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the Heatnetwork object.
        """
        # TODO
        # convert esdl network to heat network
        # create junctions
        # create assets
        # create connection between them
        assets_list = [EsdlAssetMapper().to_entity(x)
                       for x in model.get_all_assets_of_type('asset')]
        junction_list = model.get_all_assets_of_type('junction')
        return HeatNetwork(assets_list, junction_list)


class EsdlControllerMapper(EsdlMapperAbstract):
    """Creates a NetworkController entity object based on a PyESDL EnergySystem object."""

    def to_esdl(self, entity: NetworkController) -> EsdlObject:
        raise NotImplementedError("EsdlControllerMapper.to_esdl()")

    def to_entity(self, model: EsdlObject) -> NetworkController:
        # TODO
        pass


class EsdlAssetMapper(EsdlMapperAbstract):
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    def to_esdl(self, entity: AssetAbstract) -> Any:
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    def to_entity(self, model: EsdlAssetObject) -> AssetAbstract:
        """Method to map an esdl asse to local class."""
        return model.convert_esdl()


class ProductionAssetMapper(EsdlAssetMapper):

    def to_entity(self, model: EsdlAssetObject) -> ProductionCluster:
        pass
