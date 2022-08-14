"""Miners environment."""

from ...environment import Environment
from .camp import Camp
from .director import Director
from .gemstone import Gemstone
from .mine import Mine
from .miner import Miner


class MinerEnv(Environment):
    """
    Miners environment.
    """

    def __init__(self, size: tuple[int, int] = (1280, 720)) -> None:
        super().__init__(size)

        self.actors.append(
            Director(self.available_spot(Director.base_image.get_size())),
        )

        self.actors.append(
            Mine(self.available_spot(Mine.base_image.get_size()), Gemstone.Kind.RUBY),
        )
        self.actors.append(
            Mine(self.available_spot(Mine.base_image.get_size()), Gemstone.Kind.EMERALD),
        )
        self.actors.append(
            Mine(self.available_spot(Mine.base_image.get_size()), Gemstone.Kind.SAPPHIRE),
        )

        self.actors.append(
            Camp(self.available_spot(Camp.base_image.get_size())),
        )

        for _ in range(10):
            self.actors.append(
                Miner(self.available_spot(Miner.base_image.get_size())),
            )
