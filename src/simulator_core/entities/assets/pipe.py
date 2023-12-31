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
from pandapipes import create_pipe_from_parameters, pandapipesNet

from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    PIPE_DEFAULTS,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
    PROPERTY_VELOCITY_RETURN,
    PROPERTY_VELOCITY_SUPPLY,
)
from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.entities.assets.utils import (
    calculate_inverse_heat_transfer_coefficient,
    get_thermal_conductivity_table,
    mass_flow_and_temperature_to_heat_demand,
)


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
    _initialized: bool
    """Flag to indicate whether the pipe has been initialized in pandapipes."""
    output: List[Dict[str, float]]
    """The output list of the pipe with a dictionaries for each timestep."""

    def __init__(self, asset_name: str, asset_id: str, pandapipe_net: pandapipesNet):
        """Initialize a Pipe object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, pandapipe_net=pandapipe_net)
        # Initialize the default values of the pipe
        self._minor_loss_coefficient = PIPE_DEFAULTS.minor_loss_coefficient
        self._external_temperature = PIPE_DEFAULTS.external_temperature
        self._qheat_external = PIPE_DEFAULTS.qheat_external
        # Define properties of the pipe
        self.length = PIPE_DEFAULTS.length
        self.diameter = PIPE_DEFAULTS.diameter
        self.roughness = PIPE_DEFAULTS.k_value
        self.alpha_value = PIPE_DEFAULTS.alpha_value
        # Objects of the pandapipes network
        self._initialized = False
        self._pipe_index = None
        self.output = []

    def create(self) -> None:
        """Create a representation of the pipe in the pandapipes network."""
        if not self._initialized:
            # Create the pipe in the pandapipes network
            self._pipe_index = create_pipe_from_parameters(
                net=self.pandapipes_net,
                from_junction=self.from_junction.index,
                to_junction=self.to_junction.index,
                length_km=self.length * 1e-3,
                diameter_m=self.diameter,
                k_mm=self.roughness * 1e3,
                alpha_w_per_m2k=self.alpha_value,
                qext_w=self._qheat_external,
                name=f"Pipe_{self.name}",
                in_service=True,
            )
            # Set the initialized flag to True
            self._initialized = True

    def _get_diameter(self, esdl_asset: EsdlAssetObject) -> float:
        """Retrieve the diameter of the pipe and convert it if necessary."""
        temp_diameter, property_available = esdl_asset.get_property("innerDiameter", self.diameter)
        if property_available:
            return temp_diameter
        else:
            # Implement DN-conversion
            raise NotImplementedError(
                f"The innderDiamter property is unavailable for {esdl_asset.name}. \
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
            diameters = np.array(diameters)
            heat_coefficients = np.array(heat_coefficients)
            # Calculate the heat transfer coefficient from the heat transfer table
            inverse_heat_transfer_coefficient = np.sum(
                calculate_inverse_heat_transfer_coefficient(
                    inner_diameter=diameters[:-1],
                    outer_diameter=diameters[1:],
                    thermal_conductivity=heat_coefficients,
                )
            )
            return 1 / inverse_heat_transfer_coefficient
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
            esdl_property_name="roughness", default_value=self.length
        )
        self.diameter = self._get_diameter(esdl_asset=esdl_asset)
        self.alpha_value = self._get_heat_transfer_coefficient(esdl_asset=esdl_asset)

    def simulation_performed(self) -> bool:
        """Check whether a simulation has been performed.

        :return bool: True if a simulation has been performed, False otherwise.
        """
        if self.pandapipes_net.res_pipe[self._pipe_index] is AttributeError:
            # TODO: Implement specific error
            return False
        else:
            # Retrieve the setpoints
            return True

    def write_to_output(self) -> None:
        """Write the output of the asset to the output list.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.

        The output of the asset is a dictionary with the following keys:
        - PROPERTY_HEAT_DEMAND: The heat demand of the asset.
        - PROPERTY_TEMPERATURE_SUPPLY: The supply temperature of the asset.
        - PROPERTY_TEMPERATURE_RETURN: The return temperature of the asset.
        - PROPERTY_PRESSURE_SUPPLY: The supply pressure of the asset.
        - PROPERTY_PRESSURE_RETURN: The return pressure of the asset.
        - PROPERTY_MASSFLOW: The mass flow rate of the asset.
        - PROPERTY_VELOCITY_SUPPLY: The supply velocity of the asset.
        - PROPERTY_VELOCITY_RETURN: The return velocity of the asset.
        """
        output_dict = {}
        # Retrieve the temperature of the pipe at the in- and outlet (Ts, Tr)
        output_dict[PROPERTY_TEMPERATURE_SUPPLY] = self.pandapipes_net.res_pipe[
            "temp_from_k"
        ].values[self._pipe_index]
        output_dict[PROPERTY_TEMPERATURE_RETURN] = self.pandapipes_net.res_pipe["temp_to_k"].values[
            self._pipe_index
        ]
        # Retrieve the pressure of the pipe at the in- and outlet (Ps, Pr)
        output_dict[PROPERTY_PRESSURE_SUPPLY] = self.pandapipes_net.res_pipe["p_from_bar"].values[
            self._pipe_index
        ]
        output_dict[PROPERTY_PRESSURE_RETURN] = self.pandapipes_net.res_pipe["p_to_bar"].values[
            self._pipe_index
        ]
        # Retrieve the mass flow rate of the pipe (mdot)
        output_dict[PROPERTY_MASSFLOW] = self.pandapipes_net.res_pipe["mdot_from_kg_per_s"].values[
            self._pipe_index
        ]
        # Retrieve the velocity of the pipe at the in- and outlet (Vs, Vr)
        output_dict[PROPERTY_VELOCITY_SUPPLY] = self.pandapipes_net.res_pipe[
            "v_from_m_per_s"
        ].values[self._pipe_index]
        output_dict[PROPERTY_VELOCITY_RETURN] = self.pandapipes_net.res_pipe["v_to_m_per_s"].values[
            self._pipe_index
        ]
        # Calculate the heat demand of the pipe (Q)
        output_dict[PROPERTY_HEAT_DEMAND] = mass_flow_and_temperature_to_heat_demand(
            temperature_supply=output_dict[PROPERTY_TEMPERATURE_SUPPLY],
            temperature_return=output_dict[PROPERTY_TEMPERATURE_RETURN],
            mass_flow=output_dict[PROPERTY_MASSFLOW],
            pandapipes_net=self.pandapipes_net,
        )
        self.output.append(output_dict)
