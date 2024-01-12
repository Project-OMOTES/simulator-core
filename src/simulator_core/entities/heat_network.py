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

import pandas as pd
from pandapipes import create_empty_network, pandapipesNet, pipeflow, PipeflowNotConverged
from typing import Callable, List, Tuple
from simulator_core.entities.assets.asset_abstract import AssetAbstract, Junction


class HeatNetwork:
    """Class to store information on the heat network."""

    def __init__(self, conversion_factory: Callable[[pandapipesNet], Tuple[List[AssetAbstract],
                                                                           List[Junction]]]):
        """Constructor of heat network class.

        :param conversion_factory: method to convert the esdl network to pandapipes
        assets and junctions and returns list of both
        """
        self.panda_pipes_net = create_empty_network(fluid="water")
        self.assets, self.junctions = conversion_factory(self.panda_pipes_net)

    def run_time_step(self, time: float, controller_input: dict) -> None:
        """Method to simulate a time step.

        It first sets the controller input to the assets and then simulates the time step.

        :param float time: Timestep for which to simulate the model
        :param dict controller_input: Dict specifying the heat demand for the different assets.
        :return: None
        """
        for py_asset in self.assets:
            if py_asset.asset_id in controller_input:
                py_asset.set_setpoints(controller_input[py_asset.asset_id])
        try:
            pipeflow(self.panda_pipes_net, "all")
        except PipeflowNotConverged:
            raise RuntimeError("Error in time step calculation pipe flow did not converge.")

    def store_output(self) -> None:
        """Method to store the output data.

        This method takes the data from the pandapipes dataframe and stores it into our own
        dataframe. This is needed since we have the possibility to redo a timestep when results are
        not converged for the input of the controller.
        :return: None
        """
        for py_asset in self.assets:
            py_asset.write_to_output()
        for py_junction in self.junctions:
            py_junction.write_to_output()

    def gather_output(self) -> pd.DataFrame:
        """Method to gather output of all assets and return it as a dict.

        :return: Dict with for all asset a dict with all outputs.
        """
        # Todo what do we do with the junction output do we need it?
        result = pd.DataFrame()
        for py_asset in self.assets:
            result = pd.concat([result, py_asset.get_timeseries()])
        return result
