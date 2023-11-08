from pandapipes import create_flow_control, pandapipesNet

from simulator_core.entities.assets.junction import Junction


class ControlValve:
    """Wrapper class for pandapipes control valves."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        from_junction: Junction,
        to_junction: Junction,
        controlled_mdot_kg_per_s: float,
        diameter_m: float,
        control_active: bool = False,
        in_service: bool = True,
        name: str = None,
        index: int = None,
    ):
        """Initialize a ControlValve object."""
        self.pandas_net = pandapipes_net
        self.from_junction = from_junction
        self.to_junction = to_junction
        self.controlled_mdot_kg_per_s = controlled_mdot_kg_per_s
        self.diameter_m = diameter_m
        self.control_active = control_active
        self.in_service = in_service
        self.name = name
        self.index = index
        # Initialize the control valve
        self._initialized = False
        self._create()

    def _create(self) -> None:
        """Register the control valve in the pandapipes network."""
        if not self._initialized:
            self._initialized = True
            self.index = create_flow_control(
                net=self.pandapipes_net,
                from_junction=self.from_junction.index,
                to_junction=self.to_junction.index,
                controlled_mdot_kg_per_s=self.controlled_mdot_kg_per_s,
                diameter_m=self.diameter_m,
                control_active=self.control_active,
                in_service=self.in_service,
                name=self.name,
            )
