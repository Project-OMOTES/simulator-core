from simulator_core.entities import SimulationConfiguration
from simulator_core.infrastructure.simulation_manager import SimulationManager
from simulator_core.entities.esdl_object import EsdlObject
from .utils import pyesdl_from_file

from esdl import EnergySystem

import sys
import logging
import traceback

logger = logging.getLogger(__name__)


def run(file_path: str = None):
    from simulator_core.entities import SimulationConfiguration
    import uuid
    config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                     name="test run",
                                     timestep=3600,
                                     duration=3600 * 48)

    esdl_file_path = sys.argv[1] if file_path is None else file_path
    try:
        app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
        result = app.execute()
        return result
    except Exception as error:
        logger.error(f"Error occured: {error} at: {traceback.format_exc(limit=-1)}")
        logger.debug(traceback.format_exc())


if __name__ == "__main__":
    print(run())
