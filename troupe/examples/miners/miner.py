"""Miner agent."""

import pygame
from pygame import Surface, Vector2
from pygame.font import Font

from ...bdi_agent import BDIAgent
from ...environment import Environment
from .camp import Camp
from .gemstone import Gemstone
from .mine import Mine


class Miner(BDIAgent):
    """
    Miner agent.

    Miners search the map for gemstones
    and deliver the gemstones to camps.
    """

    base_image = Surface((16, 16), pygame.SRCALPHA)
    base_image.fill((191, 191, 191))

    def __init__(
        self,
        position: Vector2,
        observable_distance: float = 96,
        speed: float = 64,
    ) -> None:
        BDIAgent.__init__(self, self.base_image, position, observable_distance, 16, speed)

        self.intention = self.Desire(
            "Work",
            0,
            self.plan_work,
        )

        self.assigned_mine: Mine | None = None
        self.hands: Gemstone.Kind | None = None

    def collect_gemstone(self, mine: Mine) -> None:
        """
        Collect a gemstone from a mine.

        Args:
            mine: Mine to collect gemstone from.
        """

        self.hands = mine.kind

    def deposit_gemstone(self, camp: Camp) -> None:
        """
        Deposit held gemstone at the camp.

        Args:
            camp: Camp to deliver gemstone to.
        """

        # Return if there is nothing to deliver.
        if self.hands is None:
            return

        # Deliver gemstone.
        camp.gemstones[self.hands] += 1
        self.hands = None

    def plan_work(self) -> None:
        """
        Plan for working.

        Work consists of gathering gemstones
        and delivering them to a camp.
        """

        # If the miner has a gemstone.
        if self.hands is not None:
            # Deliver held gemstone to a camp.
            self.action_interact_closest(Camp, self.deposit_gemstone)
            return

        # If no mine has been assigned.
        if self.assigned_mine is None:
            # Collect gemstone from closest mine we know about.
            self.action_interact_closest(Mine, self.collect_gemstone)
            return

        # If we have been assigned a mine that we have no knowledge about.
        if self.recollect_id(Mine, self.assigned_mine.uuid) is None:
            # Look for the mine.
            mine_uuid = self.assigned_mine.uuid
            self.action_explore(
                lambda: (self.recollect_id(Mine, mine_uuid) is not None),
                "Find Assigned Mine",
            )
            return

        # Collect gemstone from our assigned mine.
        self.action_interact_with(self.assigned_mine, self.collect_gemstone)

    def update(self, environment: Environment, delta: float) -> None:
        BDIAgent.update(self, environment, delta)
        self.wraparound(environment)

    def draw(self, font: Font, surface: Surface) -> None:

        image = Surface(Vector2(self.image.get_size()) * 0.5, pygame.SRCALPHA)
        self.image.blit(
            image,
            image.fill(
                Gemstone.color[self.hands] if self.hands is not None else (0, 0, 0),
            ).center,
        )

        BDIAgent.draw(self, font, surface)
