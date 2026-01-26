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

import logging
import sys
import traceback
import uuid
from datetime import datetime

import pandas as pd

from omotes_simulator_core.entities.esdl_object import EsdlObject
from omotes_simulator_core.entities.simulation_configuration import SimulationConfiguration
from omotes_simulator_core.infrastructure.simulation_manager import SimulationManager
from omotes_simulator_core.infrastructure.utils import pyesdl_from_file

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def progressLogger(progress: float, message: str) -> None:
    """Function to report progress to logging/stdout."""
    logger.info(f"{message} ({progress * 100:.2f}%)")


def run(file_path: str | None = None) -> pd.DataFrame:
    """Main run function for the heatnetwork simulator."""
    config = SimulationConfiguration(
        simulation_id=uuid.uuid1(),
        name="test run",
        timestep=3600,
        start=datetime.strptime("2019-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        stop=datetime.strptime("2019-01-08T01:00:00", "%Y-%m-%dT%H:%M:%S"),
    )

    esdl_file_path = sys.argv[1] if file_path is None else file_path
    try:
        app = SimulationManager(EsdlObject(pyesdl_from_file(esdl_file_path)), config)
        result = app.execute(progressLogger)
        return result
    except Exception as error:
        logger.error(f"Error occured: {error} at: {traceback.format_exc(limit=-1)}")
        logger.debug(traceback.format_exc())
        raise error


if __name__ == "__main__":
    # Set loglevel to logging.DEBUG for more verbose output
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s]:%(name)s - %(message)s"
    )
    t1 = datetime.now()
    #result = run(r".\testdata\test1.esdl")
    result = run(r".\testdata\test1_prod_profile.esdl")
    t2 = datetime.now()

    logger.info(f"Results dataframe shape=({result.shape})")
    logger.info(f"Execution time: {t2 - t1}")
    logger.debug(result.head())
    producer_id = "cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4"

    # Producer in and out ports: "9c258b9d-3149-4720-8931-f4bef1080ec1", "2d818e3d-8a39-4cec-afa0-f6dbbfd50696", carrier in: "0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret", carrier out: "0bd9cb08-2f69-4e97-8ac8-bd87b07e466a".
    prod_massfl_in = result["9c258b9d-3149-4720-8931-f4bef1080ec1", "mass_flow"].values
    prod_massfl_out = result["2d818e3d-8a39-4cec-afa0-f6dbbfd50696", "mass_flow"].values
    prod_temp_in = result["9c258b9d-3149-4720-8931-f4bef1080ec1", "temperature"].values
    prod_temp_out = result["2d818e3d-8a39-4cec-afa0-f6dbbfd50696", "temperature"].values
    # Consumer in and out ports: "af0904f7-ba1f-4e79-9040-71e08041601b", "e890f65f-80e7-46fa-8c52-5385324bf686", carrier in: "0bd9cb08-2f69-4e97-8ac8-bd87b07e466a", carrier out: "0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret".
    cons_massfl_in = result["af0904f7-ba1f-4e79-9040-71e08041601b", "mass_flow"].values
    cons_massfl_out = result["e890f65f-80e7-46fa-8c52-5385324bf686", "mass_flow"].values
    cons_temp_in = result["af0904f7-ba1f-4e79-9040-71e08041601b", "temperature"].values
    cons_temp_out = result["e890f65f-80e7-46fa-8c52-5385324bf686", "temperature"].values
    
    prod_power = 4180 * prod_massfl_in * (prod_temp_out - prod_temp_in)
    cons_power = 4180 * cons_massfl_in * (cons_temp_in - cons_temp_out)

    plt.figure()
    plt.plot(prod_power)
    plt.show()