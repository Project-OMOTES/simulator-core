# OMOTES-simulator-core

This repository is part of the 'Nieuwe Warmte Nu Design Toolkit' project. Omotes-simulator-core is the core library for the thermo-hydraulic numerical simulations within the NWN Design toolkit. The simulator requires a network schematization in ESDL format, simulation start/end time and a timestep-duration as input. The simulator will return a pandas dataframe that contains the all the output time series.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install omotes-simulator-core.

```bash
pip install omotes-simulator-core
```

## Usage

```python
from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file

# Create a callable that prints the progress messages
def progressLogger(progress: float, message: str) -> None:
    """Function to report progress to logging/stdout."""
    logger.info(f"({progress*100:.2f}%) {message}")

#  Create simulation config parameters
config = SimulationConfiguration(
        simulation_id=uuid.uuid1(),  #creates a new uuid for this simulation
        name="test run",             # user defined name
        timestep=3600,               # timestep, start and stop datetime (simulation period)
        start=datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        stop=datetime.strptime("2019-01-01T01:00:00", "%Y-%m-%dT%H:%M:%S"),
    )
esdl_file_path = "path/to/whatever/file.esdl"

# Run the simulation
sim = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
result = sim.execute(progressLogger)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

For more information, please see [CONTRIBUTING.md]

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/), see [LICENSE]
