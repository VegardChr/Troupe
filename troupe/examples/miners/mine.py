"""Mine actor."""

import pygame
from pygame import Color, Surface, Vector2, draw, gfxdraw

from ...actor import Actor
from .gemstone import Gemstone


class Mine(Actor):
    """
    Mine actor.

    A mine where miners can collect gemstones.
    """

    base_image = Surface((32, 32), pygame.SRCALPHA)

    # Mine shape.
    gfxdraw.filled_polygon(
        base_image,
        ((15, 0), (0, 31), (31, 31)),
        Color(255, 255, 255),
    )

    # Mine entrance.
    draw.rect(
        base_image,
        Color(63, 63, 63),
        (16 - 5, 32 - 10, 10, 10),
    )

    def __init__(
        self,
        position: Vector2,
        kind: Gemstone.Kind,
    ) -> None:
        Actor.__init__(self, self.base_image.copy(), position)

        self.kind = kind

        color_image = Surface(self.image.get_size(), pygame.SRCALPHA)
        color_image.fill(Gemstone.color[self.kind])
        self.image.blit(
            color_image,
            (0, 0),
            special_flags=pygame.BLEND_RGB_MULT,
        )
