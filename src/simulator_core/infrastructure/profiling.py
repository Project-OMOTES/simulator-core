"""Module for profiling of the simulator core."""

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

import cProfile
from simulator_core.infrastructure.app import run
import argparse


parser = argparse.ArgumentParser(description="sample argument parser")
parser.add_argument("esdl_file")
parser.add_argument("profiling_output_file")
args = parser.parse_args()


def profiler_main() -> None:
    """Main function to be called from the profiler."""
    run(args.esdl_file)


cProfile.run("profiler_main()", args.profiling_output_file)
