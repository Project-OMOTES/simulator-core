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

"""Test Junction entities."""
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from omotes_simulator_core.adapter.transforms.esdl_asset_mappers.pipe_mapper import (
    EsdlAssetPipeMapper,
)
from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.solver.network.assets.solver_pipe import SolverPipe
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS


class TestEsdlAssetPipeMapper(unittest.TestCase):

    def setUp(self):
        """Define the variables used in the tests."""
        self.name: str = "pipe"
        self.asset_id: str = "pipe_id"
        self.ports: list[str] = ["test1", "test2"]
        self.length: float = 1
        self.inner_diameter: float = 1
        self.roughness: float = 0.001
        self.alpha_value: float = 0.8
        self.minor_loss_coefficient: float = 0.0
        self.external_temperature: float = 273.15 + 20.0
        self.qheat_external: float = 0.0

        """Arranging standard objects for the other test."""
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / ".." / ".." / "testdata" / "test1.esdl"
        )
        esdl_file_path = str(esdl_file_path)
        self.esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        self.mapper = EsdlAssetPipeMapper()

    def test_get_all_assets_of_type(self):
        pipes = self.esdl_object.get_all_assets_of_type("pipe")  # act
        self.assertGreater(len(pipes), 0, "No pipes found in the ESDL file.")
        self.pipe = pipes[0]

    def test_to_entity(self):
        self.test_get_all_assets_of_type()
        esdl_asset = self.pipe
        pipe_entity = self.mapper.to_entity(esdl_asset)
        self.assertEqual(pipe_entity.name, esdl_asset.esdl_asset.name)
        self.assertEqual(pipe_entity.asset_id, esdl_asset.esdl_asset.id)
        self.assertEqual(pipe_entity.connected_ports, esdl_asset.get_port_ids())  # type: ignore
        self.assertEqual(pipe_entity.length, esdl_asset.get_property("length", PIPE_DEFAULTS.length)[0])  # type: ignore
        self.assertEqual(pipe_entity.diameter, self.mapper._get_diameter(esdl_asset))  # type: ignore
        self.assertEqual(pipe_entity.roughness, esdl_asset.get_property("roughness", PIPE_DEFAULTS.roughness)[0])  # type: ignore
        self.assertEqual(pipe_entity.alpha_value, self.mapper._get_heat_transfer_coefficient(esdl_asset))  # type: ignore
        self.assertEqual(pipe_entity.minor_loss_coefficient, esdl_asset.get_property("minor_loss_coefficient", PIPE_DEFAULTS.minor_loss_coefficient)[0])  # type: ignore
        self.assertEqual(pipe_entity.external_temperature, esdl_asset.get_property("external_temperature", PIPE_DEFAULTS.external_temperature)[0])  # type: ignore
        self.assertEqual(
            pipe_entity.qheat_external,  # type: ignore
            esdl_asset.get_property("qheat_external", PIPE_DEFAULTS.qheat_external)[0],
        )
