"""Inventory."""

from .component import Component


class Inventory:
    """
    An inventory that can hold components.
    """

    def __init__(self) -> None:
        """
        Initialize inventory.
        """

        self.components: dict[Component.Kind, int] = {item: 0 for item in Component.Kind}

    def deposit(self, component: Component.Kind) -> bool:
        """
        Deposit a component.

        Args:
            component: The kind of component to be deposited.
        Returns:
            True if there was space to deposit the component.
        """

        if component not in self.components:
            return False

        self.components[component] += 1

        return True

    def withdraw(self, component: Component.Kind) -> bool:
        """
        Withdraw a component from inventory.

        Args:
            component: The kind of component to be withdrawn.
        Returns:
            True if a component was withdrawn.
        """

        if component not in self.components:
            return False

        if self.components[component] <= 0:
            return False

        self.components[component] -= 1

        return True
