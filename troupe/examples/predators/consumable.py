"""Consumable."""


class Consumable:
    """
    Inherited by an actor to make it consumable.
    """

    def __init__(self, nutrition: int = 20) -> None:

        # Has the consumable been consumed?
        self.consumed = False

        # Nutritonal value of the consumable.
        self.nutrition = nutrition
