from esdl import esdl


class EsdlObject:
    """
    EsdlObject class is a wrapper around PyEsdl
    """
    es: esdl.EnergySystem

    def __init__(self, esdl_energysystem: esdl.EnergySystem) -> None:
        """
        constructor for EsdlObject
        :param esdl_energysystem: PyEsdl EnergySystem object
        """
        self.es = esdl_energysystem

    def __repr__(self) -> str:
        return str(self.es)
