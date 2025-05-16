# code copied from: https://github.com/Dennis-van-Gils/python-fluidprop/blob/main/src/fluidprop.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Easy access to thermodynamic fluid properties as a function of temperature
and pressure. Comes with a minimal command-line interface for quick inspection.
Provides class ``FluidProperties()`` useful for working out dataseries in your
own scripts.

Thermodynamic properties are provided by CoolProp:
* http://www.coolprop.org/
* http://pubs.acs.org/doi/abs/10.1021/ie4033999
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/python-fluidprop"
__date__ = "13-05-2024"
__version__ = "1.2.0"

from typing import Union

import CoolProp.CoolProp as CP
import numpy as np
import numpy.typing as npt

ZERO_C = 273.15
"""0 'C in K"""
P_ATM = 1.01325
"""bar per 1 atm"""
P_PSI = 1 / 14.504
"""bar per 1 psi"""
HRULE = "-" * 60
"""Horizontal rule"""

# fmt: off
FLUID_SELECTION = [
    ("Air"                  , "mixture"),
    ("Hydrogen"             , "H_{2}"),
    ("Helium"               , "He"),
    ("Nitrogen"             , "N_{2}"),
    ("Oxygen"               , "O_{2}"),
    ("CarbonDioxide"        , "CO_{2}"),
    ("SulfurHexafluoride"   , "SF_{6}"),
    ("Water"                , "H_{2}O"),
    ("HeavyWater"           , "D_{2}O"),
    ("Methanol"             , "CH_{3}OH"),
    ("Ethanol"              , "C_{2}H_{5}OH"),
    # ("Acetone"              , "C_{3}H_{6}O"),
]
# fmt: on
"""Subselection of the most common fluids to chose from.
It is a list of tuples, where each tuple contains 2 strings as follows ::

    tuple[0] (str): CoolProp name
    tuple[1] (str): Chemical name
"""

# ------------------------------------------------------------------------------
#   FluidProperties
# ------------------------------------------------------------------------------


class FluidProperties:
    """Evaluates thermodynamic fluid properties of the given fluid at the given
    temperature(s) in ``['C]`` and pressure(s) in ``[bar]``. The results are
    stored as properties to this class as ``numpy.ndarray`` arrays. Useful for
    working out dataseries.

    Example ::

        fluid = FluidProperties("Water", 20, 1)
        print(fluid.rho)  # [998.2065435]

        fluid = FluidProperties("Water", [20, 21, 22], 1)
        print(fluid.rho)  # [998.2065435  997.99487638 997.77288644]

    Args:
        coolprop_name (`str`):
            The CoolProp name of the fluid to evaluate.

        T_in_deg_C (`float` | `list[float]` | `numpy.ndarray[]`):
            Temperature ['C] to evaluate fluid properties at.

        P_in_bar (`float` | `list[float]` | `numpy.ndarray[]`):
            Pressure [bar] to evaluate fluid properties at.

    Properties:
        coolprop_name (`str`):
            CoolProp name of the fluid.

        formula (`str`):
            Chemical formula of the fluid.

        MW (`float`):
            Molecular weight [kg/mol].

        T (`numpy.ndarray[]`):
            Evaluated temperature [K].

        P (`numpy.ndarray[]`):
            Evaluated pressure [Pa].

        rho (`numpy.ndarray[]`):
            Density [kg/m^3].

        nu (`numpy.ndarray[]`):
            Kinematic viscosity [m^2/s].

        eta (`numpy.ndarray[]`):
            Dynamic/shear viscosity [kg/(m s)].

        alpha (`numpy.ndarray[]`):
            Thermal expansion coefficient [1/K].

        kappa (`numpy.ndarray[]`):
            Thermal diffusivity [m^2/s].

        lambda_ (`numpy.ndarray[]`):
            Thermal conductivity [W/(m K)].

        Cp (`numpy.ndarray[]`):
            Isobaric heat capacity [J/(kg K)].

        Cv (`numpy.ndarray[]`):
            Isochoric heat capacity [J/(kg K)].

        comp (`numpy.ndarray[]`):
            Isothermal compressibility [1/Pa].

        Pr (`numpy.ndarray[]`):
            Prandtl number.
    """

    def __init__(
        self,
        coolprop_name: str,
        T_in_deg_C: Union[float, list[float], npt.NDArray],
        P_in_bar: Union[float, list[float], npt.NDArray],
    ):
        # -------------------------
        #   Check input arguments
        # -------------------------

        if isinstance(T_in_deg_C, (float, int)):
            T_in_deg_C = np.array([T_in_deg_C], dtype=float)
        else:
            T_in_deg_C = np.asarray(T_in_deg_C, dtype=float)

        if isinstance(P_in_bar, (float, int)):
            P_in_bar = np.array([P_in_bar], dtype=float)
        else:
            P_in_bar = np.asarray(P_in_bar, dtype=float)

        if T_in_deg_C.ndim != 1 or P_in_bar.ndim != 1:
            raise ValueError(
                "Arguments `T_in_deg_C` and `P_in_bar` must be one-dimensional " "arrays."
            )

        if len(T_in_deg_C) > 1 and len(P_in_bar) == 1:
            P_in_bar = np.repeat(P_in_bar, len(T_in_deg_C))

        if len(P_in_bar) > 1 and len(T_in_deg_C) == 1:
            T_in_deg_C = np.repeat(T_in_deg_C, len(P_in_bar))

        if len(T_in_deg_C) != len(P_in_bar):
            raise ValueError("Arguments `T_in_deg_C` and `P_in_bar` have unequal lengths.")

        array_len = np.size(T_in_deg_C)
        nan_array = np.empty(array_len)
        nan_array[:] = np.nan

        # -----------
        #   Members
        # -----------

        self.coolprop_name: str = coolprop_name
        """CoolProp name of the fluid"""

        self.formula: str = ""
        """Chemical formula of the fluid"""

        self.MW: float = np.nan
        """Molecular weight [kg/mol]"""

        self.T: npt.NDArray[np.float64] = np.add(T_in_deg_C, ZERO_C)
        """Evaluated temperature [K]"""

        self.P: npt.NDArray[np.float64] = np.multiply(P_in_bar, 1e5)
        """Evaluated pressure [Pa]"""

        self.rho: npt.NDArray[np.float64] = np.copy(nan_array)
        """Density [kg/m^3]"""

        self.nu: npt.NDArray[np.float64] = np.copy(nan_array)
        """Kinematic viscosity [m^2/s]"""

        self.eta: npt.NDArray[np.float64] = np.copy(nan_array)
        """Dynamic/shear viscosity [kg/(m s)]"""

        self.alpha: npt.NDArray[np.float64] = np.copy(nan_array)
        """Thermal expansion coefficient [1/K]"""

        self.kappa: npt.NDArray[np.float64] = np.copy(nan_array)
        """Thermal diffusivity [m^2/s]"""

        self.lambda_: npt.NDArray[np.float64] = np.copy(nan_array)
        """Thermal conductivity [W/(m K)]"""

        self.Cp: npt.NDArray[np.float64] = np.copy(nan_array)
        """Isobaric heat capacity [J/(kg K)]"""

        self.Cv: npt.NDArray[np.float64] = np.copy(nan_array)
        """Isochoric heat capacity [J/(kg K)]"""

        self.comp: npt.NDArray[np.float64] = np.copy(nan_array)
        """Isothermal compressibility [1/Pa]"""

        self.Pr: npt.NDArray[np.float64] = np.copy(nan_array)
        """Prandtl number"""

        # ------------------------------
        #   Calculate fluid properties
        # ------------------------------

        found_match = False
        for item_ in FLUID_SELECTION:
            if item_[0] == coolprop_name:
                found_match = True
                self.formula = item_[1]
                break

        if not found_match:
            self.formula = CP.get_fluid_param_string(coolprop_name, "formula")
            self.formula = self.formula.replace("_{1}", "")

        # Molecular weight [kg/mol]
        self.MW = CP.PropsSI(coolprop_name, "M")

        # http://coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function
        requested_quantities = [
            "DMASS",
            "VISCOSITY",
            "ISOBARIC_EXPANSION_COEFFICIENT",
            "CONDUCTIVITY",
            "CPMASS",
            "CVMASS",
            "ISOTHERMAL_COMPRESSIBILITY",
            "PRANDTL",
        ]

        for idx_, (T, P) in enumerate(zip(self.T, self.P)):
            values = np.zeros(len(requested_quantities))
            values[:] = np.nan

            for quantity_idx, quantity in enumerate(requested_quantities):
                try:
                    value = CP.PropsSI(quantity, "T", T, "P", P, coolprop_name)
                except ValueError as e:
                    value = np.nan
                    print(e)

                values[quantity_idx] = value

            # fmt: off
            (
                self.rho[idx_],     # Density                       [kg/m^3]
                self.eta[idx_],     # Dynamic viscosity             [kg/(m s)]
                self.alpha[idx_],   # Thermal expansion coefficient [1/K]
                self.lambda_[idx_], # Thermal conductivity          [W/(m K)]
                self.Cp[idx_],      # Isobaric heat capacity        [J/(kg K)]
                self.Cv[idx_],      # Isochoric heat capacity       [J/(kg K)]
                self.comp[idx_],    # Isothermal compressibility    [1/Pa]
                self.Pr[idx_],      # Prandtl number                [-]
            ) = values
            # fmt: on

        # Derived: Kinematic viscosity [m^2/s]
        self.nu = self.eta / self.rho
        # Derived: Thermal diffusivity [m^2/s]
        self.kappa = self.lambda_ / self.rho / self.Cp
