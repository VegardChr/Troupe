"""Agent module."""


from pygame import Surface, Vector2

from .actor import Actor
from .environment import Environment
from .troupe import Troupe


class Agent(Actor):
    """
    An intelligent agent that can both observe and interact with its environment.
    """

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        observable_distance: float = 0.0,
        interactable_distance: float = 0.0,
        speed: float = 0.0,
        direction: Vector2 = Vector2(0, -1),
    ) -> None:
        """
        Initialize the agent.

        Args:
            image: Image used to visualize agent.
            position: Initial position.
            observable_distance: Maximum distance at which agent can observe other actors. Defaults to 0.0.
            speed: Speed of the actor. Defaults to 0.0.
            direction: Initial direction. Defaults to Vector2(0, 1).
        """

        Actor.__init__(self, image, position, direction, speed)

        # Agent can only observe actors within this distance.
        self.observable_distance = observable_distance

        # Agent can only interact with actors within this distance.
        self.interactable_distance = interactable_distance

        # Actors observed (on this tick) by the agent.
        self.observations = Troupe()

    def observe(self, environment: Environment) -> None:
        """
        Observes all actors visible to the agent.

        Args:
            environment: Environment the agent is part of.
        """

        # Reset observations.
        self.observations.clear()

        # Get all actors within the observable distance.
        actors = environment.quadtree.query_radius(self.position, self.observable_distance)

        # Do not observe ourselves.
        if self in actors:
            actors.remove(self)

        # Update observations.
        for actor in actors:
            self.observations.add(actor)

    def can_observe(self, actor: Actor) -> bool:
        """
        Determine if the actor is within
        observable distance of the actor.

        Args:
            actor: Actor to determine if we can observe.

        Returns:
            True if the actor is observable.
        """

        return self.within_distance(actor.position, self.observable_distance)

    def can_interact(self, actor: Actor) -> bool:

        """
        Determine if the agent is in
        range to interact with the actor.

        Note: Will return false if actor is a belief.

        Args:
            actor: The actor to interact with.

        Returns:
            True if we can interact with the actor.
        """

        # An agent can not interact with a belief.
        if actor.is_belief:
            return False

        return self.within_distance(actor.position, self.interactable_distance)

    def update(self, environment: Environment, delta: float) -> None:
        Actor.update(self, environment, delta)
        self.observe(environment)
