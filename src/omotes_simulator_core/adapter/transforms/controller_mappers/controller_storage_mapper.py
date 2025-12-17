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
from typing import Optional

import numpy as np
import pandas as pd

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.controller_storage import ControllerStorage
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolator,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class ControllerStorageMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a storage entity class."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerStorageMapper.to_esdl()")

    def to_entity(
        self, esdl_asset: EsdlAssetObject, timestep: Optional[int] = None
    ) -> ControllerStorage:
        """Method to map an esdl asset to a storage entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.
        :param Optional[int] timestep: Simulation timestep in seconds.

        :return: Entity object.
        """
        discharge_power = esdl_asset.get_property(
            esdl_property_name="maxDischargeRate", default_value=np.inf
        )

        charge_power = esdl_asset.get_property(
            esdl_property_name="maxChargeRate", default_value=np.inf
        )
        temperature_in = esdl_asset.get_temperature("In", "Supply")
        temperature_out = esdl_asset.get_temperature("Out", "Return")
        profile = pd.DataFrame()  # esdl_asset.get_profile()
        self.profile_interpolator = ProfileInterpolator(
            profile=profile,
            sampling_method=esdl_asset.get_sampling_method(),
            interpolation_method=esdl_asset.get_interpolation_method(),
            timestep=timestep,
        )
        resampled_profile = self.profile_interpolator.get_resampled_profile()
        contr_storage = ControllerStorage(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            max_charge_power=charge_power,
            max_discharge_power=discharge_power,
            profile=resampled_profile,
        )
        return contr_storage
