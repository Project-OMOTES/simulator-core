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
from typing import Any

import esdl

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.demand_cluster import DemandCluster
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.pipe import Pipe
from simulator_core.entities.assets.production_cluster import ProductionCluster


class EsdlAssetMapper:
    """Creates entity Asset objects based on a PyESDL EnergySystem assets."""

    conversion_dict = {
        esdl.Producer: ProductionCluster,
        esdl.GenericProducer: ProductionCluster,
        esdl.Consumer: DemandCluster,
        esdl.HeatingDemand: DemandCluster,
        esdl.Pipe: Pipe,
    }

    def to_esdl(self, entity: AssetAbstract) -> Any:
        """Maps entity object to PyEsdl objects."""
        raise NotImplementedError("EsdlAssetMapper.to_esdl()")

    def to_entity(self, model: EsdlAssetObject) -> AssetAbstract:
        """Method to map an esdl asset to an asset entity class.

        :param EsdlAssetObject model: Object to be converted to an asset entity.

        :return: Entity object.
        """
        if not type(model.esdl_asset) in self.conversion_dict:
            raise NotImplementedError(str(model.esdl_asset) + " not implemented in conversion")
        return self.conversion_dict[type(model.esdl_asset)](
            model.esdl_asset.name, model.esdl_asset.id)
