import esdl
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class StringEsdlAssetMapper(EsdlMapperAbstract):
    """Mapper class to convert strings to an esdl class type and vica-versa."""

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

    def to_esdl(self, entity: str) -> type:
        """Method to convert a string to esdl class type.

        :param str entity: String to be converted to an esdl class type object.
        :return: ESDL class described in the string.
        """
        if entity not in self.str_to_type_dict:
            raise NotImplementedError(entity + " not implemented in StringESDLAssetMapper class")
        return self.str_to_type_dict[entity]

    def to_entity(self, entity: type) -> str:
        """Method to convert esdl type class to a string.

        The dict values are converted to a list to find the index in the list.
        Then the list of keys is created and the value at the index found is returned.
        :param type entity: ESDl object clas to be converted to a string
        :return: str belonging to the entity.
        """
        try:
            index = list(self.str_to_type_dict.values()).index(entity)
        except ValueError:
            raise NotImplementedError(str(entity) + " not implemented in StringESDLAssetMapper "
                                                    "class")
        return list(self.str_to_type_dict.keys())[index]