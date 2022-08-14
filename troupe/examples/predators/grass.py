"""Grass actor."""

from pygame import Color, Rect, Surface, Vector2, draw

from ...actor import Actor
from ...environment import Environment
from .consumable import Consumable


class Grass(Actor, Consumable):
    """Grass actor."""

    layer = 1

    # Base image, common for all grass.
    base_image = Surface((16, 16))
    draw.rect(base_image, Color(64, 255, 64), Rect(0, 0, 16, 16))

    def __init__(self, position: Vector2) -> None:
        """
        Initialize the actor.

        Args:
            position: Position of grass.
        """

        Actor.__init__(self, self.base_image, position, Vector2(0, -1), 0)
        Consumable.__init__(self, 20)

    def update(self, environment: Environment, delta: float) -> None:
        Actor.update(self, environment, delta)

        # Remove grass from environment, if it has been eaten.
        if self.consumed:
            environment.actors.remove(self)
