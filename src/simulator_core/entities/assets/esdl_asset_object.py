"""Module containing classes to be able to interact with esdl objects."""
import logging
from esdl import esdl
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

