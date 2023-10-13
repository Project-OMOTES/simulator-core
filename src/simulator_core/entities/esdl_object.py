"""Module containing classes to be able to interact with esdl objects."""
import logging
from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler
from simulator_core.entities.assets import AssetAbstract, DemandCluster, ProductionCluster, Pipe

logger = logging.getLogger(__name__)


class EsdlAssetObject:
    """
    Class to hold an esdl asset and convert it to local class objects.

    Conversion is done based on the classes in the conversion_dict.
    """

    esdl_asset: esdl.Asset
    conversion_dict = {
        esdl.Producer: ProductionCluster,
        esdl.GenericProducer: ProductionCluster,
        esdl.Consumer: DemandCluster,
        esdl.HeatingDemand: DemandCluster,
        esdl.Pipe: Pipe
    }

    def __init__(self, asset: esdl.Asset) -> None:
        """
        Constructor for EsdlAssetObject class.

        :param asset, esdl.Asset which os stored int hsi class for interaction.
        """
        self.esdl_asset = asset

    def convert_esdl(self) -> AssetAbstract:
        """Converts the esdl asset into the own class object."""
        if not type(self.esdl_asset) in self.conversion_dict:
            raise NotImplementedError(self.esdl_asset.__repr__() + ' not implemented in conversion')
        return self.conversion_dict[type(self.esdl_asset)]()


class EsdlObject:
    """EsdlObject class is a wrapper around PyEsdl."""

    esh: EnergySystemHandler

    def __init__(self, esdl_energysystem_handler: EnergySystemHandler) -> None:
        """
        Constructor for EsdlObject.

        :param esdl_energysystem: PyEsdl EnergySystem object
        """
        self.esh = esdl_energysystem_handler

    def __repr__(self) -> str:
        """Returns a string describing the esdl file object."""
        return str(self.esh)

    def get_all_assets_of_type(self, esdl_asset_type: str) -> list[EsdlAssetObject]:
        """
        Returns a list of all the esdl assets of the specified type in the esdl file.

        If the type is not found an empty list is returned.
        :param esdl_asset_type: str of the asset type assets need to be gathered.
        """
        str_to_type_dict = {
            'asset': esdl.Asset,
            'producer': esdl.Producer,
            'consumer': esdl.Consumer,
            'geothermal': esdl.GeothermalSource,
            'conversion': esdl.Conversion,
            'pipe': esdl.Pipe,
            'transport': esdl.Transport,
            'junction': esdl.Joint
        }
        if esdl_asset_type not in str_to_type_dict:
            logger.error(esdl_asset_type + " not implemented in get_all_asset_of_type method")
            return []
        return [EsdlAssetObject(asset)
                for asset in self.esh.get_all_instances_of_type(str_to_type_dict[esdl_asset_type])]
