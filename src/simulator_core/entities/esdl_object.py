import logging
from esdl import esdl
from esdl.esdl_handler import EnergySystemHandler

logger = logging.getLogger(__name__)


class EsdlObject:
    """    EsdlObject class is a wrapper around PyEsdl    """

    esh: EnergySystemHandler

    def __init__(self, esdl_energysystem_handler: EnergySystemHandler) -> None:
        """
        constructor for EsdlObject
        :param esdl_energysystem: PyEsdl EnergySystem object
        """
        self.esh = esdl_energysystem_handler

    def __repr__(self) -> str:
        return str(self.esh)

    def get_all_assets_of_type(self, esdl_asset_type: str) -> list[esdl.Asset]:
        """
        returns a list of all the esdl assets of the specified type in the esdl file
        if the type is not found an empty list is returned
        :param esdl_asset_type: str of the asset type assets need to be gathered.
        """
        str_to_type_dict = {
            'assets': esdl.Asset,
            'producer': esdl.Producer,
            'consumer': esdl.Consumer,
            'geothermal': esdl.GeothermalSource,
            'conversion': esdl.Conversion,
            'pipe': esdl.Pipe,
            'transport': esdl.Transport
        }
        if esdl_asset_type not in str_to_type_dict:
            logger.error(esdl_asset_type + " not implemented in get_all_asset_of_type method")
            return []

        return self.esh.get_all_instances_of_type(str_to_type_dict[esdl_asset_type])
