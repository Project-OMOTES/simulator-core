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

import logging
from typing import Optional

import pandas as pd

from omotes_simulator_core.entities.assets.controller.asset_controller_abstract import (
    AssetControllerAbstract,
)
from omotes_simulator_core.entities.assets.controller.controller_producer import ControllerProducer
from omotes_simulator_core.entities.assets.controller.profile_interpolation import (
    ProfileInterpolator,
)
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract

logger = logging.getLogger(__name__)


class ControllerProducerMapper(EsdlMapperAbstract):
    """Class to map an esdl asset to a producer entity class."""

    def to_esdl(self, entity: AssetControllerAbstract) -> EsdlAssetObject:
        """Map an Entity to a EsdlAsset."""
        raise NotImplementedError("EsdlAssetControllerProducerMapper.to_esdl()")

    def to_entity(
        self, esdl_asset: EsdlAssetObject, timestep: Optional[int] = None
    ) -> ControllerProducer:
        """Method to map an esdl asset to a producer entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        power = esdl_asset.get_property(esdl_property_name="power", default_value=0)
        marginal_costs = esdl_asset.get_marginal_costs()
        temperature_in = esdl_asset.get_temperature("In", "Return")
        temperature_out = esdl_asset.get_temperature("Out", "Supply")
        strategy_priority = esdl_asset.get_strategy_priority()

        if esdl_asset.has_constraint():
            profile = esdl_asset.get_constraint_max_profile()
            self.profile_interpolator = ProfileInterpolator(
                profile=profile,
                sampling_method=esdl_asset.get_sampling_method(),
                interpolation_method=esdl_asset.get_interpolation_method(),
                timestep=timestep,
            )
            resampled_profile = self.profile_interpolator.get_resampled_profile()
        else:
            resampled_profile = pd.DataFrame()

        contr_producer = ControllerProducer(
            name=esdl_asset.esdl_asset.name,
            identifier=esdl_asset.esdl_asset.id,
            temperature_in=temperature_in,
            temperature_out=temperature_out,
            power=power,
            marginal_costs=marginal_costs,
            profile=resampled_profile,  # Empty DataFrame is added if there is no profile.
            priority=strategy_priority,
        )
        return contr_producer
