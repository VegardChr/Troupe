"""
Actor module.
"""

from __future__ import annotations

from copy import deepcopy
from random import uniform
from typing import TYPE_CHECKING, TypeVar
from uuid import uuid4

from pygame import Vector2, transform
from pygame.font import Font

if TYPE_CHECKING:
    from pygame import Rect, Surface

    from .environment import Environment

ActorT = TypeVar("ActorT", bound="Actor")


class Actor:
    """
    An actor is an entity that exists within an environment.

    Actors exist largely for agents to interact with, they are not capable of interacting with other actors,
    outside of blindly bumping into them as a result of traversing the environment.
    """

    # Layer to draw the actor on.
    layer = 0

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        direction: Vector2 = Vector2(0, -1),
        speed: float = 0.0,
    ) -> None:
        """
        Initialize the actor.

        Args:
            image: Image used to visualize actor.
            position: Initial position.
            direction: Initial direction. Defaults to Vector2(0, 1).
            speed: Speed of the actor. Defaults to 0.0.
        """

        # Random steering.
        self._random_steer_time = 0.0
        self._random_steer_interval = 0.1

        # Sprite image.
        self.image: Surface = image

        # Position of the actor.
        self.position = position
        # Speed to move at.
        self.speed = speed
        # Directional vector.
        self.direction = direction

        # ID for uniquely indentifying the actor.
        self.uuid = uuid4()

        # True if actor is a belief held my an agent.
        self.is_belief = False

    @property
    def rotation(self) -> float:
        """
        Rotation of the actor.

        .. table::

            +------------+----------+
            | Direction  | Degrees  |
            +============+==========+
            | (1,  0)    | 0        |
            +------------+----------+
            | (0,  1)    | 90       |
            +------------+----------+
            | (-1, 0)    | 180      |
            +------------+----------+
            | (0, -1)    | -90      |
            +------------+----------+

        Returns:
            Actor rotation in degrees.
        """

        return self.direction.as_polar()[1]

    @property
    def bounds(self) -> Rect:
        """
        Get the bounds of the actor.

        Returns:
            Rectangle centered at the position of the actor.
        """

        return self.image.get_rect(center=self.position)

    def steer_random(self) -> None:
        """Steer the acotr in a random direction."""

        if self._random_steer_time > self._random_steer_interval:
            self._random_steer_time = 0
            self.direction = self.direction.lerp(
                Vector2(uniform(-1, 1), uniform(-1, 1)), 0.3
            ).normalize()

    def steer_towards(self, destination: Vector2) -> None:
        """
        Steer the actor such that it faces the destination.

        Args:
            destination: The destination to face towards
        """

        self.direction = (destination - self.position).normalize()

    def within_distance(self, location: Vector2, distance: int | float) -> bool:
        """
        Determine if the actor is within the specified distance of a location.

        Args:
            location: The location to determine if the actor is near.
            distance: Distance we want to determine if the actor is within.

        Returns:
            Whether or not the actor is within the distance.
        """

        return self.position.distance_to(location) <= distance

    def wraparound(self, environment: Environment) -> None:
        """
        Ensure that actors stay in bounds.
        When an actor disappears from one side of the map,
        it appears on the opposite side.

        Args:
            environment: Environment the actor is part of.
        """

        if self.position.x < environment.bounds.left:
            self.position.update(self.position.x + environment.bounds.width, self.position.y)
        elif self.position.x > environment.bounds.width:
            self.position.update(self.position.x - environment.bounds.width, self.position.y)

        if self.position.y < environment.bounds.top:
            self.position.update(self.position.x, self.position.y + environment.bounds.height)
        elif self.position.y > environment.bounds.bottom:
            self.position.update(self.position.x, self.position.y - environment.bounds.height)

    def update_position(self, delta: float) -> None:
        """
        Update the position of the actor.

        Args:
            delta: Time since last update.
        """

        if self.direction == Vector2(0, 0):
            return

        self.direction.normalize_ip()
        self.position += self.direction * self.speed * delta

    def update_random_steer(self, delta: float) -> None:
        """
        Update the random steer timer.

        Args:
            delta: Time since last update.
        """

        self._random_steer_time += delta

    def update(self, environment: Environment, delta: float) -> None:
        """
        Update the actor.

        Args:
            environment: Environment the actor is part of.
            delta: Time since last update.
        """

        self.update_random_steer(delta)
        self.update_position(delta)
        # self.wraparound(environment)

    def draw(self, font: Font, surface: Surface) -> None:
        """
        Draw the actor onto the surface.

        Args:
            surface: The surface to draw the actor onto.
        """

        # Rotate image.
        rotated_image = transform.rotate(self.image, -self.rotation - 90)

        # Draw image on surface.
        surface.blit(rotated_image, rotated_image.get_rect(center=self.position))

    def log(self, message: str) -> None:
        """
        Log a message related to this actor in console.

        Args:
            message: Message to display in the console.
        """

        print(f"[{str(self).upper()}] {message}")

    def copy(self: ActorT) -> ActorT:
        """
        Create a copy of the actor.
        Returns:
            Actor copy.
        """

        actor_copy = self.__class__.__new__(self.__class__)
        for key, value in self.__dict__.items():
            if not hasattr(value, "copy"):
                setattr(actor_copy, key, deepcopy(value))
                continue
            if callable(clone := getattr(value, "copy")):
                setattr(actor_copy, key, clone())

        return actor_copy

    def __str__(self) -> str:
        actor_type = self.__class__.__name__
        return f"{actor_type.title()}-{str(self.uuid)[:4]}"

    def __eq__(self, __o: object) -> bool:
        return self.uuid == __o.uuid if isinstance(__o, Actor) else False

    def __hash__(self) -> int:
        return self.uuid.__hash__()
