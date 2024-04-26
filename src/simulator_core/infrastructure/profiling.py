import cProfile
from src.simulator_core.infrastructure.app import run_simulator
import argparse

parser=argparse.ArgumentParser(description="sample argument parser")
parser.add_argument("esdl_file")
parser.add_argument("profiling_output_file")
args = parser.parse_args()


def main():
    run_simulator(args.esdl_file)

cProfile.run("main()", args.profiling_output_file)
