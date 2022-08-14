"""Storage unit."""


from pygame import Color, Surface, Vector2
from pygame.font import Font

from ...actor import Actor
from ...environment import Environment
from .component import Component
from .inventory import Inventory


class Storage(Actor):
    """Storage unit."""

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        component: Component.Kind,
        shipment_size: int,
        shipment_interval: float,
    ) -> None:
        """
        Initialize storage unit.

        Args:
            image: Image used to visualize the storage unit.
            position: Position of the storage unit.
            component: Component to recieve shipments of.
            shipment_size: Number of components in each shipment.
            shipment_interval: Time between shipments.
        """

        Actor.__init__(self, image, position, direction=Vector2(0, -1))

        # Inventory that can hold components.
        self.inventory = Inventory()
        # Components that are shipped to this storage unit.
        self.shipment_type = component
        # Time until the next shipment arrives.
        self.shipment_time = 0.0
        # Time between shipments.
        self.shipment_interval = shipment_interval
        # Size of shipments.
        self.shipment_size = shipment_size

    @property
    def _component_color(self) -> Color:
        """
        Color associated with the component that the storage unit recieves shipments of.

        Returns:
            The color asssociated with the component.
        """

        return Component.color[self.shipment_type]

    def shipment(self, delta: float) -> None:
        """
        Process shipment.

        Args:
            delta: Time since last tick.
        """

        # Recieve a shipment of components every "shipment_interval" seconds.
        self.shipment_time -= delta
        if self.shipment_time < 0:
            self.inventory.components[self.shipment_type] += self.shipment_size
            self.shipment_time = self.shipment_interval

    def update(self, environment: Environment, delta: float) -> None:

        Actor.update(self, environment, delta)
        self.shipment(delta)

    def draw(self, font: Font, surface: Surface) -> None:

        self.image.fill(self._component_color)
        component_count = self.inventory.components[self.shipment_type]

        text = str(component_count) if component_count <= 99 else "99+"
        self.image.blit(
            font.render(text, True, (0, 0, 0, 0)),
            (0, 0),
        )

        Actor.draw(self, font, surface)
