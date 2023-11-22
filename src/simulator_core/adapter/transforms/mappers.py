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

""" Mapper classes."""

from typing import Any

from simulator_core.adapter.transforms.esdl_asset_mapper import EsdlAssetMapper
from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.production_cluster import ProductionCluster
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.entities.heat_network import HeatNetwork
from simulator_core.entities.network_controller import NetworkController
from simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlEnergySystemMapper(EsdlMapperAbstract):
    """Creates a Heatnetwork entity object based on a PyESDL EnergySystem object."""

    def to_esdl(self, entity: HeatNetwork) -> EsdlObject:
        raise NotImplementedError("EsdlEnergySystemMapper.to_esdl()")

    def to_entity(self, model: EsdlObject) -> HeatNetwork:
        """
        Method to convert esdl to Heatnetwork object.

        This method first converts all assets into a list of assets.
        Next to this a list of Junctions is created. This is then used
        to create the Heatnetwork object.
        """
        # TODO
        # convert esdl network to heat network
        # create junctions
        # create assets
        # create connection between them

        assets_list = [
            EsdlAssetMapper().to_entity(asset) for asset in model.get_all_assets_of_type("asset")
        ]
        junction_list = model.get_all_assets_of_type("junction")
        return HeatNetwork(assets_list, junction_list)


class EsdlControllerMapper(EsdlMapperAbstract):
    """Creates a NetworkController entity object based on a PyESDL EnergySystem object."""

    def to_esdl(self, entity: NetworkController) -> EsdlObject:
        raise NotImplementedError("EsdlControllerMapper.to_esdl()")

    def to_entity(self, model: EsdlObject) -> NetworkController:
        # TODO
        pass


class ProductionAssetMapper(EsdlAssetMapper):
    def to_entity(self, model: EsdlAssetObject) -> ProductionCluster:
        pass
