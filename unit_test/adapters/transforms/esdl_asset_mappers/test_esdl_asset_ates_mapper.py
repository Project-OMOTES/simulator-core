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

"""Test ates mapper."""

import unittest
from pathlib import Path

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.ates_mapper import (
    EsdlAssetAtesMapper,
)
from omotes_simulator_core.entities.assets.asset_defaults import (
    ATES_DEFAULTS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
)
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file


class TestEsdlAssetAtesMapper(unittest.TestCase):
    """Test class for ates mapper."""

    def setUp(self) -> None:
        """Set up test case."""
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test_ates.esdl"
        )
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetAtesMapper()

    def test_to_entity_method(self):
        """Test for to_entity method."""
        # Arrange
        atess_all = self.esdl_object.get_all_assets_of_type("storage")
        esdl_asset = atess_all[0]

        # Act
        ates_entity = self.mapper.to_entity(esdl_asset)

        # Assert
        self.assertEqual(ates_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(ates_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(ates_entity.connected_ports, esdl_asset.get_port_ids())
        self.assertEqual(
            ates_entity.aquifer_depth,
            esdl_asset.get_property("aquiferTopDepth", ATES_DEFAULTS.aquifer_depth),
        )
        self.assertEqual(
            ates_entity.aquifer_thickness,
            esdl_asset.get_property("aquiferThickness", ATES_DEFAULTS.aquifer_thickness),
        )
        self.assertEqual(
            ates_entity.aquifer_mid_temperature,
            esdl_asset.get_property("aquiferMidTemperature", ATES_DEFAULTS.aquifer_mid_temperature),
        )
        self.assertEqual(
            ates_entity.aquifer_net_to_gross,
            esdl_asset.get_property("aquiferNetToGross", ATES_DEFAULTS.aquifer_net_to_gross),
        )
        self.assertEqual(
            ates_entity.aquifer_porosity,
            esdl_asset.get_property("aquiferPorosity", ATES_DEFAULTS.aquifer_porosity),
        )
        self.assertEqual(
            ates_entity.aquifer_permeability,
            esdl_asset.get_property("aquiferPermeability", ATES_DEFAULTS.aquifer_permeability),
        )
        self.assertEqual(
            ates_entity.aquifer_anisotropy,
            esdl_asset.get_property("aquiferAnisotropy", ATES_DEFAULTS.aquifer_anisotropy),
        )
        self.assertEqual(
            ates_entity.salinity, esdl_asset.get_property("salinity", ATES_DEFAULTS.salinity)
        )
        self.assertEqual(
            ates_entity.well_casing_size,
            esdl_asset.get_property("wellCasingSize", ATES_DEFAULTS.well_casing_size),
        )
        self.assertEqual(
            ates_entity.well_distance,
            esdl_asset.get_property("wellDistance", ATES_DEFAULTS.well_distance),
        )

        self.assertEqual(
            ates_entity.maximum_flow_charge,
            (
                heat_demand_and_temperature_to_mass_flow(
                    esdl_asset.get_property(esdl_property_name="maxChargeRate", default_value=12e7),
                    DEFAULT_TEMPERATURE,
                    DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE,
                )
            ),
        )
        self.assertEqual(
            ates_entity.maximum_flow_discharge,
            (
                heat_demand_and_temperature_to_mass_flow(
                    esdl_asset.get_property(
                        esdl_property_name="maxDischargeRate", default_value=12e7
                    ),
                    DEFAULT_TEMPERATURE,
                    DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE,
                )
            ),
        )
