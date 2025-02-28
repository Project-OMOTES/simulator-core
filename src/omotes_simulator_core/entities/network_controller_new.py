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
"""Module for new controller which can also cope with Heat pumps and heat exchangers."""

import datetime
from omotes_simulator_core.entities.assets.controller.controller_network import ControllerNetwork
from omotes_simulator_core.entities.network_controller_abstract import NetworkControllerAbstract


class NetworkControllerNew(NetworkControllerAbstract):
    """class for the enw network controller."""

    def __init__(
        self,
        networks: list[ControllerNetwork],
    ) -> None:
        self.networks = networks

    def update_setpoints(self, time: datetime.datetime) -> dict:
        """Method to get the controller inputs for the network.

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        pass
