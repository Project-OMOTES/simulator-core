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
import numpy as np
import pandas as pd

from omotes_simulator_core.entities.assets.asset_defaults import HeatBufferDefaults
from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import (
    ControllerAtestStorage,
    ControllerIdealHeatStorage,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class ControllerAtesStorageMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a Ates Storage entity class."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetAtesStorageMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerAtestStorage:
        """Method to map an esdl asset to a Ates Storage entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        profile = pd.DataFrame()  # esdl_asset.get_profile()

        return ControllerAtestStorage(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_in=esdl_asset.get_temperature("In", "Supply"),
            temperature_out=esdl_asset.get_temperature("Out", "Return"),
            max_charge_power=esdl_asset.get_property("maxChargeRate", np.inf),
            max_discharge_power=esdl_asset.get_property("maxDischargeRate", np.inf),
            profile=profile,
        )


class ControllerIdealHeatStorageMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a Ideal Heat Storage entity class."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetIdealHeatStorageMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> ControllerIdealHeatStorage:
        """Method to map an esdl asset to a Ideal Heat Storage entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        profile = pd.DataFrame()  # esdl_asset.get_profile()

        return ControllerIdealHeatStorage(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_in=esdl_asset.get_temperature("In", "Supply"),
            temperature_out=esdl_asset.get_temperature("Out", "Return"),
            max_charge_power=esdl_asset.get_property("maxChargeRate", np.inf),
            max_discharge_power=esdl_asset.get_property("maxDischargeRate", np.inf),
            profile=profile,
            fill_level=esdl_asset.get_property("fillLevel", HeatBufferDefaults.fill_level),
            volume=esdl_asset.get_property("volume", HeatBufferDefaults.volume),
        )
