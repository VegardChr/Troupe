# Introduction
Troupe is a framework for creating multi-agent simulations in Python. \
Please see the examples for an introduction to using the framework.

# Installation
Please note that troupe requires Python 3.10 or newer! \
To install the framework, please:
1. Create a new directory for your project.
2. Download and extract troupe as `troupe`.
3. (optional) Create a [virutal environment](https://docs.python.org/3/library/venv.html).
4. Install the package using `pip install troupe`

# Documentation
Please see [docs](./docs/README.md) for steps to build documentation.

# Examples
Troupe includes several example environments:
- [Boids](./troupe/examples/boids/)
- [Miners](./troupe/examples/miners/)
- [Predator-Prey](./troupe/examples/predators/)
- [Factory](./troupe/examples/factory/)

Example environments can be run progrematically, \
or via the command-line interface:

```py
from troupe import Simulation
from troupe.examples.boids import BoidEnv

Simulation.run(BoidEnv())
```

```
python -m troupe -e boids
```
