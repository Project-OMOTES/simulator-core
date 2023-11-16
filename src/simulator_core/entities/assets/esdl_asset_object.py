"""Module containing classes to be able to interact with esdl objects."""
import logging
from esdl import esdl
from simulator_core.entities.assets import AssetAbstract, DemandCluster, ProductionCluster, Pipe

logger = logging.getLogger(__name__)


@dataclass
class EsdlKey:
    name: str
    default: any


ASSET_DICT = {
    "producer": {
        "heating demand": EsdlKey(name="power", default=0.0),
    },
}


class EsdlAssetObject:
    """
    Class to hold an esdl asset and convert it to local class objects.

    Conversion is done based on the classes in the conversion_dict.
    """

    esdl_asset: esdl.Asset

    def __init__(self, asset: esdl.Asset) -> None:
        """
        Constructor for EsdlAssetObject class.

        :param asset, esdl.Asset which os stored int hsi class for interaction.
        """
        self.esdl_asset = asset

    def get_property_dict_for_asset(self, asset_type: type) -> dict:
        """
        Get the properties of the ESDL asset required for the simulation.

        :param asset_type: type of the asset
        :return: dict of properties
        """
        # Retrieve NWN string from ESDL asset type
        asset_type_string = StringEsdlAssetMapper().to_entity(asset_type)
        # Retrieve the properties from the asset
        return ASSET_DICT[asset_type_string]

    def get_asset_parameters(self) -> dict:
        """
        Get the parameters of the asset.

        :return: dict of parameters
        """
        # Retrieve the asset specific parameter dictionary
        asset_specific_parameter = self.get_property_dict_for_asset(
            asset_type=type(self.esdl_asset)
        )
        # Retrieve the parameters from the asset
        parameters = {}
        for parameter_key, esdl_key in asset_specific_parameter.items():
            try:
                parameters[parameter_key] = getattr(self.esdl_asset, esdl_key.name)
            except AttributeError:
                logger.warning(f"Attribute {esdl_key.name} not found in {self.esdl_asset}.")
                logger.warning(f"Default value of {esdl_key.default} used for {esdl_key.name}.")
                parameters[parameter_key] = esdl_key.default
        return parameters
