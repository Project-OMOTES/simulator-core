"""Module for profiling of the simulator core."""
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
