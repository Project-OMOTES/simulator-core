"""Module to map an esdl asset to a controller entity class."""

import numpy as np
from simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract, Entity
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject


class EsdlAssetControllerProducerMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a producer entity class."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerProducer:
        """Method to map an esdl asset to a producer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        result = esdl_asset.get_property(esdl_property_name="power", default_value=0)
        if result[1]:
            power = result[0]
        else:
            raise ValueError("No power found for asset: " + esdl_asset.esdl_asset.name)
        temperature_supply = esdl_asset.get_supply_temperature("Out")
        temperature_return = esdl_asset.get_return_temperature("In")
        contr_producer = ControllerProducer(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_supply=temperature_supply,
            temperature_return=temperature_return,
            power=power,
        )
        return contr_producer


class EsdlAssetControllerConsumerMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a consumer entity class."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerConsumer:
        """Method to map an esdl asset to a consumer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        result = esdl_asset.get_property(esdl_property_name="power", default_value=np.inf)
        power = np.inf
        if result[1]:
            power = result[0]
        if power == 0:
            power = np.inf

        temperature_supply = esdl_asset.get_supply_temperature("In")
        temperature_return = esdl_asset.get_return_temperature("Out")
        profile = esdl_asset.get_profile()
        contr_consumer = ControllerConsumer(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_supply=temperature_supply,
            temperature_return=temperature_return,
            max_power=power,
            profile=profile,
        )
        return contr_consumer


class EsdlAssetControllerStorageMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a storage entity class."""

    def to_esdl(self, entity: Entity) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerStorageMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerStorage:
        """Method to map an esdl asset to a storage entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        result = esdl_asset.get_property(esdl_property_name="power", default_value=np.inf)
        power = np.inf
        if result[1]:
            power = result[0]
        if power == 0:
            power = np.inf

        temperature_supply = esdl_asset.get_supply_temperature("In")
        temperature_return = esdl_asset.get_return_temperature("Out")
        profile = esdl_asset.get_profile()
        contr_storage = ControllerStorage(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_supply=temperature_supply,
            temperature_return=temperature_return,
            max_power=power,
            profile=profile,
        )
        return contr_storage
