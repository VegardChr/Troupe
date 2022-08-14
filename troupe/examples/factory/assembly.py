"""Assembly unit."""

import pygame
from pygame import Color, Surface, Vector2
from pygame.font import Font

from ...actor import Actor
from ...environment import Environment
from .component import Component
from .inventory import Inventory


class Assembly(Actor):
    """Assembly unit."""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        cooldown_time: float = 4.0,
    ) -> None:
        """
        Initialize assembly unit.

        Args:
            image: Image used to visualize the assembly.
            position: Position of the assembly unit.
            cooldown_time: Time to wait after producing a component. Defaults to 0.0.
        """

        Actor.__init__(self, image, position)

        # Color indicating that assembly is busy.
        self._busy_color = Color(127, 15, 15)
        # Color indicating that assembly is idle.
        self._idle_color = Color(15, 127, 15)

        # Total time spent idle.
        self.total_idle_time: float = 0.0

        # Time the assembly must wait after producing a component.
        self.cooldown_time: float = cooldown_time
        # Time until the assembly is ready to produce another component.
        self.cooldown_timer: float = 0.0

        # Total components produced by this assembly.
        self.produced_count: int = 0

        # Inventory that can hold components.
        self.inventory = Inventory()

    @property
    def is_ready(self) -> bool:
        """
        Is the assembly is ready to produce another product?

        Returns:
            True if the assembly is ready.
        """

        return self.cooldown_timer <= 0

    @property
    def least_stocked(self) -> Component.Kind:
        """
        The least stocked component in the assembly.

        Returns:
            The least stocked kind of component.
        """

        return min(
            self.inventory.components,
            key=lambda component: self.inventory.components[component],
        )

    def _assemble(self) -> bool:
        """
        Use stocked components to assemble a new product.

        Returns:
            True if a new product was assembled.
        """

        # Return false if assembly is not ready (Cooldown).
        if not self.is_ready:
            return False

        # Return false if assembly unit does not have at least one of all components.
        if 0 in self.inventory.components.values():
            return False

        # Withdraw one of each component to produce the product.
        for component in self.inventory.components:
            self.inventory.withdraw(component)
        self.produced_count += 1

        # Reset cooldown.
        self.cooldown_timer = self.cooldown_time

        self.log(f"{str(self)} produced a new component. Total: {self.produced_count}")

        return True

    def missing(self) -> list[Component.Kind]:
        """
        Components that are missing in order to product a new component.

        Returns:
            List of missing components.
        """

        return [component for component, count in self.inventory.components.items() if count == 0]

    def update(self, environment: Environment, delta: float) -> None:
        Actor.update(self, environment, delta)

        # Update idle time.
        if self.is_ready:
            self.total_idle_time += delta

        self._assemble()

        # Update cooldown timer.
        self.cooldown_timer -= delta

    def draw(self, font: Font, surface: Surface) -> None:
        image = Surface(Vector2(self.image.get_size()) * 0.5, pygame.SRCALPHA)

        self.image.blit(
            image,
            image.fill(
                self._idle_color if self.is_ready else self._busy_color,
            ).center,
        )

        Actor.draw(self, font, surface)
