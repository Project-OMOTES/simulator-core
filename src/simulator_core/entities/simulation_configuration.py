from dataclasses import dataclass
import uuid


@dataclass
class SimulationConfiguration:
    simulation_id: uuid.UUID
    name: str
    timestep: float
    start: float
    stop: float
