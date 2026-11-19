#  Copyright (c) 2026. Deltares & TNO
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
"""Module containing utilities to retrieve asset data from the ESDL Energy Data Repository."""

from esdl.edr.client import EDRClient

from omotes_simulator_core.entities.assets.asset_defaults import (
    PIPE_DEFAULTS,
    PROPERTY_INNER_DIAMETER,
    PipeSchedules,
)


def get_diameter_from_edr(
    dn_diameter: str, schedule: PipeSchedules = PIPE_DEFAULTS.default_schedule
) -> float:
    """
    Retrieves the inner diameter of a pipe from the EDR list based on the nominal diameter.

    :param dn_diameter: the nominal diameter of the pipe.
    :param schedule: the insulation schedule (PipeSchedules enum: S1, S2, or S3).
    :return: Inner diameter [m] of the EDR pipe matching the DN diameter and schedule.

    """
    try:
        diameter = int(dn_diameter.replace("DN", ""))
        title = f"/edr/Public/Assets/Logstor/Steel-{schedule.name}-DN-{diameter}.edd"
        edr_client = EDRClient()
        esdl_object = edr_client.get_object_esdl(title)
        return float(getattr(esdl_object, PROPERTY_INNER_DIAMETER, PIPE_DEFAULTS.diameter))
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve ESDL object for DN diameter '{dn_diameter}': {e}")
