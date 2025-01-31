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

from typing import Any, Optional

from omotes_simulator_core.entities.assets.asset_defaults import (
    DEFAULT_NODE_HEIGHT,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
)
from omotes_simulator_core.solver.network.assets.node import Node


class Junction:
    """Juntion connects two or more assets."""

    def __init__(
        self,
        solver_node: Node,
        pn_bar: float = DEFAULT_PRESSURE,
        tfluid_k: float = DEFAULT_TEMPERATURE,
        height_m: float = DEFAULT_NODE_HEIGHT,
        geodata: Optional[list[Any]] = None,
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
        self.pn_bar = pn_bar
        self.tfluid_k = tfluid_k
        self.height_m = height_m
        self.name = name
        self.index = index
        # Initialize the junction
        self.solver_junction = solver_node

    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        return
