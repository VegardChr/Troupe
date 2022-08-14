"""Prey agent."""

from random import uniform

import pygame
from pygame import Color, Surface, Vector2, gfxdraw

from ...actor import Actor
from ...bdi_agent import BDIAgent
from ...environment import Environment
from .consumable import Consumable
from .grass import Grass


class Prey(BDIAgent, Consumable):
    """
    Prey is a BDI agent that traverses
    the environment looking for food,
    such that it can reproduce.
    """

    layer = 3

    # Base image, common for all prey.
    base_image = Surface((16, 16), pygame.SRCALPHA)
    gfxdraw.filled_polygon(
        base_image,
        [(8, 0), (15, 6), (15, 15), (8, 11), (7, 11), (0, 15), (0, 6), (7, 0)],
        Color(64, 32, 220),
    )

    # What the prey consumes to reduce hunger.
    consumes: type[Actor] = Grass

    def __init__(
        self,
        position: Vector2,
        observable_distance: float = 64,
        speed: float = 32,
    ) -> None:
        """
        Initialize prey.

        Args:
            position: Initial position of prey.
            consumables: Food consumed by the prey.
            observable_distance: Maximum visible range of prey. Defaults to 64.
            speed: Speed of prey. Defaults to 32.
        """

        BDIAgent.__init__(
            self,
            self.base_image,
            position,
            observable_distance,
            10,
            speed,
            Vector2(uniform(-1, 1), uniform(-1, 1)),
        )
        Consumable.__init__(self, nutrition=30)

        # Hunger 100 = Death, Hunger < 30 = Can Reproduce.
        self.hunger = 50.0

        # Initialize the intention of the actor.
        self.intention = self.Desire("Reproduce", 0, self.plan_reproduce)

        # True if the agent should produce offspring.
        self.produce_offspring = False

    @property
    def can_reproduce(self) -> bool:
        """
        Determine if the agent can reproduce.
        """

        return self.hunger <= 30

    @property
    def alive(self) -> bool:
        """
        Determine if agent is alive.
        """

        return self.hunger <= 100

    def eat(self, food: Actor) -> None:  # Consume.
        """
        Eat food.

        Args:
            food: The food to eat.
        """

        # Ensure the food is eaten by the actor.
        if not isinstance(food, self.consumes):
            return
        # Ensure the food is consumable.
        if not isinstance(food, Consumable):
            return

        # Consume food.
        food.consumed = True

        # Update hunger.
        self.hunger -= food.nutrition
        self.hunger = max(self.hunger, 0)  # Hunger can not go below zero.

    def mate(self, partner: "Prey") -> None:
        """
        Produce offspring.

        (Called by another agent to mate with this agent.)

        Args:
            partner: Partner to reproduce with.
        """

        partner.hunger += 20
        self.hunger += 20
        self.produce_offspring = True

    def plan_reproduce(self) -> None:
        """
        Plan for reproducing.
        """

        # If unable to reproduce.
        if not self.can_reproduce:
            # Find closest food and eat it.
            self.action_interact_closest(self.consumes, self.eat)
            return

        # Find closest partner and mate with them.
        self.action_interact_closest(type(self), self.mate)

    def create_child(self) -> Actor:
        """
        Produce offspring.

        Returns:
            The offspring.
        """

        return Prey(Vector2(self.position))

    def update(self, environment: Environment, delta: float) -> None:
        BDIAgent.update(self, environment, delta)

        self.wraparound(environment)

        # Update hunger.
        self.hunger += delta
        if not self.alive:
            environment.actors.remove(self)

        # Produce offspring.
        if self.produce_offspring:
            environment.actors.append(self.create_child())
            self.produce_offspring = False

        # Remove ourselves from env, if consumed.
        if self.consumed:
            environment.actors.remove(self)
