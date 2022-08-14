"""Command-line interface for interacting with the Troupe framework."""

from argparse import ArgumentParser
from random import seed

from .examples.boids import BoidEnv
from .examples.factory import FactoryEnv
from .examples.miners import MinerEnv
from .examples.predators import PredatorEnv
from .simulation import Simulation

examples = {
    "boids": BoidEnv,
    "miners": MinerEnv,
    "predators": PredatorEnv,
    "factory": FactoryEnv,
}

parser = ArgumentParser(prog="troupe")
parser.add_argument(
    "-e",
    "--example",
    help="Run an example envrionment",
    choices=examples.keys(),
    required=True,
)

args = parser.parse_args()
name: str = getattr(args, "example")

seed(0)
Simulation.run(examples[name]())
