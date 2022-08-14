"""Boids environment."""

import pygame
from pygame import Color, Surface, gfxdraw

from ...environment import Environment
from .boid import Boid


class BoidEnv(Environment):
    """
    Boids environment.
    """

    def __init__(self, size: tuple[int, int] = (1280, 720)) -> None:
        super().__init__(size)

        # Create boid image.
        boid_image = Surface((16, 16), pygame.SRCALPHA)
        gfxdraw.filled_polygon(
            boid_image,
            [(8, 0), (15, 6), (15, 15), (8, 11), (7, 11), (0, 15), (0, 6), (7, 0)],
            Color(220, 220, 200),
        )

        # Add boids to environment.
        for _ in range(128):
            position = self.available_spot(boid_image.get_size())
            self.actors.append(
                Boid(
                    image=boid_image,
                    position=position,
                    observable_distance=64,
                    speed=32,
                )
            )
