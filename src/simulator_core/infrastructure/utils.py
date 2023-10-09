from esdl.esdl_handler import EnergySystemHandler
from pathlib import Path


def pyesdl_from_file(file_path: str):
    if not Path(file_path).is_file():
        raise FileNotFoundError("Not a valid path to an ESDL file")
    return EnergySystemHandler().load_file(file_path)


def pyesdl_from_string(input_str: str):
    return EnergySystemHandler().load_from_string(input_str)
