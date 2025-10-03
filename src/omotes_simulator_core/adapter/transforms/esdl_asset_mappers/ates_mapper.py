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
"""Module containing the Esdl to Ates asset mapper class."""

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import ATES_DEFAULTS
from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


class EsdlAssetAtesMapper(EsdlMapperAbstract):
    """Class to map an ESDL asset to a ates entity class."""

    def to_esdl(self, entity: AtesCluster) -> EsdlAssetObject:
        """Map a Ates entity to an EsdlAsset."""
        raise NotImplementedError("EsdlAssetAtesMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
        """Method to map an ESDL asset to a ates entity class.

        :param EsdlAssetObject esdl_asset: Object to be converted to a ates entity.
        :return: Ates object.
        """
        ates_entity = AtesCluster(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
            aquifer_depth=esdl_asset.get_property(
                esdl_property_name="aquiferTopDepth", default_value=ATES_DEFAULTS.aquifer_depth
            ),
            aquifer_thickness=esdl_asset.get_property(
                esdl_property_name="aquiferThickness", default_value=ATES_DEFAULTS.aquifer_thickness
            ),
            aquifer_mid_temperature=esdl_asset.get_property(
                esdl_property_name="aquiferMidTemperature",
                default_value=ATES_DEFAULTS.aquifer_mid_temperature,
            ),
            aquifer_net_to_gross=esdl_asset.get_property(
                esdl_property_name="aquiferNetToGross",
                default_value=ATES_DEFAULTS.aquifer_net_to_gross,
            ),
            aquifer_porosity=esdl_asset.get_property(
                esdl_property_name="aquiferPorosity", default_value=ATES_DEFAULTS.aquifer_porosity
            ),
            aquifer_permeability=esdl_asset.get_property(
                esdl_property_name="aquiferPermeability",
                default_value=ATES_DEFAULTS.aquifer_permeability,
            ),
            aquifer_anisotropy=esdl_asset.get_property(
                esdl_property_name="aquiferAnisotropy",
                default_value=ATES_DEFAULTS.aquifer_anisotropy,
            ),
            salinity=esdl_asset.get_property(
                esdl_property_name="salinity", default_value=ATES_DEFAULTS.salinity
            ),
            well_casing_size=esdl_asset.get_property(
                esdl_property_name="wellCasingSize", default_value=ATES_DEFAULTS.well_casing_size
            ),
            well_distance=esdl_asset.get_property(
                esdl_property_name="wellDistance", default_value=ATES_DEFAULTS.well_distance
            ),
        )

        return ates_entity
