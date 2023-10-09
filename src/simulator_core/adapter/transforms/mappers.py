from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
from simulator_core.entities.assets import AssetAbstract
from simulator_core.entities import HeatNetwork, NetworkController
from typing import Any
from esdl.esdl import Asset as PyEsdlAsset
from esdl.esdl import EnergySystem as PyEsdlEnergySystem


class EsdlEnergySystemMapper(EsdlMapperAbstract):
    """
    Creates a Heatnetwork entity object based on a PyESDL EnergySystem object
    """
    def to_esdl(self, entity: HeatNetwork) -> PyEsdlEnergySystem:
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")

    def to_entity(self, model: PyEsdlEnergySystem) -> HeatNetwork:
        # TODO
        pass


class EsdlControllerMapper(EsdlMapperAbstract):
    """
    Creates a NetworkController entity object based on a PyESDL EnergySystem object
    """
    def to_esdl(self, entity: NetworkController) -> PyEsdlEnergySystem:
        raise NotImplementedError("EsdlControllerMapper.to_esdl()")

    def to_entity(self, model: PyEsdlEnergySystem) -> NetworkController:
        # TODO
        pass


class EsdlAssetMapper(EsdlMapperAbstract):
    """
    Creates entity Asset objects based on a PyESDL EnergySystem assets
    """
    def to_esdl(self, entity: AssetAbstract) -> Any:
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    def to_entity(self, model: PyEsdlAsset) -> AssetAbstract:
        # TODO
        pass
