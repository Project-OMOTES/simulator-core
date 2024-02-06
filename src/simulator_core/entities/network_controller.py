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

"""NetworkController entity."""
from simulator_core.entities.assets.asset_defaults import (PROPERTY_TEMPERATURE_SUPPLY,
                                                           PROPERTY_TEMPERATURE_RETURN,
                                                           PROPERTY_HEAT_DEMAND)


class NetworkController:
    """Class to store the network controller."""

    def __init__(self) -> None:
        """Constructor for controller for a heat network."""
        pass

    def run_time_step(self, time: float) -> dict:
        """Method to get the controller inputs for the network.

        :param float time: Time step for which to run the controller.
        :return: dict with the key the asset id and the heat demand for that asset.
        """
        # TODO add also the possibility to return mass flow rate instead of heat demand.
        controller_input = {
            "cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4":
                {PROPERTY_TEMPERATURE_SUPPLY: 80 + 273.15,
                 PROPERTY_TEMPERATURE_RETURN: 40 + 273.15,
                 PROPERTY_HEAT_DEMAND: 5000000},
            "48f3e425-2143-4dcd-9101-c7e22559e82b": {PROPERTY_HEAT_DEMAND: 5000000,
                                                     PROPERTY_TEMPERATURE_RETURN: 40 + 273.15,
                                                     PROPERTY_TEMPERATURE_SUPPLY: 80 + 273.15}
        }
        return controller_input
