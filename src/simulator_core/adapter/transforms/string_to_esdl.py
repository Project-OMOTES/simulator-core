"""Module containing class to convert a string to asdl class type and vica-versa"""
import esdl


class StringEsdlAssetMapper:
    """Mapper class to convert strings to an esdl class type and vica-versa.

    Please note that the str_to_type_dict needs to have unique keys and values.
    """

    type_to_str_dict = {
        esdl.Asset: "asset",
        esdl.Producer: "producer",
        esdl.GenericProducer: "producer",
        esdl.Consumer: "consumer",
        esdl.HeatingDemand: "consumer",
        esdl.GeothermalSource: "geothermal",
        esdl.Conversion: "conversion",
        esdl.Pipe: "pipe",
        esdl.Transport: "transport",
        esdl.Joint: "junction",
    }

    str_to_type_dict = {
        "asset": esdl.Asset,
        "producer": esdl.Producer,
        "consumer": esdl.Consumer,
        "geothermal": esdl.GeothermalSource,
        "conversion": esdl.Conversion,
        "pipe": esdl.Pipe,
        "transport": esdl.Transport,
        "junction": esdl.Joint,
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
        if entity not in self.type_to_str_dict:
            raise NotImplementedError(
                str(entity) + " not implemented in StringESDLAssetMapper class"
            )
        return self.type_to_str_dict[entity]
