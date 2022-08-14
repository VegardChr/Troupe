"""Director agent."""

import pygame
from pygame import Surface, Vector2, gfxdraw

from ...agent import Agent
from ...environment import Environment
from .camp import Camp
from .gemstone import Gemstone
from .mine import Mine
from .miner import Miner


class Director(Agent):
    """
    Director agent.

    Gives orders to workers in a bid to improve efficiency.
    """

    base_image = Surface((32, 32), pygame.SRCALPHA)
    gfxdraw.filled_polygon(base_image, [(0, 32), (32, 32), (16, 16)], (255, 0, 0))
    gfxdraw.filled_circle(base_image, 16, 16, 10, (240, 220, 160))

    def __init__(
        self,
        position: Vector2,
        observable_distance: float = 5000,
        speed: float = 0,
    ) -> None:
        Agent.__init__(self, self.base_image, position, observable_distance, speed)

    def assign_workers(self) -> None:
        """
        Assign workers to the mine which the director believes will maximize profit.

        Args:
            environment: Environment the director is part of.
        """

        if not (camps := self.observations.find(Camp)):
            return
        if not (mines := self.observations.find(Mine)):
            return
        if not (miners := self.observations.find(Miner)):
            return

        # Determine which mine miners should collect from to maximize profit/"value".
        mine = min(
            mines,
            key=lambda mine: mine.position.distance_to(
                min(camps, key=lambda camp: camp.position.distance_to(mine.position)).position
            )
            / Gemstone.value[mine.kind],
        )

        # Assign all miners to the mine.
        for miner in miners:
            miner.assigned_mine = mine

    def update(self, environment: Environment, delta: float) -> None:
        Agent.update(self, environment, delta)

        # Strategically assign workers to mines.
        self.assign_workers()
