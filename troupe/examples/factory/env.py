"""Factory environment."""

import itertools

import pygame
from pygame import Color, Surface

from ...environment import Environment
from .assembly import Assembly
from .chairman import Chairman
from .component import Component
from .storage import Storage
from .worker import Worker


class FactoryEnv(Environment):
    """Factory environment."""

    def __init__(self, size: tuple[int, int] = (1280, 720)) -> None:
        """
        Initialize the factory environment.

        Args:
            size: Boundaries of the environment. Defaults to (1280, 720).
        """

        Environment.__init__(self, size)

        # Add two storage units for each component type.
        for component, _ in itertools.product(Component.Kind, range(6)):  # range(6)
            image = Surface((25, 25), pygame.SRCALPHA)
            image.fill(Component.color[component])
            position = self.available_spot(image.get_size())
            self.actors.append(
                Storage(
                    image=image,
                    position=position,
                    component=component,
                    shipment_size=5,
                    shipment_interval=15.0,
                )
            )

        # Add assemblies.
        for _ in range(4):  # range(4)
            image = Surface((40, 40), pygame.SRCALPHA)
            image.fill(Color(180, 180, 180))
            position = self.available_spot(image.get_size())
            self.actors.append(
                Assembly(
                    image=image,
                    position=position,
                    cooldown_time=2.0,
                )
            )

        # Add workers.
        for _ in range(16):  # range(32)
            image = Surface((15, 15), pygame.SRCALPHA)
            image.fill(Color(200, 80, 80))
            position = self.available_spot(image.get_size())
            self.actors.append(
                Worker(
                    image=image,
                    position=position,
                )
            )

        # Add a chairman.
        image = Surface((30, 30), pygame.SRCALPHA)
        image.fill(Color(255, 128, 64))
        position = self.available_spot(image.get_size())
        self.actors.append(
            Chairman(
                image=image,
                position=position,
                observable_distance=2048,
                interactable_distance=2048,
                reassignment_interval=2.0,
                reassignment_policy=Chairman.ReassignmentPolicy.MOST_IDLE,
            )
        )
