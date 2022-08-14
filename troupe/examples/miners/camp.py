"""Camp actor."""

import pygame
from pygame import Color, Surface, Vector2, gfxdraw

from ...actor import Actor
from .gemstone import Gemstone


# Camp/Market
class Camp(Actor):
    """
    Camp actor.

    A camp where miners can deposit their gemstones.
    """

    base_image = Surface((32, 32), pygame.SRCALPHA)

    # Mine shape.
    gfxdraw.filled_polygon(
        base_image,
        ((16, 0), (0, 32), (32, 32)),
        Color(191, 191, 0),
    )

    def __init__(self, position: Vector2) -> None:
        Actor.__init__(self, self.base_image, position)

        self.gemstones: dict[Gemstone.Kind, int] = {
            Gemstone.Kind.RUBY: 0,
            Gemstone.Kind.EMERALD: 0,
            Gemstone.Kind.SAPPHIRE: 0,
        }
