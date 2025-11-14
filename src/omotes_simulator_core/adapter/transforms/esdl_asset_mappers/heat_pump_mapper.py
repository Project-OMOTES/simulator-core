#  Copyright (c) 2025. Deltares & TNO
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
"""Module containing the Esdl to HeatPump asset mapper class."""

from omotes_simulator_core.entities.assets.air_to_water_heat_pump import AirToWaterHeatPump
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import HeatPumpDefaults
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.heat_pump import HeatPump
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlAssetHeatPumpMapper(EsdlMapperAbstract):
    """Class to map an ESDL asset to a heatpump entity class."""

    def to_esdl(self, entity: HeatPump) -> EsdlAssetObject:
        """Map a HeatPump entity to an EsdlAsset."""
        raise NotImplementedError("EsdlAssetHeatPumpMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
        """Method to map an ESDL asset to a heatpump entity class.

        :param EsdlAssetObject esdl_asset: Object to be converted to a heatpump entity.
        :return: HeatPump object.
        """
        hp_ports = esdl_asset.get_number_of_ports()
        if hp_ports == 4:  # Water to water heat pump case
            heatpump_entity = HeatPump(
                asset_name=esdl_asset.esdl_asset.name,
                asset_id=esdl_asset.esdl_asset.id,
                connected_ports=esdl_asset.get_port_ids(),
                coefficient_of_performance=esdl_asset.get_property(
                    "COP", HeatPumpDefaults.coefficient_of_performance
                ),
            )
        elif hp_ports == 2:  # Air to water heat pump case.
            heatpump_entity = AirToWaterHeatPump(  # type:ignore
                asset_name=esdl_asset.esdl_asset.name,
                asset_id=esdl_asset.esdl_asset.id,
                port_ids=esdl_asset.get_port_ids(),
                coefficient_of_performance=esdl_asset.get_property(
                    "COP", HeatPumpDefaults.coefficient_of_performance
                ),
            )
        else:
            raise NotImplementedError(
                str(esdl_asset.esdl_asset) + " uncompatible number of ports for heat pump. "
                "Use 2 ports for air to water HP, or 4 for a water to water HP."
            )

        return heatpump_entity
