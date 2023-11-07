from pandapipes import create_flow_control, pandapipesNet


class ControlValve:
    """Wrapper class for pandapipes control valves."""

    def __init__(
        self,
        from_junction: int,
        to_junction: int,
        controlled_mdot_kg_per_s: float,
        diameter_m: float,
        control_active: bool = False,
        in_service: bool = True,
        name: str = None,
        index: int = None,
    ):
        """Initialize a ControlValve object."""
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.controlled_mdot_kg_per_s = controlled_mdot_kg_per_s
        self.diameter_m = diameter_m
        self.control_active = control_active
        self.in_service = in_service
        self.name = name
        self.index = index

    def create(self, pandapipes_net: pandapipesNet) -> None:
        """Register the control valve in the pandapipes network."""
        self.index = create_flow_control(
            net=pandapipes_net,
            from_junction=self.from_junction,
            to_junction=self.to_junction,
            controlled_mdot_kg_per_s=self.controlled_mdot_kg_per_s,
            diameter_m=self.diameter_m,
            control_active=self.control_active,
            in_service=self.in_service,
            name=self.name,
        )
