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

"""Entry point for running simulator-core library from cmdline."""

import pandas as pd
from simulator_core.entities.simulation_configuration import SimulationConfiguration
from simulator_core.infrastructure.simulation_manager import SimulationManager
from simulator_core.entities.esdl_object import EsdlObject
from simulator_core.infrastructure.utils import pyesdl_from_file
import sys
import logging
import traceback
import uuid

logger = logging.getLogger(__name__)


def run(file_path: str | None = None) -> pd.DataFrame:
    """Main run function for the heatnetwork simulator."""
    config = SimulationConfiguration(simulation_id=uuid.uuid1(),
                                     name="test run",
                                     timestep=3600,
                                     start=0,
                                     stop=3600 * 1)

    esdl_file_path = sys.argv[1] if file_path is None else file_path
    try:
        app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
        result = app.execute()
        return result
    except Exception as error:
        logger.error(f"Error occured: {error} at: {traceback.format_exc(limit=-1)}")
        logger.debug(traceback.format_exc())


if __name__ == "__main__":
    print(run(r'.\testdata\test1.esdl'))
