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

"""Test Zero flow of a simple network."""
import unittest
from uuid import uuid4

from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.network.assets.solver_pipe import SolverPipe
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver


class NetworkZeroFlowTest(unittest.TestCase):
    """Testcase for zero flow of a simple network."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create ProductionAsset object
        self.production_asset = HeatBoundary(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create DemandAsset object
        self.demand_asset = HeatBoundary(
            name=str(uuid4()),
            _id=str(uuid4()),
        )
        # Create a SolverPipe object supply
        self.supply_pipe = SolverPipe(
            name=str(uuid4()),
            _id=str(uuid4()),
            length=1.0,
            diameter=0.1,
            roughness=0.1,
        )
        # Create a SolverPipe object return
        self.return_pipe = SolverPipe(
            name=str(uuid4()),
            _id=str(uuid4()),
            length=1.0,
            diameter=0.1,
            roughness=0.1,
        )
        # Create a Network object
        self.network = Network()
        # Add assets to the network
        self.network.add_existing_asset(self.production_asset)
        self.network.add_existing_asset(self.demand_asset)
        self.network.add_existing_asset(self.supply_pipe)
        self.network.add_existing_asset(self.return_pipe)

        # Connect assets
        self.network.connect_assets(
            asset1_id=self.production_asset.name,
            connection_point_1=0,
            asset2_id=self.return_pipe.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.production_asset.name,
            connection_point_1=1,
            asset2_id=self.supply_pipe.name,
            connection_point_2=0,
        )
        self.network.connect_assets(
            asset1_id=self.demand_asset.name,
            connection_point_1=0,
            asset2_id=self.supply_pipe.name,
            connection_point_2=1,
        )
        self.network.connect_assets(
            asset1_id=self.demand_asset.name,
            connection_point_1=1,
            asset2_id=self.return_pipe.name,
            connection_point_2=0,
        )

    def test_zeroflow(self) -> None:
        """Test zero flow."""
        # Arrange
        # - Create a solver object
        self.solver = Solver(network=self.network)
        # - Set the temperature of the demand
        self.demand_asset.supply_temperature = 40 + 273.15
        self.demand_asset.mass_flow_rate_set_point = 0.0  # +1e-6
        self.demand_asset.pre_scribe_mass_flow = True
        # - Set the temperature of the production
        self.production_asset.supply_temperature = 60 + 273.15
        self.production_asset.pre_scribe_mass_flow = False
        # Act
        self.solver.solve()
        # Assert
        for asset in self.network.assets:
            for connection_point in [0, 1]:
                self.assertEqual(
                    abs(
                        self.network.get_asset(asset).prev_sol[
                            self.network.get_asset(asset).get_index_matrix(
                                property_name="mass_flow_rate",
                                connection_point=connection_point,
                                use_relative_indexing=True,
                            )
                        ]
                    ),
                    0.0,
                )
