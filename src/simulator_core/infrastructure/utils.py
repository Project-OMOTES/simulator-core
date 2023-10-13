"""Module containing utility functions."""
from esdl.esdl_handler import EnergySystemHandler
from pathlib import Path


def pyesdl_from_file(file_path: str) -> EnergySystemHandler:
    """
    Loads esdl file into memory and returns a handle to be able to use this file.

    Please note that it is not checked if the file is a valid esdl file.
    :param file_path: string pointing to the esdl file to be loaded into memory
    """
    if not Path(file_path).is_file():
        raise FileNotFoundError("Not a valid path to an ESDL file")
    esh = EnergySystemHandler()
    esh.load_file(file_path)
    return esh


def pyesdl_from_string(input_str: str) -> EnergySystemHandler:
    """
    Loads esdl file from a string into memory.

    Please note that it is not checked if the contents of the string is a valid esdl.
    :param input_str: string containing the contents of an esdl file.
    """
    esh = EnergySystemHandler()
    esh.load_from_string(input_str)
    return esh
