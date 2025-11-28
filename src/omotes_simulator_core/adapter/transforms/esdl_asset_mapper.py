#  Copyright (c) 2023. Deltares & TNO
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Module containing the Esdl to asset mapper class."""
import esdl

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.ates_mapper import (
    EsdlAssetAtesMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.consumer_mapper import (
    EsdlAssetConsumerMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.heat_pump_mapper import (
    EsdlAssetHeatPumpMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper import (
    EsdlAssetPipeMapper,
)
from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.producer_mapper import (
    EsdlAssetProducerMapper,
)
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract

# Define the conversion dictionary
conversion_dict_mappers: dict[type, type[EsdlMapperAbstract]] = {
    esdl.Producer: EsdlAssetProducerMapper,
    esdl.HeatProducer: EsdlAssetProducerMapper,
    esdl.GenericProducer: EsdlAssetProducerMapper,
    esdl.GeothermalSource: EsdlAssetProducerMapper,
    esdl.ResidualHeatSource: EsdlAssetProducerMapper,
    esdl.SolarCollector: EsdlAssetProducerMapper,
    esdl.GasHeater: EsdlAssetProducerMapper,
    esdl.Consumer: EsdlAssetConsumerMapper,
    esdl.GenericConsumer: EsdlAssetConsumerMapper,
    esdl.HeatingDemand: EsdlAssetConsumerMapper,
    esdl.Pipe: EsdlAssetPipeMapper,
    esdl.HeatPump: EsdlAssetHeatPumpMapper,
    esdl.HeatExchange: EsdlAssetHeatPumpMapper,
    esdl.ATES: EsdlAssetAtesMapper,
}


class EsdlAssetMapper:
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    @staticmethod
    def to_esdl(entity: AssetAbstract) -> EsdlAssetObject:
        """Maps entity object to PyEsdl objects."""
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    @staticmethod
    def to_entity(model: EsdlAssetObject) -> AssetAbstract:
        """Method to map an esdl asset to an asset entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object of type AssetAbstract.
        """
        if type(model.esdl_asset) not in conversion_dict_mappers:
            raise NotImplementedError(str(model.esdl_asset) + " not implemented in conversion")

        # Use the dictionary to get the appropriate mapper
        asset_type = type(model.esdl_asset)
        mapper = conversion_dict_mappers[asset_type]()
        return mapper.to_entity(model)  # type: ignore
