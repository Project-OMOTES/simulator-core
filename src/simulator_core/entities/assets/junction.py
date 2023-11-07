from typing import List

from pandapipes import create_junction, pandapipesNet


class Junction:
    """Wrapper class for pandapipes junctions."""

    def __init__(
        self,
        pn_bar: float = 5.0,
        tfluid_k: float = 300.0,
        height_m: float = 0.0,
        geodata: List = None,
        name: str = None,
        in_service: bool = True,
        index: int = None,
    ):
        """Initialize a Junction object."""
        self.pn_bar = pn_bar
        self.tfluid_k = tfluid_k
        self.height_m = height_m
        self.geodata = geodata
        self.name = name
        self.in_service = in_service
        self.index = index

    def create(self, pandapipes_net: pandapipesNet) -> None:
        """Register the junction in the pandapipes network."""
        self.index = create_junction(
            net=pandapipes_net,
            pn_bar=self.pn_bar,
            tfluid_k=self.tfluid_k,
            height_m=self.height_m,
            geodata=self.geodata,
            name=self.name,
            in_service=self.in_service,
        )
