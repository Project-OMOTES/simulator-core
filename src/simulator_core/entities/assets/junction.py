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

"""Junction classes."""

from typing import Any, List, Optional

from pandapipes import create_junction, pandapipesNet

from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
)


class Junction:
    """Wrapper class for pandapipes junctions."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        pn_bar: float = DEFAULT_PRESSURE,
        tfluid_k: float = DEFAULT_TEMPERATURE,
        height_m: float = DEFAULT_NODE_HEIGHT,
        geodata: Optional[List[Any]] = None,
        name: str = "None",
        in_service: bool = True,
        index: Optional[int] = None,
    ):
        """Initialize a Junction object.

        :param pn_bar: The pressure at the junction [bar], defaults to DEFAULT_PRESSURE
        :type pn_bar: float, optional
        :param tfluid_k: The temperature at the junction [K], defaults to DEFAULT_TEMPERATURE
        :type tfluid_k: float, optional
        :param height_m: The height of the junction [m], defaults to DEFAULT_NODE_HEIGHT
        :type height_m: float, optional

        """
        self.pandapipes_net = pandapipes_net
        self.pn_bar = pn_bar
        self.tfluid_k = tfluid_k
        self.height_m = height_m
        self.geodata = geodata
        self.name = name
        self.in_service = in_service
        self.index = index
        # Initialize the junction
        self._initialized = False
        self.create()

    def create(self) -> None:
        """Register the junction in the pandapipes network."""
        if not self._initialized:
            self._initialized = True
            self.index = create_junction(
                net=self.pandapipes_net,
                pn_bar=self.pn_bar,
                tfluid_k=self.tfluid_k,
                height_m=self.height_m,
                geodata=self.geodata,
                name=self.name,
                in_service=self.in_service,
            )

    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        pass
