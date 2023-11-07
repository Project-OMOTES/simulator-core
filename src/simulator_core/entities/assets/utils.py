from pandapipes import pandapipesNet


def heat_demand_and_temperature_to_mass_flow(
    thermal_demand: float,
    temperature_supply: float,
    temperature_return: float,
    pandapipes_net: pandapipesNet,
) -> float:
    """Calculate the mass flow rate that is required to meet the thermal demand.

    :param float thermal_demand: The thermal demand of the asset. The thermal demand should be
        supplied in Watts.
    :param float temperature_supply: The temperature that the asset delivers to the "to_junction".
        The temperature should be supplied in Kelvin. The supply temperature is used to calculate
        the specific heat capacity of the fluid.
    :param float temeprature_return: The temperature that the asset receives from the
        "from_junction". The temperature should be supplied in Kelvin.
    :param pandapipesNet net: The pandapipes network used to calculate the specific heat capacity.
    """
    return thermal_demand / (
        (temperature_supply - temperature_return)
        * float(pandapipes_net.fluid.get_heat_capacity(temperature_supply))
    )
