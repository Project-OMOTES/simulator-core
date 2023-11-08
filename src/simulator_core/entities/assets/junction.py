from typing import Any, List

from pandapipes import create_junction, pandapipesNet


class Junction:
    """Wrapper class for pandapipes junctions."""

    def __init__(
        self,
        pandapipes_net: pandapipesNet,
        pn_bar: float = 5.0,
        tfluid_k: float = 300.0,
        height_m: float = 0.0,
        geodata: List[Any] = [None, None],
        name: str = "None",
        in_service: bool = True,
        index: int = None,
    ):
        """Initialize a Junction object."""
        self.pandapipes_net = pandapipes_net
        self.pn_bar = pn_bar
        self.tfluid_k = tfluid_k
        self.height_m = height_m
        self.geodata = geodata
        self.name = name
        self.in_service = in_service
        self.index = index
        # Initialize the junction
        self._initialized = False
        self._create()

    def _create(self) -> None:
        """Register the junction in the pandapipes network."""
        if not self._initialized:
            self._initialized = True
            self.index = create_junction(
                net=self.pandapipes_net,
                pn_bar=self.pn_bar,
                tfluid_k=self.tfluid_k,
                height_m=self.height_m,
                geodata=self.geodata,
                name=self.name,
                in_service=self.in_service,
            )
