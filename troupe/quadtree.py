"""Quadtree module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Rect, Surface, draw

if TYPE_CHECKING:
    from pygame import Vector2

    from .actor import Actor


class Quadtree:
    """
    Quadtree for spatial partitioning of actors.
    """

    def __init__(
        self,
        bounds: Rect,
        actors: list[Actor],
        capacity: int = 8,
        max_depth: int = 8,
        curr_depth: int = 0,
    ) -> None:
        """
        Initialize the quadtree.

        Args:
            bounds: Boundaries of the quadtree.
            actors: Actors to partition within the quadtree.
            capacity: Capacity of each partition. Defaults to 8.
            max_depth: Maximum tree depth. Defaults to 8.
            curr_depth: Current depth of the quadtree. Defaults to 0.
        """

        assert capacity > 0, "Quadtree capacity must be greater than zero."

        self.depth = curr_depth
        self.bounds = bounds
        self.actors = [actor for actor in actors if bounds.collidepoint(actor.position)]

        self.partitions = None

        if len(self.actors) < capacity:
            return

        if self.depth >= max_depth:
            return

        new_width = (self.bounds.w / 2, self.bounds.height / 2)

        self.partitions = (
            # Sorth-West
            Quadtree(
                Rect(
                    self.bounds.topleft,
                    new_width,
                ),
                self.actors,
                capacity,
                max_depth,
                curr_depth + 1,
            ),
            # Sorth-East
            Quadtree(
                Rect(
                    (self.bounds.centerx, self.bounds.y),
                    new_width,
                ),
                self.actors,
                capacity,
                max_depth,
                curr_depth + 1,
            ),
            # South-West
            Quadtree(
                Rect(
                    (self.bounds.x, self.bounds.centery),
                    new_width,
                ),
                self.actors,
                capacity,
                max_depth,
                curr_depth + 1,
            ),
            # South-East
            Quadtree(
                Rect(
                    self.bounds.center,
                    new_width,
                ),
                self.actors,
                capacity,
                max_depth,
                curr_depth + 1,
            ),
        )

    def draw(self, surface: Surface) -> None:
        """
        Draw the Quadtree.

        Args:
            surface: Surface to draw the quadtree onto.
        """

        draw.rect(surface, (255, 255, 255), self.bounds, 1)
        if self.partitions is None:
            return

        for partition in self.partitions:
            partition.draw(surface)

    def query(self, area: Rect) -> list[Actor]:
        """
        Query the quadtree for all actors within an area.

        Args:
            area: Area to look for actors within.

        Returns:
            Actors inside the area.
        """

        if self.partitions is None:
            # Return all actors in the partition that are within the area.
            return [actor for actor in self.actors if area.collidepoint(actor.position)]

        result: list[Actor] = []
        for partition in self.partitions:
            # TODO: if partition.bounds.contains() # Add all actors from partition if area completely encloses it?
            if partition.bounds.colliderect(area):
                result += partition.query(area)

        return result

    def query_radius(self, position: Vector2, radius: float) -> list[Actor]:
        """
        Query the quadtree for all actors within the radius of the position.

        Args:
            position: Position to search in radius of.
            radius: Radius to search in.

        Returns:
            Actors within the radius of the position.
        """

        return [
            actor
            for actor in self.query(
                Rect(
                    position.x - radius,
                    position.y - radius,
                    radius * 2 + 1,
                    radius * 2 + 1,
                )
            )
            if position.distance_to(actor.position) <= radius
        ]
