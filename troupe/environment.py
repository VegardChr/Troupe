"""Environment module."""

from random import randint
from typing import TYPE_CHECKING

from pygame import Rect, Surface, Vector2
from pygame.font import Font

from .quadtree import Quadtree

if TYPE_CHECKING:
    from .actor import Actor


class Environment:
    """Environment which all actors exist within."""

    def __init__(self, size: tuple[int, int]) -> None:
        """
        Initialize the environment.

        Args:
            bounds: Environment boundaries.
        """

        # Font for displaying debug information.
        self.font = Font(None, 15)

        # Environment boundaries.
        self.bounds = Rect((0, 0), size)

        # Actors of the environment.
        self.actors: list["Actor"] = []

        # Initial quadtree.
        self.quadtree_capacity = 8
        self.quadtree_maxdepth = 4
        self.quadtree = Quadtree(
            self.bounds,
            self.actors,
            self.quadtree_capacity,
            self.quadtree_maxdepth,
        )

        print("Initialized environment!")

    def update(self, delta: float) -> None:
        """
        Update all actors in the environment.

        Args:
            delta: Time since last update.
        """

        # Create a new quadtree.
        self.quadtree = Quadtree(
            self.bounds,
            self.actors,
            self.quadtree_capacity,
            self.quadtree_maxdepth,
        )

        # Update actors layer by layer.
        self.actors.sort(key=lambda actor: actor.layer)
        for actor in self.actors:
            actor.update(self, delta)

    def draw(self, surface: Surface) -> None:
        """
        Draw all actors in the environment

        Args:
            surface: The surface to draw the actors on.
        """

        # Visualize quadtree.
        # self.quadtree.draw(surface)

        # Draw actors layer by layer.
        self.actors.sort(key=lambda actor: actor.layer)
        for actor in self.actors:
            actor.draw(self.font, surface)

    def available_spot(self, size: tuple[int, int]) -> Vector2:
        """
        Find an avaliable position where the actor can be positioned,
        without overlapping with another actor.

        Args:
            size: The size of the actor to find an avaiable spot for.

        Raises:
            RuntimeError: Raised if no avaliable spot was found.

        Returns:
            Position (center) where the actor can be positioned.
        """

        # Randomly place a rect and see if it collides with another rect.
        # Try again if collision occurs.
        # Give up if number of attempts exceed 128.
        rect = Rect((0, 0), size)

        for _ in range(128):
            rect.x = randint(self.bounds.x, self.bounds.w - rect.right)
            rect.y = randint(self.bounds.y, self.bounds.h - rect.bottom)

            if not self.bounds.contains(rect):
                break

            rects = [actor.bounds for actor in self.actors]
            if rect.collidelist(rects) == -1:
                break
        else:
            # No avaliable spot was found.
            raise RuntimeError("No avaliable spot was found!")

        # An avaliable spot was found.
        return Vector2(rect.center)
