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

"""HeatNetwork entity class."""
import datetime
from typing import Callable

import pandas as pd

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver


class HeatNetwork:
    """Class to store information on the heat network."""

    def __init__(
        self, conversion_factory: Callable[[Network], tuple[list[AssetAbstract], list[Junction]]]
    ) -> None:
        """Constructor of heat network class.

        :param conversion_factory: method to convert the esdl network to lists of assets&junctions
        and returns list of both
        """
        self.network = Network()
        self.assets, self.junctions = conversion_factory(self.network)
        self.solver = Solver(self.network)

        # Mapping from asset id to asset object for easy access
        self._asset_id_to_asset: dict[str, AssetAbstract] = {
            asset.asset_id: asset for asset in self.assets
        }

    def run_time_step(
        self, time: datetime.datetime, time_step: float, controller_input: dict
    ) -> None:
        """Method to simulate a time step.

        It first sets the controller input to the assets and then simulates the time step.

        :param Datetime time: Time for which to simulate the model
        :param float time_step: The time step to simulate
        :param dict controller_input: Dict specifying the heat demand for the different assets.
        :return: None
        """
        for py_asset in self.assets:
            if py_asset.asset_id in controller_input:
                py_asset.set_time_step(time_step)
                py_asset.set_time(time)
                py_asset.set_setpoints(controller_input[py_asset.asset_id])

        self.solver.solve()

    def plot_network(self) -> None:
        """Method to plot the network.

        plots the network in a simple plot all junctions are translated to a circle.
        :return:
        """

    def store_output(self) -> None:
        """Method to store the output data.

        This method takes the data from the assets and stores it into our own
        dataframe. This is needed since we have the possibility to redo a timestep when results are
        not converged for the input of the controller.
        :return: None
        """
        for py_asset in self.assets:
            py_asset.write_standard_output()
            py_asset.write_to_output()

    def gather_output(self) -> pd.DataFrame:
        """Method to gather output of all assets and return it as a dict.

        :return: Dict with for all asset a dict with all outputs.
        """
        # Todo what do we do with the junction output do we need it?
        result = pd.DataFrame()
        for py_asset in self.assets:
            result = pd.concat([result, py_asset.get_timeseries()], axis=1)
        return result

    def check_convergence(self) -> bool:
        """Method to check if the network has converged.

        :return: True if the network has converged, False otherwise
        """
        for py_asset in self.assets:
            if not py_asset.is_converged():
                return False
        return True

    def get_asset_by_id(self, asset_id: str) -> AssetAbstract:
        """Method to get an asset by its ID.

        :param str asset_id: The ID of the asset to get.
        :return: The asset with the given ID.
        """
        return self._asset_id_to_asset[asset_id]
