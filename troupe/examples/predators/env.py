"""Predator-Prey environment."""

from random import uniform

from pygame import Vector2

from ...environment import Environment
from .grass import Grass
from .predator import Predator
from .prey import Prey


class PredatorEnv(Environment):
    """
    Predator-Prey environment.
    """

    def __init__(self, size: tuple[int, int] = (1280, 720)) -> None:
        Environment.__init__(self, size)

        # Maximum number of grass actors allowed in the environment.
        self.max_grass = 64
        # How often grass should spawn.
        self.grass_interval = 0.20
        # Time until we should spawn next grass actor.
        self.grass_timer = self.grass_interval

        # Add preys to environment.
        for _ in range(32):
            position = self.available_spot(Prey.base_image.get_size())
            prey = Prey(position)
            self.actors.append(prey)

        # Add predators to environment
        for _ in range(16):
            position = self.available_spot(Predator.base_image.get_size())
            self.actors.append(Predator(position))

    def plant_grass(self) -> None:
        """
        Plant grass at a random spot in the environment.
        Only plants grass as long as grass actros in the environment do not exceed max_grass.
        """

        # Only plant more grass if grass limit (max_grass) has not been reached.
        if len([actor for actor in self.actors if isinstance(actor, Grass)]) > self.max_grass:
            return

        # Append new grass actor to the environment.
        self.actors.append(
            Grass(
                Vector2(
                    uniform(self.bounds.x, self.bounds.w),
                    uniform(self.bounds.y, self.bounds.h),
                )
            )
        )

    def update(self, delta: float) -> None:
        Environment.update(self, delta)

        self.grass_timer -= delta
        if self.grass_timer < 0:
            self.grass_timer = self.grass_interval
            self.plant_grass()
