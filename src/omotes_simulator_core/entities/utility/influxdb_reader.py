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
from datetime import datetime
from typing import cast

import esdl
import pandas as pd
from esdl.esdl_handler import EnergySystemHandler
from esdl.profiles.influxdbprofilemanager import ConnectionSettings, InfluxDBProfileManager
from esdl.units.conversion import ENERGY_IN_J, POWER_IN_W, convert_to_unit

logger = logging.getLogger(__name__)


def _normalize_influx_filters(filters: str | None) -> list[dict[str, str]]:
    """Parse and normalize filters to the format expected by load_influxdb.

    The upstream parser may return dictionaries with a `key` field while
    load_influxdb expects `tag`. This shim keeps compatibility across versions.
    """
    parsed_filters = InfluxDBProfileManager._parse_esdl_profile_filters(filters)
    normalized_filters: list[dict[str, str]] = []
    for influx_filter in parsed_filters:
        tag = influx_filter.get("tag") or influx_filter.get("key")
        value = influx_filter.get("value")
        if not tag or value is None:
            continue
        normalized_filters.append(
            {
                "tag": str(tag),
                "value": str(value).strip().strip("\"").strip("'"),
            }
        )
    return normalized_filters


def parse_esdl_profiles(esh: EnergySystemHandler) -> dict[str, pd.DataFrame]:
    """Method to parse the esdl profiles from an energy system.

    This method tries to parse the esdl profiles from an energy system.
    :param esh: EnergySystemHandler with the energy system
    :param start_date: datetime.datetime with the start date
    :param end_date: datetime.datetime with the end date
    :return: dict with the parsed profiles
    """
    data_set = {}
    for profile in esh.get_all_instances_of_type(esdl.InfluxDBProfile):
        data_set[profile.id] = get_data_from_profile(profile)
    return data_set


def get_data_from_profile(esdl_profile: esdl.InfluxDBProfile) -> pd.DataFrame:
    """Method to get the data from the esdl influxdb profile.

    This method tries to get the data from the esdl profile.
    :param esdl_profile: esdl.Profile with the profile
    :return: pandas.DataFrame with the data
    """
    influx_cred_map: dict[str, tuple[str, str]] = {}
    profile_host = str(esdl_profile.host)
    profile_port = int(esdl_profile.port)
    profile_database = str(esdl_profile.database)
    profile_measurement = str(esdl_profile.measurement)
    profile_field = str(esdl_profile.field)
    ssl_setting = False
    if "https" in profile_host:
        profile_host = profile_host[8:]
        ssl_setting = True
    elif "http" in profile_host:
        profile_host = profile_host[7:]
    # why is this here?
    if profile_port == 443:
        ssl_setting = True

    influx_host = f"{profile_host}:{profile_port}"
    if influx_host in influx_cred_map:
        (username, password) = influx_cred_map[influx_host]
    else:
        username = None
        password = None
    conn_settings = ConnectionSettings(
        host=profile_host,
        port=profile_port,
        database=profile_database,
        username=username or "",
        password=password or "",
        ssl=ssl_setting,
        verify_ssl=ssl_setting,
    )
    time_series_data = InfluxDBProfileManager(conn_settings)
    time_series_data.load_influxdb(
        measurement=profile_measurement,
        fields=[profile_field],
        from_datetime=cast(datetime, esdl_profile.startDate),
        to_datetime=cast(datetime, esdl_profile.endDate),
        filters=_normalize_influx_filters(str(esdl_profile.filters)
                                          if esdl_profile.filters else None),
    )
    # Error check start and end dates of profiles

    # I do not think this is required since you set it in mapeditor.
    if time_series_data.end_datetime != esdl_profile.endDate:
        logger.error(
            f"The user input profile end datetime: {esdl_profile.endDate} does not match the end"
            f" datetime in the datbase: {time_series_data.end_datetime} for variable: "
            f"{esdl_profile.field}",
            extra={"esdl_object_id": esdl_profile.id},
        )
        raise RuntimeError(
            f"The user input profile end datetime: {esdl_profile.endDate} does not match the end"
            f" datetime in the datbase: {time_series_data.end_datetime} for variable: "
            f"{esdl_profile.field}"
        )
    if time_series_data.start_datetime != esdl_profile.startDate:
        logger.error(
            f"The user input profile start datetime: {esdl_profile.startDate} does not match the"
            f" start date in the datbase: {time_series_data.start_datetime} for variable: "
            f"{esdl_profile.field}",
            extra={"esdl_object_id": esdl_profile.id},
        )
        raise RuntimeError(
            f"The user input profile start datetime: {esdl_profile.startDate} does not match the"
            f" start date in the datbase: {time_series_data.start_datetime} for variable: "
            f"{esdl_profile.field}"
        )
    if time_series_data.start_datetime != time_series_data.profile_data_list[0][0]:
        logger.error(
            f"The profile's variable value for the start datetime: "
            f"{time_series_data.start_datetime} does not match the start datetime of the"
            f" profile data: {time_series_data.profile_data_list[0][0]}",
            extra={"esdl_object_id": esdl_profile.id},
        )
        raise RuntimeError(
            f"The profile's variable value for the start datetime: "
            f"{time_series_data.start_datetime} does not match the start datetime of the"
            f" profile data: {time_series_data.profile_data_list[0][0]}"
        )
    if time_series_data.end_datetime != time_series_data.profile_data_list[-1][0]:
        logger.error(
            f"The profile's variable value for the end datetime: "
            f"{time_series_data.end_datetime} does not match the end datetime of the"
            f" profile data: {time_series_data.profile_data_list[-1][0]}",
            extra={"esdl_object_id": esdl_profile.id},
        )
        raise RuntimeError(
            f"The profile's variable value for the end datetime: "
            f"{time_series_data.end_datetime} does not match the end datetime of the"
            f" profile data: {time_series_data.profile_data_list[-1][0]}"
        )

    unit = get_unit(esdl_profile)
    dates = [time_stamp for time_stamp, _ in time_series_data.profile_data_list]
    values = [
        convert_to_unit(value, esdl_profile.profileQuantityAndUnit, unit) * esdl_profile.multiplier
        for _, value in time_series_data.profile_data_list
    ]
    data_points = {"date": dates, "values": values}

    return pd.DataFrame(data_points)


def get_unit(profile: esdl.InfluxDBProfile) -> esdl.PhysicalQuantityEnum:
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
