"""Boid agent."""

from __future__ import annotations

from random import uniform

from pygame import Surface, Vector2

from ...agent import Agent
from ...environment import Environment


class Boid(Agent):
    """Boid"""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        speed: float = 0,
        observable_distance: float = 0,
    ) -> None:
        Agent.__init__(
            self,
            image,
            position,
            observable_distance,
            speed=speed,
            direction=Vector2(uniform(-1, 1), uniform(-1, 1)),
        )

        self._position = Vector2(0, 0)

    def update(self, environment: Environment, delta: float) -> None:
        Agent.update(self, environment, delta)
        boids = self.look(Boid)

        self.flocking(boids)
        self.wraparound(environment)

    def flocking(self, boids: list[Boid]) -> None:
        """
        Boid flocking behaviour,
        changes direction of boid such that:

        - (Cohesion) Boids stay together.
        - (Seperation) Boids not collide.
        - (Alignment) Boids move in the same direction.

        Args:
            boids: Boids that have been observed.
        """

        if not boids:
            return

        # Seperation direction only caluclated using boids within this distance.
        seperation_distance = self.observable_distance / 2

        # Initialize direction vectors.
        separation_direction = Vector2(0, 0)
        cohesion_direction = Vector2(0, 0)
        alignment_direction = Vector2(0, 0)

        for boid in boids:
            if self.position.distance_to(boid.position) <= seperation_distance:
                separation_direction -= boid.position - self.position
            cohesion_direction += boid.position - self.position
            alignment_direction += boid.direction

        # Normalize vectors.
        if separation_direction.magnitude() > 0:
            separation_direction.normalize_ip()
        cohesion_direction.normalize_ip()
        alignment_direction.normalize_ip()

        # Apply rules (Seperation, Cohesion, Alignment)
        self.direction = self.direction.lerp(separation_direction, 0.08)
        self.direction = self.direction.lerp(cohesion_direction, 0.03)
        self.direction = self.direction.lerp(alignment_direction, 0.02)
