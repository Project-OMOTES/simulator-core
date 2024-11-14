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

from omotes_simulator_core.entities.assets.ates_cluster import AtesCluster
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract
from omotes_simulator_core.entities.assets.asset_defaults import ATES_DEFAULTS

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
        )


        aquifer_depth, _ = esdl_asset.get_property(
            esdl_property_name="aquiferTopDepth", default_value=ATES_DEFAULTS.aquifer_depth
        )
        self.aquifer_thickness, _ = esdl_asset.get_property(
            esdl_property_name="aquiferThickness", default_value=ATES_DEFAULTS.aquifer_thickness
        )
        self.aquifer_mid_temperature, _ = esdl_asset.get_property(
            esdl_property_name="aquiferMidTemperature", default_value=ATES_DEFAULTS.aquifer_mid_temperature
        )
        self.aquifer_net_to_gross, _ = esdl_asset.get_property(
            esdl_property_name="aquiferNetToGross", default_value=ATES_DEFAULTS.aquifer_net_to_gross
        )
        self.aquifer_porosity, _ = esdl_asset.get_property(
            esdl_property_name="aquiferPorosity", default_value=ATES_DEFAULTS.aquifer_porosity
        )
        self.aquifer_permeability, _ = esdl_asset.get_property(
            esdl_property_name="aquiferPermeability", default_value=ATES_DEFAULTS.aquifer_permeability
        )
        self.aquifer_anisotropy, _ = esdl_asset.get_property(
            esdl_property_name="aquiferAnisotropy", default_value=ATES_DEFAULTS.aquifer_anisotropy
        )
        self.salinity, _ = esdl_asset.get_property(
            esdl_property_name="salinity", default_value=ATES_DEFAULTS.salinity
        )
        self.well_casing_size, _ = esdl_asset.get_property(
            esdl_property_name="wellCasingSize", default_value=ATES_DEFAULTS.well_casing_size
        )
        self.well_distance, _ = esdl_asset.get_property(
            esdl_property_name="wellDistance", default_value=ATES_DEFAULTS.well_distance
        )

        maximum_charge_power, _ = esdl_asset.get_property(
            esdl_property_name="maxChargeRate", default_value=12e7
        )

        self.maximum_flow_charge = heat_demand_and_temperature_to_mass_flow(
            maximum_charge_power, self.temperature_supply, self.temperature_return
        )

        maximum_discharge_power, _ = esdl_asset.get_property(
            esdl_property_name="maxChargeRate", default_value=12e7
        )

        self.maximum_flow_discharge = heat_demand_and_temperature_to_mass_flow(
            maximum_discharge_power, ATES_DEFAULTS.temperature_supply, ATES_DEFAULTS.temperature_return
        )

        self._init_rosim()
        return ates_entity
    
    def _init_rosim(self) -> None:
    """Function to initailized Rosim from XML file."""
    xmlfile = os.path.join(path, "bin/sequentialTemplate_v0.4.2_template.xml")
    with open(xmlfile, "r") as fd:
        xml_str = fd.read()

    # overwrite template value with ESDL properties for ROSIM input

    MODEL_TOP = self.aquifer_depth - 100
    AQUIFER_THICKNESS = self.aquifer_thickness
    NZ_AQUIFER = math.floor(AQUIFER_THICKNESS / 2)
    NZ = NZ_AQUIFER + 8
    AQUIFER_TOP = self.aquifer_depth
    AQUIFER_BASE = self.aquifer_depth + self.aquifer_thickness
    SURFACE_TEMPERATURE = self.aquifer_mid_temperature - 0.034 * (
        self.aquifer_depth + self.aquifer_thickness / 2
    )
    AQUIFER_NTG = self.aquifer_net_to_gross
    AQUIFER_PORO = self.aquifer_porosity
    AQUIFER_PERM_XY = self.aquifer_permeability
    AQUIFER_PERM_Z = AQUIFER_PERM_XY / self.aquifer_anisotropy
    SALINITY = self.salinity
    WELL2_X = self.well_distance + 300
    CASING_SIZE = self.well_casing_size

    xml_str = xml_str.replace("$NZ$", str(NZ))
    xml_str = xml_str.replace("$MODEL_TOP$", str(MODEL_TOP))
    xml_str = xml_str.replace("$TIME_STEP_UNIT$", str(2))
    xml_str = xml_str.replace("$WELL2_X$", str(WELL2_X))
    xml_str = xml_str.replace("$AQUIFER_TOP$", str(AQUIFER_TOP))
    xml_str = xml_str.replace("$AQUIFER_BASE$", str(AQUIFER_BASE))
    xml_str = xml_str.replace("$CASING_SIZE$", str(CASING_SIZE))
    xml_str = xml_str.replace("$SURFACE_TEMPERATURE$", str(SURFACE_TEMPERATURE))
    xml_str = xml_str.replace("$SALINITY$", str(SALINITY))
    xml_str = xml_str.replace("$NZ_AQUIFER$", str(NZ_AQUIFER))
    xml_str = xml_str.replace("$AQUIFER_THICKNESS$", str(AQUIFER_THICKNESS))
    xml_str = xml_str.replace("$AQUIFER_PORO$", str(AQUIFER_PORO))
    xml_str = xml_str.replace("$AQUIFER_NTG$", str(AQUIFER_NTG))
    xml_str = xml_str.replace("$AQUIFER_PERM_XY$", str(AQUIFER_PERM_XY))
    xml_str = xml_str.replace("$AQUIFER_PERM_Z$", str(AQUIFER_PERM_Z))

    temp_xmlfile_path = os.path.join(path, "bin/ates_sequential_temp.xml")
    with open(temp_xmlfile_path, "w") as temp_xmlfile:
        temp_xmlfile.write(xml_str)

    xmlfilejava = javaioFile(temp_xmlfile_path)
    self.rosim = RosimSequential(xmlfilejava, False, 2)