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
import logging
import math
import os
from datetime import datetime

from omotes_simulator_core.entities.assets.asset_abstract import AssetAbstract
from omotes_simulator_core.entities.assets.asset_defaults import (
    ATES_DEFAULTS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_COLD_WELL_TEMPERATURE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_HOT_WELL_TEMPERATURE,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_SET_PRESSURE,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
    PROPERTY_TIMESTEP,
)
from omotes_simulator_core.entities.assets.controller.temperature_data import (
    celcius_to_kelvin,
    kelvin_to_celcius,
)
from omotes_simulator_core.entities.assets.pyjnius_loader import PyjniusLoader
from omotes_simulator_core.entities.assets.utils import (
    heat_demand_and_temperature_to_mass_flow,
    mass_flow_and_temperature_to_heat_demand,
)
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

logger = logging.getLogger(__name__)

MINIMUM_TEMPERATURE_DIFFERENCE = 1e-3
"""Minimum temperature difference over the asset to calculate a mass flow rate [K]."""


class AtesCluster(AssetAbstract):
    """An AtesCluster contains Ates assets that consumes heat and produces heat."""

    temperature_connection_0: float
    """The temperature at connection point 0 of the asset [K].

    Connection point 0 is always connected to the supply (hot) side of the network. It is the
    inflow of the asset when charging and the outflow of the asset when discharging.
    """

    temperature_connection_1: float
    """The temperature at connection point 1 of the asset [K].

    Connection point 1 is always connected to the return (cold) side of the network. It is the
    outflow of the asset when charging and the inflow of the asset when discharging.
    """

    thermal_power_allocation: float
    """The thermal power charged (positive) or discharged (negative) by the asset [W].

    This follows the controller convention: heat flowing from the network into the asset
    (charging the aquifer) is positive, heat flowing from the asset into the network
    (discharging the aquifer) is negative.
    """

    mass_flowrate: float
    """The mass flow rate set point of the asset [kg/s].

    Positive when charging (flow from connection point 0 to 1) and negative when discharging
    (flow from connection point 1 to 0).
    """

    aquifer_depth: float
    """The depth of the aquifer [m]."""

    aquifer_thickness: float
    """The thickness of the aquifer [m]."""

    aquifer_mid_temperature: float
    """The mid temperature of the aquifer [Celcius]."""

    aquifer_net_to_gross: float
    """The net to gross of the aquifer [%]."""

    aquifer_porosity: float
    """The porosity of the aquifer [%]."""

    aquifer_permeability: float
    """The permeability of the aquifer [mD]."""

    aquifer_anisotropy: float
    """The anisotropy of the aquifer [-]."""

    salinity: float
    """The salinity of the aquifer [ppm]."""

    well_casing_size: float
    """The casing size of the well [inch]."""

    well_distance: float
    """The distance of the well [m]."""

    pyjnius_loader: PyjniusLoader
    """Loader object to delay importing pyjnius module and Java classes."""

    def __init__(
        self,
        asset_name: str,
        asset_id: str,
        port_ids: list[str],
        aquifer_depth: float,
        aquifer_thickness: float,
        aquifer_mid_temperature: float,
        aquifer_net_to_gross: float,
        aquifer_porosity: float,
        aquifer_permeability: float,
        aquifer_anisotropy: float,
        salinity: float,
        well_casing_size: float,
        well_distance: float,
    ) -> None:
        """Initialize a AtesCluster object.

        :param str asset_name: The name of the asset.
        :param str asset_id: The unique identifier of the asset.
        """
        super().__init__(asset_name=asset_name, asset_id=asset_id, connected_ports=port_ids)
        self.temperature_connection_0 = DEFAULT_TEMPERATURE
        self.temperature_connection_1 = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        self.hot_well_temperature = self.temperature_connection_0
        self.cold_well_temperature = self.temperature_connection_1
        self.thermal_power_allocation = 0  # Watt
        self.mass_flowrate = 0  # kg/s
        self.solver_asset = HeatBoundary(name=self.name, _id=self.asset_id)
        # ATES default properties
        self.aquifer_depth = aquifer_depth  # meters
        self.aquifer_thickness = aquifer_thickness  # meters
        self.aquifer_mid_temperature = aquifer_mid_temperature  # Celcius
        self.aquifer_net_to_gross = aquifer_net_to_gross  # percentage
        self.aquifer_porosity = aquifer_porosity  # percentage
        self.aquifer_permeability = aquifer_permeability  # mD
        self.aquifer_anisotropy = aquifer_anisotropy  # -
        self.salinity = salinity  # ppm
        self.well_casing_size = well_casing_size  # inch
        self.well_distance = well_distance  # meters

        # Output list
        self.output: list = []
        self.pyjnius_loader = PyjniusLoader.get_loader()

        self.current_time = datetime.now()
        self._init_rosim()
        self.first_time_step = True

    def _calculate_massflowrate(self) -> None:
        """Calculate the mass flow rate set point of the asset.

        The temperatures are bound to the connection points of the asset, so the sign of the
        thermal power allocation determines the flow direction: positive (charging) results in a
        positive mass flow rate set point, which is a flow from connection point 0 to connection
        point 1.
        """
        if (
            abs(self.temperature_connection_0 - self.temperature_connection_1)
            < MINIMUM_TEMPERATURE_DIFFERENCE
        ):
            logger.warning(
                f"The temperature difference over asset {self.name} is too small to calculate a"
                + " mass flow rate. The mass flow rate is set to zero.",
                extra={"esdl_object_id": self.asset_id},
            )
            self.mass_flowrate = 0.0
            return
        self.mass_flowrate = -1 * heat_demand_and_temperature_to_mass_flow(
            self.thermal_power_allocation,
            self.temperature_connection_0,
            self.temperature_connection_1,
        )
        self._limit_massflowrate()

    def _get_maximum_mass_flow_rate(self) -> float:
        """Get the maximum mass flow rate the wells of the asset can handle.

        :return float: The maximum mass flow rate of the asset [kg/s].
        """
        if self.thermal_power_allocation >= 0:
            maximum_volume_flow_rate = ATES_DEFAULTS.maximum_flow_charge  # m3/h
        else:
            maximum_volume_flow_rate = ATES_DEFAULTS.maximum_flow_discharge  # m3/h
        density = fluid_props.get_density(
            (self.temperature_connection_0 + self.temperature_connection_1) / 2
        )
        return maximum_volume_flow_rate / 3600 * density

    def _limit_massflowrate(self) -> None:
        """Limit the mass flow rate of the asset to the capacity of the wells.

        The requested thermal power can only be delivered when the temperature difference over
        the asset is large enough. When the aquifer is close to depleted, the required mass flow
        rate runs away and would push the rest of the network out of its operating range. The mass
        flow rate is therefore limited and the thermal power allocation is reduced to the power
        that the asset can actually exchange.
        """
        maximum_mass_flow_rate = self._get_maximum_mass_flow_rate()
        if abs(self.mass_flowrate) <= maximum_mass_flow_rate:
            return
        logger.warning(
            f"The mass flow rate {self.mass_flowrate} of asset {self.name} exceeds the maximum"
            + f" mass flow rate {maximum_mass_flow_rate}. The mass flow rate is limited and the"
            + " requested thermal power is not met.",
            extra={"esdl_object_id": self.asset_id},
        )
        self.mass_flowrate = math.copysign(maximum_mass_flow_rate, self.mass_flowrate)
        self.thermal_power_allocation = mass_flow_and_temperature_to_heat_demand(
            temperature_out=self.temperature_connection_1,
            temperature_in=self.temperature_connection_0,
            mass_flow=self.mass_flowrate,
        )

    def _set_solver_asset_setpoint(self) -> None:
        """Set the setpoint of solver asset.

        The solver asset prescribes its supply temperature at the connection point where the flow
        leaves the asset. The temperature of the inflowing connection point is taken from the
        connected node.
        """
        if self.thermal_power_allocation >= 0:
            # Charging: the flow leaves the asset at connection point 1 (return side).
            self.solver_asset.supply_temperature = self.cold_well_temperature
        else:
            # Discharging: the flow leaves the asset at connection point 0 (supply side).
            self.solver_asset.supply_temperature = self.hot_well_temperature
        self.solver_asset.mass_flow_rate_set_point = self.mass_flowrate  # type: ignore

    def set_setpoints(self, setpoints: dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
            PROPERTY_SET_PRESSURE,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if not (necessary_setpoints.issubset(setpoints_set)):
            logger.error(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing.",
                extra={"esdl_object_id": self.asset_id},
            )
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )
        self.thermal_power_allocation = setpoints[PROPERTY_HEAT_DEMAND]
        charging = self.thermal_power_allocation >= 0
        if self.first_time_step or self.solver_asset.prev_sol[0] == 0.0:
            # The controller supplies the temperatures of the ATES with a producer-like
            # definition, which is swapped between charging and discharging. Connection point 0
            # is always connected to the supply (hot) side of the network and connection point 1
            # to the return (cold) side, so the setpoints are mapped per operating mode.
            if charging:
                self.temperature_connection_0 = setpoints[PROPERTY_TEMPERATURE_IN]
                self.temperature_connection_1 = setpoints[PROPERTY_TEMPERATURE_OUT]
            else:
                self.temperature_connection_0 = setpoints[PROPERTY_TEMPERATURE_OUT]
                self.temperature_connection_1 = setpoints[PROPERTY_TEMPERATURE_IN]
            self.first_time_step = False
        else:
            # After the first time step: the temperature of the inflowing connection point is
            # taken from the solver and the outflowing connection point from the aquifer.
            if charging:
                self.temperature_connection_0 = self.solver_asset.get_temperature(0)
                self.temperature_connection_1 = self.cold_well_temperature
            else:
                self.temperature_connection_0 = self.hot_well_temperature
                self.temperature_connection_1 = self.solver_asset.get_temperature(1)
        self.solver_asset.pre_scribe_mass_flow = not (  # type: ignore
            setpoints[PROPERTY_SET_PRESSURE]
        )
        self._calculate_massflowrate()
        if self.current_time != self.time:
            self._run_rosim()
            self.current_time = self.time
        self._set_solver_asset_setpoint()

    def get_state(self) -> dict[str, float]:
        """Get the state of the asset.

        The controller uses the well temperatures to determine how much power the asset can
        still charge or discharge.

        :return: dict[str, float] A dictionary containing the state of the asset.
        """
        return {
            PROPERTY_HOT_WELL_TEMPERATURE: self.hot_well_temperature,
            PROPERTY_COLD_WELL_TEMPERATURE: self.cold_well_temperature,
            PROPERTY_TIMESTEP: self.time_step,
        }

    def write_to_output(self) -> None:
        """Method to write time step results to the output dict.

        The output list is a list of dictionaries, where each dictionary
        represents the output of the asset for a specific timestep.
        """
        output_dict = {
            PROPERTY_MASSFLOW: self.solver_asset.get_mass_flow_rate(1),
            PROPERTY_PRESSURE_SUPPLY: self.solver_asset.get_pressure(0),
            PROPERTY_PRESSURE_RETURN: self.solver_asset.get_pressure(1),
            PROPERTY_TEMPERATURE_IN: self.solver_asset.get_temperature(0),
            PROPERTY_TEMPERATURE_OUT: self.solver_asset.get_temperature(1),
        }
        self.output.append(output_dict)
        self.first_time_step = False

    def postprocess(self) -> None:
        """Postprocess after a simulation time step to update internal states.

        :return: None
        """
        pass

    def _init_rosim(self) -> None:
        """Function to initailized Rosim from XML file."""
        path = os.path.dirname(__file__)
        xmlfile = os.path.join(path, "bin/sequentialTemplate_v1.2.0_template.xml")
        with open(xmlfile) as fd:
            xml_str = fd.read()

        # overwrite template value with ESDL properties for ROSIM input

        MODEL_TOP = self.aquifer_depth - 100
        AQUIFER_THICKNESS = self.aquifer_thickness
        NZ_AQUIFER = math.floor(AQUIFER_THICKNESS / 2)
        NZ = NZ_AQUIFER + 8
        AQUIFER_TOP = self.aquifer_depth
        AQUIFER_BASE = self.aquifer_depth + self.aquifer_thickness
        SURFACE_TEMPERATURE = self.aquifer_mid_temperature - 0.034 * (
            self.aquifer_depth + self.aquifer_thickness / 2
        )
        AQUIFER_NTG = self.aquifer_net_to_gross
        AQUIFER_PORO = self.aquifer_porosity
        AQUIFER_PERM_XY = self.aquifer_permeability
        AQUIFER_PERM_Z = AQUIFER_PERM_XY / self.aquifer_anisotropy
        SALINITY = self.salinity
        WELL2_X = self.well_distance + 300
        CASING_SIZE = self.well_casing_size

        xml_str = xml_str.replace("$NZ$", str(NZ))
        xml_str = xml_str.replace("$MODEL_TOP$", str(MODEL_TOP))
        xml_str = xml_str.replace("$TIME_STEP_UNIT$", str(2))
        xml_str = xml_str.replace("$WELL2_X$", str(WELL2_X))
        xml_str = xml_str.replace("$AQUIFER_TOP$", str(AQUIFER_TOP))
        xml_str = xml_str.replace("$AQUIFER_BASE$", str(AQUIFER_BASE))
        xml_str = xml_str.replace("$CASING_SIZE$", str(CASING_SIZE))
        xml_str = xml_str.replace("$SURFACE_TEMPERATURE$", str(SURFACE_TEMPERATURE))
        xml_str = xml_str.replace("$SALINITY$", str(SALINITY))
        xml_str = xml_str.replace("$NZ_AQUIFER$", str(NZ_AQUIFER))
        xml_str = xml_str.replace("$AQUIFER_THICKNESS$", str(AQUIFER_THICKNESS))
        xml_str = xml_str.replace("$AQUIFER_PORO$", str(AQUIFER_PORO))
        xml_str = xml_str.replace("$AQUIFER_NTG$", str(AQUIFER_NTG))
        xml_str = xml_str.replace("$AQUIFER_PERM_XY$", str(AQUIFER_PERM_XY))
        xml_str = xml_str.replace("$AQUIFER_PERM_Z$", str(AQUIFER_PERM_Z))

        temp_xmlfile_path = os.path.join(path, "bin/ates_sequential_temp.xml")
        with open(temp_xmlfile_path, "w") as temp_xmlfile:
            temp_xmlfile.write(xml_str)

        javaioFile = self.pyjnius_loader.load_class("java.io.File")
        RosimSequential = self.pyjnius_loader.load_class("rosim.calc.RosimSequential")
        xmlfilejava = javaioFile(temp_xmlfile_path)
        logLevel = self.pyjnius_loader.load_class("org.slf4j.event.Level")
        self.rosim = RosimSequential(xmlfilejava, logLevel, -1)

        setpoints = {
            PROPERTY_HEAT_DEMAND: 10e6,
            PROPERTY_TEMPERATURE_OUT: celcius_to_kelvin(35),
            PROPERTY_TEMPERATURE_IN: celcius_to_kelvin(85),
            PROPERTY_SET_PRESSURE: False,
        }
        # initially charging 12 weeks with 85-35 temperature 1 MW
        logger.info("initializing ates with charging for 12 weeks")
        for i in range(20):
            logger.info(f"charging ates week {i + 1}")
            self.set_time_step(3600 * 24 * 7)
            self.set_time(datetime(2023, 1, i + 1, 0, 0, 0))
            self.first_time_step = True  # dont get temperature from solver
            self.set_setpoints(setpoints=setpoints)

    def _run_rosim(self) -> None:
        """Function to calculate storage temperature after injection and production."""
        volume_flow = self.mass_flowrate * 3600 / 1027  # convert to second and hardcoded saline
        # density needs to change with PVT calculation
        timestep = self.time_step / 3600  # convert to hours

        rosim_input__flow = [volume_flow, -1 * volume_flow]  # first element is for the hot well
        # and second element is for the cold well. A positive flow injects into the well and a
        # negative flow produces from the well. A positive mass flow rate of the asset is
        # charging, which injects into the hot well and produces from the cold well.

        if volume_flow > 0:
            # Charging: water from the supply side of the network (connection point 0) is
            # injected into the hot well, the cold well is produced.
            rosim_input_temperature = [
                kelvin_to_celcius(self.temperature_connection_0),
                -1,
            ]  # Celcius, -1 in the cold well to make sure it is not used
        elif volume_flow < 0:
            # Discharging: water from the return side of the network (connection point 1) is
            # injected into the cold well, the hot well is produced.
            rosim_input_temperature = [
                -1,
                kelvin_to_celcius(self.temperature_connection_1),
            ]  # Celcius, -1 in the hot well to make sure it is not used
        else:
            rosim_input_temperature = [-1, -1]  # -1 in both the hot and cold well to make
            # sure it is not used
        logger.debug("rosim input temperature %s", rosim_input_temperature)
        logger.debug("rosim input flow %s", rosim_input__flow)

        ates_temperature = self.rosim.calcTimeStepAndGetTemps(
            rosim_input__flow, rosim_input_temperature, timestep
        )
        if ates_temperature[1] < 0:
            logger.info("Temperature Rossim to low")
        logger.debug("rosim output temperature %s", ates_temperature)
        self.hot_well_temperature = celcius_to_kelvin(ates_temperature[0])  # convert to K
        self.cold_well_temperature = celcius_to_kelvin(ates_temperature[1])  # convert to K

    def get_heat_supplied(self) -> float:
        """Get the actual heat exchanged with the network by the asset.

        The sign follows the controller convention: positive when the asset is charging (heat
        from the network into the aquifer) and negative when it is discharging.

        :return float: The actual heat supplied by the asset [W].
        """
        return (
            self.solver_asset.get_internal_energy(1) - self.solver_asset.get_internal_energy(0)
        ) * self.solver_asset.get_mass_flow_rate(0)

    def is_converged(self) -> bool:
        """Check if the asset has converged with accepted error of 0.1%.

        :return: True if the asset has converged, False otherwise
        """
        if self.solver_asset.pre_scribe_mass_flow:  # type: ignore
            return abs(self.get_heat_supplied() - self.thermal_power_allocation) < (
                abs(self.thermal_power_allocation) * 0.001
            )
        return True
