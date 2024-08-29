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
from typing import Callable, List, Tuple

import pandas as pd

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.junction import Junction
from omotes_simulator_core.solver.network.network import Network
from omotes_simulator_core.solver.solver import Solver


class HeatNetwork:
    """Class to store information on the heat network."""

    def __init__(
        self, conversion_factory: Callable[[Network], Tuple[List[AssetAbstract], List[Junction]]]
    ) -> None:
        """Constructor of heat network class.

        :param conversion_factory: method to convert the esdl network to lists of assets&junctions
        and returns list of both
        """
        self.network = Network()
        self.assets, self.junctions = conversion_factory(self.network)
        self.solver = Solver(self.network)

    def run_time_step(self, time: datetime.datetime, controller_input: dict) -> None:
        """Method to simulate a time step.

        It first sets the controller input to the assets and then simulates the time step.

        :param float time: Timestep for which to simulate the model
        :param dict controller_input: Dict specifying the heat demand for the different assets.
        :return: None
        """
        for py_asset in self.assets:
            if py_asset.asset_id in controller_input:
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
