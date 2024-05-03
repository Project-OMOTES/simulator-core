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

"""atesCluster class."""
import uuid
from typing import Dict
import os


from simulator_core.entities.assets.asset_abstract import AssetAbstract
from simulator_core.entities.assets.asset_defaults import (
    DEFAULT_DIAMETER,
    DEFAULT_POWER,
    DEFAULT_PRESSURE,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_TEMPERATURE_RETURN,
    PROPERTY_TEMPERATURE_SUPPLY,
)

from simulator_core.entities.assets.esdl_asset_object import EsdlAssetObject
from simulator_core.solver.network.assets.production_asset import ProductionAsset
from simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
)

path = os.path.dirname(__file__)
import jnius_config # noqa
jnius_config.add_classpath(os.path.join(path, 'bin/rosim-batch-0.4.2.jar'))
from jnius import autoclass # noqa
javaioFile = autoclass('java.io.File')
xmlfile = os.path.join(path, 'bin/sequentialTemplate_v0.4.2_template.xml')
xmlfilejava = javaioFile(xmlfile)


class AtesCluster(AssetAbstract):
    """A AtesCluster represents an asset that consumes heat and produces heat."""

    def __init__(
            self,
            asset_name: str,
            asset_id: str,
    ):
        """Initialize a AtesCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        :param PandapipesNet pandapipe_net: Pandapipes network object to register asset to.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id)

        self._internal_diameter = DEFAULT_DIAMETER
        self.temperature_supply = DEFAULT_TEMPERATURE
        self.temperature_return: float = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        self.pressure_input = DEFAULT_PRESSURE
        self.thermal_power_allocation = DEFAULT_POWER
        self.mass_flowrate = 0
        self.solver_asset = ProductionAsset(uuid.uuid4())
        # Output list
        self.output: list = []

        self.init_rosim()

    def set_setpoints(self, setpoints: Dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_SUPPLY,
            PROPERTY_TEMPERATURE_RETURN,
            PROPERTY_HEAT_DEMAND,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if not necessary_setpoints.issubset(setpoints_set):
            # Print missing setpoints
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )
        self.thermal_power_allocation = setpoints[PROPERTY_HEAT_DEMAND]
        self.temperature_return = setpoints[PROPERTY_TEMPERATURE_RETURN]
        self.temperature_supply = setpoints[PROPERTY_TEMPERATURE_SUPPLY]
        adjusted_mass_flowrate = heat_demand_and_temperature_to_mass_flow(
            self.thermal_power_allocation, self.temperature_supply, self.temperature_return
        )

        [self.temperature_supply, self.temperature_return] = self.run_rosim(adjusted_mass_flowrate,
                                                                            self.temperature_supply,
                                                                            self.temperature_return)

        if adjusted_mass_flowrate > 0:
            self.solver_asset.supply_temperature = self.temperature_return
        else:
            self.solver_asset.supply_temperature = self.temperature_supply
        self.solver_asset.mass_flow_rate_set_point = adjusted_mass_flowrate  # type: ignore

    def add_physical_data(self, esdl_asset: EsdlAssetObject) -> None:
        """Method to add physical data to the asset.

        :param EsdlAssetObject esdl_asset: The esdl asset object to add the physical data from.
         :return:
        """

    def write_to_output(self) -> None:
        """Placeholder to write the asset to the output.

        The output list is a list of dictionaries, where each dictionary
        represents the output of its asset for a specific timestep.
        """
        output_dict = {
            PROPERTY_MASSFLOW: self.solver_asset.get_mass_flow_rate(1),
            PROPERTY_PRESSURE_SUPPLY: self.solver_asset.get_pressure(0),
            PROPERTY_PRESSURE_RETURN: self.solver_asset.get_pressure(1),
            PROPERTY_TEMPERATURE_SUPPLY: self.solver_asset.get_temperature(0),
            PROPERTY_TEMPERATURE_RETURN: self.solver_asset.get_temperature(1),
        }
        self.output.append(output_dict)

    def init_rosim(self) -> None:
        """Function to initailized Rosim from XML file."""
        RosimSequential = autoclass('tno.calc.RosimSequential')

        self.rosimObj = RosimSequential(xmlfilejava, False, 2)

    def run_rosim(self, mass_flow_rate: float, temperature_supply: float,
                  temperature_return: float) -> tuple[float, float]:
        """Function to calculate storage temperature after injection and production.

        :param float mass_flow_rate: mass flow rate going to (positive) / going out (negative)
        to ATES [kg/s]
        :param float temperature_supply: temperature in the hot pipe of ATES [K]
        :param float temperature_return: temperature in the cold pipe of ATES [K]
        """
        volume_flow = mass_flow_rate * 3600 / 1000
        timestep = 1  # HARDCODED to 1 hour

        ates_flow = [volume_flow, -1 * volume_flow]
        if volume_flow > 0:
            T = [temperature_supply - 273, -1]  # Celcius
        elif volume_flow < 0:
            T = [-1, temperature_return - 273]  # Celcius
        else:
            T = [-1, -1]

        Tstorage = self.rosimObj.getTempsNextTimeStep(ates_flow, T, timestep)

        return Tstorage[0] + 273, Tstorage[1] + 273
