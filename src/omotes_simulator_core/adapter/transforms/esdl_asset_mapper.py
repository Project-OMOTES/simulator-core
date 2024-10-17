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
from typing import Any, Type

import esdl
import numpy as np

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.demand_cluster import DemandCluster
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.entities.assets.production_cluster import ProductionCluster
from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster
from omotes_simulator_core.entities.assets.heat_pump import HeatPump

from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.controller_consumer import ControllerConsumer
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract, Entity


from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS
from omotes_simulator_core.entities.assets.utils import (
    calculate_inverse_heat_transfer_coefficient,
    get_thermal_conductivity_table,
)


CONVERSION_DICT: dict[esdl.EnergyAsset, Type[AssetAbstract]] = {
    esdl.Producer: ProductionCluster,
    esdl.GenericProducer: ProductionCluster,
    esdl.Consumer: DemandCluster,
    esdl.GenericConsumer: DemandCluster,
    esdl.HeatingDemand: DemandCluster,
    esdl.Pipe: Pipe,
    esdl.ATES: AtesCluster,
    esdl.HeatPump: HeatPump,
}


class EsdlAssetMapper:
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    @staticmethod
    def to_esdl(entity: AssetAbstract) -> Any:
        """Maps entity object to PyEsdl objects."""
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    @staticmethod
    def to_entity(model: EsdlAssetObject) -> AssetAbstract:
        """Method to map an esdl asset to an asset entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object of type AssetAbstract.
        """
        if not type(model.esdl_asset) in CONVERSION_DICT:
            raise NotImplementedError(str(model.esdl_asset) + " not implemented in conversion")
        if isinstance(model.esdl_asset, esdl.Pipe):
            return EsdlAssetPipeMapper().to_entity(model)
        else:
            return CONVERSION_DICT[type(model.esdl_asset)](
                model.esdl_asset.name,
                model.esdl_asset.id,
                model.get_port_ids(),
            )


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
        result = esdl_asset.get_property(
            esdl_property_name="maxDischargeRate", default_value=np.inf
        )
        discharge_power = np.inf
        if result[1]:
            discharge_power = result[0]

        result = esdl_asset.get_property(esdl_property_name="maxChargeRate", default_value=np.inf)
        charge_power = np.inf
        if result[1]:
            charge_power = result[0]

        temperature_supply = esdl_asset.get_supply_temperature("In")
        temperature_return = esdl_asset.get_return_temperature("Out")
        profile = esdl_asset.get_profile()
        contr_storage = ControllerStorage(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_supply=temperature_supply,
            temperature_return=temperature_return,
            max_charge_power=charge_power,
            max_discharge_power=discharge_power,
            profile=profile,
        )
        return contr_storage


class EsdlAssetPipeMapper(EsdlMapperAbstract):
    """Class to map an ESDL asset to a pipe entity class."""

    def to_esdl(self, entity: Pipe) -> EsdlAssetObject:
        """Map a Pipe entity to an EsdlAsset."""
        raise NotImplementedError("EsdlAssetPipeMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
        """Method to map an ESDL asset to a pipe entity class.

        :param EsdlAssetObject esdl_asset: Object to be converted to a pipe entity.
        :return: Pipe object.
        """
        # Note: Need to add a check if the returned value is false or not. Some values can be zero.
        pipe_entity = Pipe(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
            length=esdl_asset.get_property("length", PIPE_DEFAULTS.length)[0],
            inner_diameter=esdl_asset.get_property("innerDiameter", PIPE_DEFAULTS.diameter)[0],
            roughness=esdl_asset.get_property("roughness", PIPE_DEFAULTS.roughness)[0],
            alpha_value=self._get_heat_transfer_coefficient(esdl_asset),
            minor_loss_coefficient=esdl_asset.get_property(
                "minor_loss_coefficient", PIPE_DEFAULTS.minor_loss_coefficient
            )[0],
            external_temperature=esdl_asset.get_property(
                "external_temperature", PIPE_DEFAULTS.external_temperature
            )[0],
            qheat_external=esdl_asset.get_property("qheat_external", PIPE_DEFAULTS.qheat_external)[
                0
            ],
        )

        return pipe_entity

    def _get_heat_transfer_coefficient(self, esdl_asset: EsdlAssetObject) -> float:
        """Calculate the heat transfer coefficient of the pipe.

        :param EsdlAssetObject esdl_asset: The ESDL asset object associated with the
                current pipe object.

        :return: The heat transfer coefficient of the pipe [W/(m2 K)]. If the heat transfer
                coefficient cannot be calculated - for example when the material table is
                not specified - , the default alpha value is returned.
        """
        diameters, heat_coefficients = get_thermal_conductivity_table(esdl_asset=esdl_asset)
        if diameters:
            diameters_np = np.array(diameters)
            heat_coefficients_np = np.array(heat_coefficients)
            inverse_heat_transfer_coefficient = np.sum(
                calculate_inverse_heat_transfer_coefficient(
                    inner_diameter=diameters_np[:-1],
                    outer_diameter=diameters_np[1:],
                    thermal_conductivity=heat_coefficients_np,
                )
            )
            return 1.0 / float(inverse_heat_transfer_coefficient)
        else:
            return PIPE_DEFAULTS.alpha_value
