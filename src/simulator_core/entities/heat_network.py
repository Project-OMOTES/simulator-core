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

from simulator_core.entities.assets.asset_abstract import AssetAbstract


class HeatNetwork:
    """Class to store information on the heat network."""

    def __init__(self, asset_list: list[AssetAbstract], junction_list: list[AssetAbstract]):
        """Constructor of heat network class.

        :param list[AssetAbstract] asset_list: List with assets in the network
        :param list[AssetAbstract] junction_list: List with junction in the network.
        """
        self.assets = asset_list
        self.junctions = junction_list

    def run_time_step(self, time: float, controller_input: dict):
        """Method to simulate a time step.

        :param float time: Timestep for which to simulate the model
        :param dict controller_input: Dict specifying the heat demand for the different assets.
        :return: None
        """
        pass

    def store_output(self):
        """Method to store the output data.

        This method takes the data from the pandapipes dataframe and stores it into our own
        dataframe. This is needed since we have the possibility to redo a timestep when results are
        not converged for the input of the controller.
        :return: None
        """
        pass
