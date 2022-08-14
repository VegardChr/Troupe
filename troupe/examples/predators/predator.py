"""Predator agent."""

import pygame
from pygame import Color, Surface, Vector2, gfxdraw

from ...actor import Actor
from .prey import Prey


class Predator(Prey):
    """
    Predator is a BDI Agent that hunts prey for food,
    with the ultimate goal of producing offspring.
    """

    layer = 4

    # Base image, common for all predators.
    base_image = Surface((16, 16), pygame.SRCALPHA)
    gfxdraw.filled_polygon(
        base_image,
        [(8, 0), (15, 6), (15, 15), (8, 11), (7, 11), (0, 15), (0, 6), (7, 0)],
        Color(220, 32, 64),
    )

    consumes = Prey

    def __init__(
        self,
        position: Vector2,
        observable_distance: float = 64,
        speed: float = 38,
    ) -> None:

        Prey.__init__(
            self,
            position,
            observable_distance,
            speed,
        )

    def create_child(self) -> Actor:
        return Predator(Vector2(self.position))
