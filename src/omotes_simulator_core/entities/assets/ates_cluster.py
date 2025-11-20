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
    DEFAULT_TEMPERATURE,
    DEFAULT_TEMPERATURE_DIFFERENCE,
    PROPERTY_HEAT_DEMAND,
    PROPERTY_MASSFLOW,
    PROPERTY_PRESSURE_RETURN,
    PROPERTY_PRESSURE_SUPPLY,
    PROPERTY_TEMPERATURE_IN,
    PROPERTY_TEMPERATURE_OUT,
)
from omotes_simulator_core.entities.assets.pyjnius_loader import PyjniusLoader
from omotes_simulator_core.entities.assets.utils import (
    celcius_to_kelvin,
    heat_demand_and_temperature_to_mass_flow,
    kelvin_to_celcius,
)
from omotes_simulator_core.solver.network.assets.production_asset import HeatBoundary
from omotes_simulator_core.solver.utils.fluid_properties import fluid_props

logger = logging.getLogger(__name__)


class AtesCluster(AssetAbstract):
    """An AtesCluster contains Ates assets that consumes heat and produces heat."""

    temperature_in: float
    """The inlet temperature of the asset [K]."""

    temperature_out: float
    """The outlet temperature of the asset [K]."""

    thermal_power_allocation: float
    """The thermal for injection (positive) or production (negative) by the asset [W]."""

    mass_flowrate: float
    """The flow rate going in or out by the asset [kg/s]."""

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
        self.temperature_in = DEFAULT_TEMPERATURE
        self.temperature_out = DEFAULT_TEMPERATURE - DEFAULT_TEMPERATURE_DIFFERENCE
        self.hot_well_temperature = self.temperature_in
        self.cold_well_temperature = self.temperature_out
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
        self.wellbore_diameter = 31.0  # inch
        self.max_charge_volume_flow = 500.0
        self.max_discharge_volume_flow = 500.0

        # Output list
        self.output: list = []
        self.pyjnius_loader = PyjniusLoader.get_loader()

        self.current_time = datetime.now()
        self._init_rosim()
        self.first_time_step = True

    def _calculate_massflowrate(self) -> None:
        """Calculate mass flowrate of the asset."""
        self.mass_flowrate = heat_demand_and_temperature_to_mass_flow(
            self.thermal_power_allocation, self.temperature_in, self.temperature_out
        )

    def _set_solver_asset_setpoint(self) -> None:
        """Set the setpoint of solver asset."""
        if self.mass_flowrate >= 0:
            self.solver_asset.supply_temperature = self.cold_well_temperature  # injection
        else:
            self.solver_asset.supply_temperature = self.hot_well_temperature  # production
        self.solver_asset.mass_flow_rate_set_point = self.mass_flowrate  # type: ignore

    def set_setpoints(self, setpoints: dict) -> None:
        """Placeholder to set the setpoints of an asset prior to a simulation.

        :param Dict setpoints: The setpoints that should be set for the asset.
            The keys of the dictionary are the names of the setpoints and the values are the values
        """
        if self.current_time == self.time:
            return
        self.current_time = self.time
        # Default keys required
        necessary_setpoints = {
            PROPERTY_TEMPERATURE_IN,
            PROPERTY_TEMPERATURE_OUT,
            PROPERTY_HEAT_DEMAND,
        }
        # Dict to set
        setpoints_set = set(setpoints.keys())
        # Check if all setpoints are in the setpoints
        if necessary_setpoints.issubset(setpoints_set):
            self.thermal_power_allocation = -1 * setpoints[PROPERTY_HEAT_DEMAND]
            if self.first_time_step:
                self.temperature_in = setpoints[PROPERTY_TEMPERATURE_IN]
                self.temperature_out = setpoints[PROPERTY_TEMPERATURE_OUT]
                self.first_time_step = False
            else:
                # After the first time step: use solver temperature
                if self.thermal_power_allocation >= 0:
                    self.temperature_in = self.hot_well_temperature
                    self.temperature_out = self.solver_asset.get_temperature(1)
                else:
                    self.temperature_in = self.solver_asset.get_temperature(0)
                    self.temperature_out = self.cold_well_temperature

            self._calculate_massflowrate()
            self._run_rosim()
            self._set_solver_asset_setpoint()
        else:
            # Print missing setpoints
            logger.error(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing.",
                extra={"esdl_object_id": self.asset_id},
            )
            raise ValueError(
                f"The setpoints {necessary_setpoints.difference(setpoints_set)} are missing."
            )

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
        CASING_SIZE = self.wellbore_diameter

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
            PROPERTY_HEAT_DEMAND: 1e6,
            PROPERTY_TEMPERATURE_OUT: celcius_to_kelvin(35),
            PROPERTY_TEMPERATURE_IN: celcius_to_kelvin(85),
        }
        # initially charging 12 weeks with 85-35 temperature 1 MW
        logger.info("initializing ates with charging for 12 weeks")
        for i in range(12):
            logger.info(f"charging ates week {i + 1}")
            self.set_time_step(3600 * 24 * 7)
            self.set_time(datetime(2023, 1, i + 1, 0, 0, 0))
            self.first_time_step = True  # dont get temperature from solver
            self.set_setpoints(setpoints=setpoints)

    def _run_rosim(self) -> None:
        """Function to calculate storage temperature after injection and production."""
        saline_density = self._get_saline_density(
            20, kelvin_to_celcius((self.hot_well_temperature + self.cold_well_temperature) / 2)
        )

        volume_flow = self.mass_flowrate * 3600 / saline_density  # convert to second and
        if volume_flow > 0:
            volume_flow = min(volume_flow, self.max_charge_volume_flow)
        if volume_flow < 0:
            volume_flow = -1 * min(abs(volume_flow), self.max_discharge_volume_flow)

        # hardcoded saline
        timestep = self.time_step / 3600  # convert to hours

        rosim_input_flow = [volume_flow, -1 * volume_flow]  # the first-element is for hot well
        # and the second-element is for cold well. positive flow is charge and negative flow
        # is discharge

        if volume_flow > 0:
            rosim_input_temperature = [kelvin_to_celcius(self.temperature_in), -1]  # Celcius, -1 in
        # injection well to make sure it is not used
        elif volume_flow < 0:
            rosim_input_temperature = [
                -1,
                kelvin_to_celcius(self.temperature_out),
            ]  # Celcius, -1 in
        # producer well to make sure it is not used
        else:
            rosim_input_temperature = [-1, -1]  # -1 in both producer and injection well to make
        # sure it is not used

        ates_temperature = self.rosim.calcTimeStepAndGetTemps(
            rosim_input_flow, rosim_input_temperature, timestep
        )

        self.hot_well_temperature = celcius_to_kelvin(ates_temperature[0])  # convert to K
        self.cold_well_temperature = celcius_to_kelvin(ates_temperature[1])  # convert to K

    def get_state(self) -> dict[str, float]:
        """Function to calculate the maximum charge and discharge rate based on NVOE."""
        P = self.aquifer_depth * 0.1  # bar assume pressure increase 1 bar per 10 m depth

        average_temperature = (self.temperature_in + self.temperature_out) / 2
        water_density = fluid_props.get_density(average_temperature)
        water_heat_capacity = fluid_props.get_heat_capacity(average_temperature)

        max_extraction_flow_cold_well = self._get_max_flowrate_extraction_norm(
            P, kelvin_to_celcius(self.cold_well_temperature)
        )
        max_injection_flow_cold_well = self._get_max_flowrate_injection_norm(
            P, kelvin_to_celcius(self.cold_well_temperature)
        )

        max_extraction_flow_hot_well = self._get_max_flowrate_extraction_norm(
            P, kelvin_to_celcius(self.hot_well_temperature)
        )
        max_injection_flow_hot_well = self._get_max_flowrate_injection_norm(
            P, kelvin_to_celcius(self.hot_well_temperature)
        )

        self.max_charge_volume_flow = min(
            max_extraction_flow_cold_well, max_injection_flow_hot_well
        )
        self.max_discharge_volume_flow = min(
            max_injection_flow_cold_well, max_extraction_flow_hot_well
        )

        max_charge_power = (
            (self.hot_well_temperature - self.cold_well_temperature)
            * self.max_charge_volume_flow
            * water_density
            / 3600
            * water_heat_capacity
        )

        max_discharge_power = (
            (self.hot_well_temperature - self.cold_well_temperature)
            * self.max_discharge_volume_flow
            * water_density
            / 3600
            * water_heat_capacity
        )

        return {"max_charge_power": max_charge_power, "max_discharge_power": max_discharge_power}

    def _get_max_flowrate_extraction_norm(self, P: float, T: float) -> float:
        """Function to calculate the maximum flowrate of production in norm."""
        grav_accel = 9.81  # m/s2
        saline_density = self._get_saline_density(P, T)
        saline_viscosity = self._get_saline_viscosity(P, T)
        aquifer_permeability = self.aquifer_permeability * 9.8692326671601e-16  # mD to m2
        # diameter
        well_radius = 0.5 * self.wellbore_diameter * 0.0254  # m

        max_extract_flow_velocity = (
            2 * 60 * 60 * aquifer_permeability * saline_density * grav_accel / saline_viscosity
        )  # m/h

        max_flowrate = (
            2 * math.pi * well_radius * self.aquifer_thickness * max_extract_flow_velocity
        )

        max_flowrate = max_flowrate * self.aquifer_depth * 0.01  # using depth factor because ATES
        # is deeper than WKO

        return max_flowrate

    def _get_max_flowrate_injection_norm(self, P: float, T: float) -> float:
        """Function to calculate the maximum flowrate of injection in norm."""
        grav_accel = 9.81  # m/s2
        saline_density = self._get_saline_density(P, T)
        saline_viscosity = self._get_saline_viscosity(P, T)
        aquifer_permeability = self.aquifer_permeability * 9.8692326671601e-16  # mD to m2
        # diameter
        well_radius = 0.5 * self.wellbore_diameter * 0.0254  # m

        cloggingVel = 0.3
        membraneFilterIndex = 0.1
        equivLoadHoursPerYear = 3500
        max_infiltrate_flow_velocity = (
            1000
            * math.pow(
                576 * aquifer_permeability * saline_density * grav_accel / saline_viscosity, 0.6
            )
            * math.sqrt(cloggingVel / (2 * membraneFilterIndex * equivLoadHoursPerYear))
        )

        max_flowrate = (
            2 * math.pi * well_radius * self.aquifer_thickness * max_infiltrate_flow_velocity
        )  # m/h

        return max_flowrate

    def _get_saline_density(self, P: float, T: float) -> float:
        """Function to calculate the saline density."""
        P = P * 1e5 * 1e-6  # Bar to MPa
        S = self.salinity * 1e-6  # ppm to kg/kg

        density_fresh = 1 + 1e-6 * (
            -80.0 * T
            - 3.3 * T * T
            + 0.00175 * T * T * T
            + 489.0 * P
            - 2.0 * T * P
            + 0.016 * T * T * P
            - 1.3e-5 * T * T * T * P
            - 0.333 * P * P
            - 0.002 * T * P * P
        )

        density = density_fresh + S * (
            0.668
            + 0.44 * S
            + 1e-6
            * (
                300.0 * P
                - 2400.0 * P * S
                + T * (80.0 + 3.0 * T - 3300.0 * S - 13.0 * P + 47.0 * P * S)
            )
        )

        density = density * 1000  # g/cm3 to kg/m3

        return density

    def _get_saline_viscosity(self, P: float, T: float) -> float:
        """Function to calculate the saline viscosity."""
        P = P * 1e5 * 1e-6  # Bar to MPa
        S = self.salinity * 1e-6  # ppm to kg/kg

        viscosity = (
            0.1
            + 0.333 * S
            + (1.65 + 91.90 * S * S * S)
            * math.exp(
                -(0.42 * math.pow((math.pow(S, 0.8) - 0.17), 2.0) + 0.045) * math.pow(T, 0.8)
            )
        )

        viscosity = viscosity * 1e-3  # cP to Pas

        return viscosity
