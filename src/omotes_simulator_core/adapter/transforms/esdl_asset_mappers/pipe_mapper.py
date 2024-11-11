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
"""Module containing the Esdl to Pipe asset mapper class."""

import numpy as np
from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from omotes_simulator_core.entities.assets.pipe import Pipe
from omotes_simulator_core.simulation.mappers.mappers import EsdlMapperAbstract


from omotes_simulator_core.entities.assets.asset_defaults import PIPE_DEFAULTS
from omotes_simulator_core.entities.assets.utils import (
    calculate_inverse_heat_transfer_coefficient,
    get_thermal_conductivity_table,
)


class EsdlAssetPipeMapper(EsdlMapperAbstract):
    """Class to map an ESDL asset to a pipe entity class."""

    def to_esdl(self, entity: Pipe) -> EsdlAssetObject:
        """Map a Pipe entity to an EsdlAsset."""
        raise NotImplementedError("EsdlAssetPipeMapper.to_esdl()")

    def to_entity(self, esdl_asset: EsdlAssetObject) -> AssetAbstract:
        """Method to map an ESDL asset to a pipe entity class.

        :param EsdlAssetObject esdl_asset: Object to be converted to a pipe entity.
        :return: Pipe object.
        """
        pipe_entity = Pipe(
            asset_name=esdl_asset.esdl_asset.name,
            asset_id=esdl_asset.esdl_asset.id,
            port_ids=esdl_asset.get_port_ids(),
            length=esdl_asset.get_property("length", PIPE_DEFAULTS.length)[0],
            inner_diameter=self._get_diameter(esdl_asset=esdl_asset),
            roughness=esdl_asset.get_property("roughness", PIPE_DEFAULTS.roughness)[0],
            alpha_value=self._get_heat_transfer_coefficient(esdl_asset),
            minor_loss_coefficient=esdl_asset.get_property(
                "minor_loss_coefficient", PIPE_DEFAULTS.minor_loss_coefficient
            )[0],
            external_temperature=esdl_asset.get_property(
                "external_temperature", PIPE_DEFAULTS.external_temperature
            )[0],
            qheat_external=esdl_asset.get_property("qheat_external", PIPE_DEFAULTS.qheat_external)[
                0
            ],
        )

        return pipe_entity

    @staticmethod
    def _get_heat_transfer_coefficient(esdl_asset: EsdlAssetObject) -> float:
        """Calculate the heat transfer coefficient of the pipe.

        :param EsdlAssetObject esdl_asset: The ESDL asset object associated with the
                current pipe object.

        :return: The heat transfer coefficient of the pipe [W/(m2 K)]. If the heat transfer
                coefficient cannot be calculated - for example when the material table is
                not specified - , the default alpha value is returned.
        """
        diameters, heat_coefficients = get_thermal_conductivity_table(esdl_asset=esdl_asset)
        if diameters:
            diameters_np = np.array(diameters)
            heat_coefficients_np = np.array(heat_coefficients)
            inverse_heat_transfer_coefficient = np.sum(
                calculate_inverse_heat_transfer_coefficient(
                    inner_diameter=diameters_np[:-1],
                    outer_diameter=diameters_np[1:],
                    thermal_conductivity=heat_coefficients_np,
                )
            )
            return 1.0 / float(inverse_heat_transfer_coefficient)
        else:
            return PIPE_DEFAULTS.alpha_value

    @staticmethod
    def _get_diameter(esdl_asset: EsdlAssetObject) -> float:
        """Retrieve the diameter of the pipe and convert it if necessary."""
        temp_diameter, property_available = esdl_asset.get_property(
            "innerDiameter", PIPE_DEFAULTS.diameter
        )
        if property_available:
            if temp_diameter == 0:
                return PIPE_DEFAULTS.diameter
            return float(temp_diameter)
        else:
            # Implement DN-conversion
            raise NotImplementedError(
                f"The innerDiameter property is unavailable for {esdl_asset.esdl_asset.name}. "
                "Conversion from DN to diameter is not yet implemented."
            )
