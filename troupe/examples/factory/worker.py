"""Factory worker."""


from uuid import UUID
import pygame
from pygame import Color, Surface, Vector2
from pygame.font import Font

from ...bdi_agent import BDIAgent
from ...environment import Environment
from .assembly import Assembly
from .component import Component
from .storage import Storage


class Worker(BDIAgent):
    """
    Workers traverse the environment looking for components to bring to assembly units,
    such that the assembly units can produce products.
    """

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        observable_distance: float = 64.0,
        interactable_distance: float = 16.0,
        speed: float = 64.0,
    ) -> None:
        """
        Initialize the worker.

        Args:
            image: Image for visualizing the worker.
            position: Initial position.
            observable_distance: Observable distance. Defaults to 64.0.
            interactable_distance: Interactible distance. Defaults to 32.0.
            speed: Speed at which the worker moves. Defaults to 64.0.
        """

        BDIAgent.__init__(
            self,
            image,
            position,
            observable_distance,
            interactable_distance,
            speed,
        )

        # Hands for holding a single component.
        self.hands: Component.Kind | None = None

        # Color for indicating that worker's hands are empty.
        self._empty_hand_color = Color(0, 0, 0, 255)

        # Assembly unit which the worker has been assigned to work at.
        self.assigned_assembly: UUID | None = None  # UUID(int=0)

        # Add desire to produce engines.
        self.intention = self.Desire(
            name="Produce Engines",
            strength=0,
            plan=self.plan_produce_engines,
        )

    @property
    def _held_color(self) -> Color:
        """
        Color associated with the held component.

        Returns:
            The color associated with the component.
        """

        return Component.color[self.hands] if self.hands is not None else self._empty_hand_color

    def deposit_component(self, assembly: Assembly) -> None:
        """
        Deposit a component in an assembly unit.

        Args:
            assembly: The assembly unit to deposit to.
        """

        if self.hands is None:
            return

        assembly.inventory.deposit(self.hands)
        self.hands = None

    def withdraw_component(self, component: Component.Kind, storage: Storage) -> None:
        """
        Withdraw a component from a storage unit.

        Args:
            component: The kind of component to withdraw.
            storage: The storage unit to withdraw from.
        """

        if storage.inventory.withdraw(component):
            self.hands = component

    def plan_assign_assembly(self) -> None:
        """
        Plan for assigning an assembly to work at.
        """

        # Find the closest assembly.
        closest_assembly = self.recollect_closest(Assembly)
        # If no assembly can be found.
        if closest_assembly is None:
            # Explore until an assembly is found.
            self.action_explore(
                lambda: bool(self.look(Assembly)),
                "Explore (Any Assembly)",
            )
            return

        # Assign worker to work at the closest assembly.
        self.assigned_assembly = closest_assembly.uuid

        # Remove desire to assign assembly.
        self.desires.remove(self.intention)

    def action_assign_assembly(self) -> None:
        """
        Make the intention of the worker to find an assembly to work at.
        """

        self.intention = self.Desire(
            "Assign Any Assembly",
            0,
            self.plan_assign_assembly,
        )

    def plan_produce_engines(self) -> None:
        """
        Plan for producing engines.
        """

        # If no assembly has been assigned.
        if self.assigned_assembly is None:
            self.action_assign_assembly()
            return

        # If we have been assigned an assembly that we have no knowledge about.
        # (Chairman assigned an assembly to us, which we have never seen before.)
        if (assembly := self.recollect_id(Assembly, self.assigned_assembly)) is None:

            # Explore until the assembly is found.
            assembly_uuid = self.assigned_assembly
            self.action_explore(
                lambda: bool(self.recollect_id(Assembly, assembly_uuid)),
                "Explore (Assigned Assembly)",
            )
            return

        # If worker has a component.
        if self.hands is not None:
            # Deliver component to assigned assembly.
            self.action_interact_with(assembly, self.deposit_component)
            return

        least_stocked = assembly.least_stocked

        # Find storage until that has least stocked component of assembly in stock.
        candidates = self.recollect_where(
            Storage,
            lambda storage: storage.inventory.components[least_stocked] > 0,
        )

        # Return if no storage units have the component in stock.
        if not candidates:
            self.action_explore(
                lambda: bool(
                    self.look_where(
                        Storage,
                        lambda storage: storage.inventory.components[least_stocked] > 0,
                    )
                ),
                f"Explore ({least_stocked.name.title()})",
            )
            return

        # Closest storage unit with the component in stock.
        storage_unit = min(
            candidates,
            key=lambda storage: self.position.distance_to(storage.position),
        )

        # Withdraw component from the storage unit,
        self.action_interact_with(
            storage_unit,
            lambda storage: self.withdraw_component(least_stocked, storage),
        )

    def update(self, environment: Environment, delta: float) -> None:
        BDIAgent.update(self, environment, delta)

        # Ensure worker stays in factory.
        if not environment.bounds.contains(self.bounds):
            self.steer_towards(Vector2(environment.bounds.center))

    def draw(self, font: Font, surface: Surface) -> None:

        image = Surface(Vector2(self.image.get_size()) * 0.5, pygame.SRCALPHA)
        self.image.blit(image, image.fill(self._held_color).center)

        BDIAgent.draw(self, font, surface)
