"""Module to read the esdl profiles from an energy system."""
from esdl.profiles.influxdbprofilemanager import InfluxDBProfileManager
from esdl.units.conversion import ENERGY_IN_J, POWER_IN_W, convert_to_unit
import esdl
from esdl.esdl_handler import EnergySystemHandler
from typing import Dict
import pandas as pd


def parse_esdl_profiles(esh: EnergySystemHandler) -> Dict[str, pd.DataFrame]:
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


def get_data_from_profile(profile: esdl.InfluxDBProfile) -> pd.DataFrame:
    """Method to get the data from the esdl influxdb profile.

    This method tries to get the data from the esdl profile.
    :param esdl_profile: esdl.Profile with the profile
    :return: pandas.DataFrame with the data
    """
    influx_cred_map = {
        "wu-profiles.esdl-beta.hesi.energy:443": ("warmingup", "warmingup"),
        "omotes-poc-test.hesi.energy:8086": ("write-user", "nwn_write_test"),
    }
    profile_host = profile.host
    ssl_setting = False
    if "https" in profile_host:
        profile_host = profile_host[8:]
        ssl_setting = True
    elif "http" in profile_host:
        profile_host = profile_host[7:]
    # why is this here?
    if profile.port == 443:
        ssl_setting = True

    influx_host = "{}:{}".format(profile_host, profile.port)
    if influx_host in influx_cred_map:
        (username, password) = influx_cred_map[influx_host]
    else:
        username = None
        password = None
    time_series_data = InfluxDBProfileManager.create_esdl_influxdb_profile_manager(
        profile,
        username,
        password,
        ssl_setting,
        ssl_setting,
    )
    # Error check start and end dates of profiles

    # I do not thing this is required since you set it in mapeditor.
    if time_series_data.end_datetime != profile.endDate:
        raise RuntimeError(
            f"The user input profile end datetime: {profile.endDate} does not match the end"
            f" datetime in the datbase: {time_series_data.end_datetime} for variable: "
            f"{profile.field}"
        )
    if time_series_data.start_datetime != profile.startDate:
        raise RuntimeError(
            f"The user input profile start datetime: {profile.startDate} does not match the"
            f" start date in the datbase: {time_series_data.start_datetime} for variable: "
            f"{profile.field}"
        )
    if time_series_data.start_datetime != time_series_data.profile_data_list[0][0]:
        raise RuntimeError(
            f"The profile's variable value for the start datetime: "
            f"{time_series_data.start_datetime} does not match the start datetime of the"
            f" profile data: {time_series_data.profile_data_list[0][0]}"
        )
    if time_series_data.end_datetime != time_series_data.profile_data_list[-1][0]:
        raise RuntimeError(
            f"The profile's variable value for the end datetime: "
            f"{time_series_data.end_datetime} does not match the end datetime of the"
            f" profile data: {time_series_data.profile_data_list[-1][0]}"
        )

    unit = get_unit(profile)
    dates = [time_stamp for time_stamp, _ in
             time_series_data.profile_data_list]
    values = [convert_to_unit(value, profile.profileQuantityAndUnit, unit) * profile.multiplier
              for _, value in time_series_data.profile_data_list]
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
        esdl.PhysicalQuantityEnum.ENERGY: ENERGY_IN_J
    }
    try:
        profile_unit = profile.profileQuantityAndUnit.reference.physicalQuantity
    except AttributeError:
        profile_unit = profile.profileQuantityAndUnit.physicalQuantity
    if profile_unit in conversion_dict:
        return conversion_dict[profile_unit]
    return profile_unit


if __name__ == "__main__":
    esdl_file = r'.\testdata\test1.esdl'
    esh = EnergySystemHandler()
    es = esh.load_file(esdl_file)
    print(parse_esdl_profiles(esh))
