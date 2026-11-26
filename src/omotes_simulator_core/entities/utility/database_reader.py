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

"""Module to read the esdl profiles from an energy system."""

import logging

import esdl
import pandas as pd
from esdl.profiles.profile_utils import load_profile_data_and_header
from esdl.units.conversion import ENERGY_IN_J, POWER_IN_W, convert_to_unit

logger = logging.getLogger(__name__)


def get_data_from_profile(esdl_profile: esdl.DataTableProfile | esdl.InfluxDBProfile
                          | esdl.TimeSeriesProfile | esdl.DateTimeProfile
                          | esdl.ProfileReference) -> pd.DataFrame:
    """Method to get the data from the esdl  profile.

    This method tries to get the data from the esdl profile.
    :param esdl_profile: esdl.Profile with the profile
    :return: pandas.DataFrame with the data
    """
    profile_data, _ = load_profile_data_and_header(esdl_profile, apply_multiplier=True)
    unit = get_unit(esdl_profile)
    return pd.DataFrame(
        (
            (
                time_stamp,
                convert_to_unit(value, esdl_profile.profileQuantityAndUnit, unit)
            )
            for time_stamp, value in profile_data  # type-ignore
        ),
        columns=["date", "values"],
    )


def get_unit(profile: esdl.DataTableProfile | esdl.InfluxDBProfile | esdl.TimeSeriesProfile
             | esdl.DateTimeProfile | esdl.ProfileReference) -> esdl.PhysicalQuantityEnum:
    """Method to get the SI unit of the profile.

    This method tries to get the unit of the profile.
    if the unit is not in the list the same unit as the profile is returned
    :param profile: esdl.InfluxDBProfile with the profile
    :return: esdl.PhysicalQuantityEnum with the unit
    """
    conversion_dict = {
        esdl.PhysicalQuantityEnum.POWER: POWER_IN_W,
        esdl.PhysicalQuantityEnum.ENERGY: ENERGY_IN_J,
    }
    try:
        profile_unit = profile.profileQuantityAndUnit.reference.physicalQuantity
    except AttributeError:
        profile_unit = profile.profileQuantityAndUnit.physicalQuantity
    if profile_unit in conversion_dict:
        return conversion_dict[profile_unit]
    return profile_unit
