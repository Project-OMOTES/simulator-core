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
from unittest.mock import Mock

from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file
from omotes_simulator_core.solver.network.assets.solver_pipe import SolverPipe


class PipeTest(unittest.TestCase):
    """Testcase for HeatNetwork class."""

    def setUp(self):
        """Define the variables used in the tests."""
        self.length: float = 1
        self.inner_diameter: float = 1
        self.roughness: float = 0.001
        self.alpha_value: float = 0.8
        self.minor_loss_coefficient: float = 0.0
        self.external_temperature: float = 273.15 + 20.0
        self.qheat_external: float = 0.0

    def test_pipe_create(self):
        """Evaluate the creation of a pipe object."""
        # Arrange

        # Act
        pipe = Pipe(
            asset_name="pipe",
            asset_id="pipe_id",
            port_ids=["test1", "test2"],
            length=self.length,
            inner_diameter=self.inner_diameter,
            roughness=self.roughness,
            alpha_value=self.alpha_value,
            minor_loss_coefficient=self.minor_loss_coefficient,
            external_temperature=self.external_temperature,
            qheat_external=self.qheat_external,
        )

        # Assert
        self.assertIsInstance(pipe, Pipe)
        self.assertEqual(pipe.name, "pipe")
        self.assertEqual(pipe.asset_id, "pipe_id")
        self.assertEqual(pipe.length, self.length)
        self.assertEqual(pipe.diameter, self.inner_diameter)
        self.assertEqual(pipe.roughness, self.roughness)
        self.assertEqual(pipe.alpha_value, self.alpha_value)
        self.assertEqual(pipe.minor_loss_coefficient, self.minor_loss_coefficient)
        self.assertEqual(pipe.external_temperature, self.external_temperature)
        self.assertEqual(pipe.qheat_external, self.qheat_external)

    def test_pipe_unit_conversion(self):
        """Evaluate the unit conversion of the pipe object."""
        # Arrange
        pipe = Pipe(
            asset_name="pipe",
            asset_id="pipe_id",
            port_ids=["test1", "test2"],
            length=self.length,
            inner_diameter=self.inner_diameter,
            roughness=self.roughness,
            alpha_value=self.alpha_value,
            minor_loss_coefficient=self.minor_loss_coefficient,
            external_temperature=self.external_temperature,
            qheat_external=self.qheat_external,
        )

        # Act
        solver_pipe = SolverPipe(
            name="pipe", _id="pipe_id", length=pipe.length, roughness=pipe.roughness
        )

        # Assert
        self.assertEqual(solver_pipe.length, pipe.length)
        self.assertEqual(solver_pipe.roughness, pipe.roughness)

    def test_pipe_get_property_diameter(self):
        """Evaluate the get property diameter method to retrieve diameters."""
        # Arrange
        pipe = Pipe(
            asset_name="pipe",
            asset_id="pipe_id",
            port_ids=["test1", "test2"],
            length=self.length,
            inner_diameter=self.inner_diameter,
            roughness=self.roughness,
            alpha_value=self.alpha_value,
            minor_loss_coefficient=self.minor_loss_coefficient,
            external_temperature=self.external_temperature,
            qheat_external=self.qheat_external,
        )
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, True)

        # Act

        # Assert
        self.assertEqual(pipe._get_diameter(esdl_asset=esdl_asset_mock), 1.0)

    def test_pipe_get_property_diameter_failed(self):
        """Evaluate failure to retrieve diameter from ESDL asset."""
        # Arrange
        pipe = Pipe(
            asset_name="pipe",
            asset_id="pipe_id",
            port_ids=["test1", "test2"],
            length=self.length,
            inner_diameter=self.inner_diameter,
            roughness=self.roughness,
            alpha_value=self.alpha_value,
            minor_loss_coefficient=self.minor_loss_coefficient,
            external_temperature=self.external_temperature,
            qheat_external=self.qheat_external,
        )
        esdl_asset_mock = Mock()
        esdl_asset_mock.get_property.return_value = (1.0, False)

        # Act
        pass

        # Assert
        with self.assertRaises(NotImplementedError):
            pipe._get_diameter(esdl_asset=esdl_asset_mock)

    def test_pipe_get_heat_transfer_coefficient(self):
        """Evaluate the get heat transfer coefficient method."""
        # Arrange
        # - Load esdl pipe asset
        esdl_file_path = (
            Path(__file__).parent / ".." / ".." / "testdata" / "test_pipe_material.esdl"
        )
        esdl_file_path = str(esdl_file_path)
        esdl_object = EsdlObject(pyesdl_from_file(esdl_file_path))
        esdl_pipes = esdl_object.get_all_assets_of_type("pipe")
        esdl_pipe = [pipe for pipe in esdl_pipes if pipe.esdl_asset.name == "pipe_with_material"][0]
        # - Create pipe object
        # Act
        alpha_value = self.alpha_value
        pipe = Pipe(
            asset_name="pipe",
            asset_id="pipe_id",
            port_ids=["test1", "test2"],
            length=self.length,
            inner_diameter=self.inner_diameter,
            roughness=self.roughness,
            alpha_value=self.alpha_value,
            minor_loss_coefficient=self.minor_loss_coefficient,
            external_temperature=self.external_temperature,
            qheat_external=self.qheat_external,
        )

        alpha_value = pipe._get_heat_transfer_coefficient(esdl_asset=esdl_pipe)  # act

        # Assert
        self.assertEqual(alpha_value, 0.8901927763663371)
