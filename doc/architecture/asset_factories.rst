.. _asset_factory:

Asset factories
====================================
This encloses multiple classes, which are used to map esdl asset object to objects used by the simulator.
All classes are derived from the EsdlMapperAbstract class, which is a base class for all asset factories.
The following classes are available:

#. Producer
#. Consumer
#. Ates
#. HeatPump
#. Pipe

Each of these classes have a to_entity method, which maps the esdl asset object to the simulator object.

.. autoclass:: omotes_simulator_core.simulation.mappers.mappers.EsdlMapperAbstract
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.adapter.transforms.esdl_asset_mappers.producer_mapper.EsdlAssetProducerMapper
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.adapter.transforms.esdl_asset_mappers.consumer_mapper.EsdlAssetConsumerMapper
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.adapter.transforms.esdl_asset_mappers.ates_mapper.EsdlAssetAtesMapper
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.adapter.transforms.esdl_asset_mappers.heat_pump_mapper.EsdlAssetHeatPumpMapper
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper.EsdlAssetPipeMapper
    :members:
    :no-index: