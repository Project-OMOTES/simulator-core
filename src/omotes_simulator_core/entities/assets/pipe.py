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
"""Module containing pipe class."""
from typing import Dict, List

import numpy as np

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.utils import (
    calculate_inverse_heat_transfer_coefficient,
    get_thermal_conductivity_table,
)
from omotes_simulator_core.solver.network.assets.solver_pipe import SolverPipe


class Pipe(AssetAbstract):
    """A class representing a pipe in a heat network."""

    _minor_loss_coefficient: float
    """The minor loss coefficient of the pipe [-]."""
    _external_temperature: float
    """The external temperature surrounding the pipe [K]."""
    _qheat_external: float
    """The external heat flow into the pipe [W]."""
    length: float
    """The length of the pipe [m]."""
    diameter: float
    """The diameter of the pipe [m]."""
    roughness: float
    """The wall roughness of the pipe [m]."""
    alpha_value: float
    """The alpha value of the pipe [W/(m2 K)]."""
    output: List[Dict[str, float]]
    """The output list of the pipe with a dictionaries for each timestep."""

    def __init__(self, asset_name: str, asset_id: str, port_ids: list[str]):
        """Initialize a Pipe object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param List[str] port_ids: List of ids of the connected ports.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, connected_ports=port_ids)
        # Initialize the default values of the pipe
        self._minor_loss_coefficient = PIPE_DEFAULTS.minor_loss_coefficient
        self._external_temperature = PIPE_DEFAULTS.external_temperature
        self._qheat_external = PIPE_DEFAULTS.qheat_external
        # Define properties of the pipe
        self.length = PIPE_DEFAULTS.length
        self.diameter = PIPE_DEFAULTS.diameter
        self.roughness = PIPE_DEFAULTS.k_value
        self.alpha_value = PIPE_DEFAULTS.alpha_value
        self.solver_asset = SolverPipe(
            name=self.name,
            _id=self.asset_id,
            length=self.length,
            diameter=self.diameter,
            roughness=self.roughness,
        )
        self.output = []

    def _get_diameter(self, esdl_asset: EsdlAssetObject) -> float:
        """Retrieve the diameter of the pipe and convert it if necessary."""
        temp_diameter, property_available = esdl_asset.get_property("innerDiameter", self.diameter)
        if property_available:
            if temp_diameter == 0:
                return self.diameter
            return float(temp_diameter)
        else:
            # Implement DN-conversion
            raise NotImplementedError(
                f"The innderDiamter property is unavailable for {esdl_asset.esdl_asset.name}. \
                    Conversion from DN to diameter is not yet implemented."
            )

    def _get_heat_transfer_coefficient(self, esdl_asset: EsdlAssetObject) -> float:
        """Calculate the heat transfer coefficient of the pipe.

        :param EsdlAssetObject esdl_asset: The ESDL asset object associated with the
                current pipe object.

        :return: The heat transfer coefficient of the pipe [W/(m2 K)]. If the heat transfer
                coefficient cannot be calculated - for example when the material table is
                not specified - , the default alpha value is returned.
        """
        diameters, heat_coefficients = get_thermal_conductivity_table(esdl_asset=esdl_asset)
        if diameters:
            # Create a numpy array of the diameters and heat coefficients
            diameters_np = np.array(diameters)
            heat_coefficients_np = np.array(heat_coefficients)
            # Calculate the heat transfer coefficient from the heat transfer table
            inverse_heat_transfer_coefficient = np.sum(
                calculate_inverse_heat_transfer_coefficient(
                    inner_diameter=diameters_np[:-1],
                    outer_diameter=diameters_np[1:],
                    thermal_conductivity=heat_coefficients_np,
                )
            )
            return 1.0 / float(inverse_heat_transfer_coefficient)
        else:
            return self.alpha_value

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The ESDL asset object associated with the
                current pipe object.
        """
        # Error handling is performed in EsdlAssetObject.get_asset_parameters
        self.length, _ = esdl_asset.get_property(
            esdl_property_name="length", default_value=self.length
        )
        self.roughness, _ = esdl_asset.get_property(
            esdl_property_name="roughness", default_value=self.roughness
        )
        self.roughness = PIPE_DEFAULTS.k_value if self.roughness == 0 else self.roughness
        self.diameter = self._get_diameter(esdl_asset=esdl_asset)

        self.alpha_value = self._get_heat_transfer_coefficient(esdl_asset=esdl_asset)
        prop_dict = {"length": self.length, "diameter": self.diameter, "roughness": self.roughness}
        self.solver_asset.set_physical_properties(physical_properties=prop_dict)

    def set_setpoints(self, setpoints: Dict) -> None:
        """Set the setpoints of the pipe prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the pipe.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """

    def write_to_output(self) -> None:
        """Write the output of the asset to the output list.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        pass
