"""Agent module."""


from typing import Callable, TypeVar, cast
from uuid import UUID

from pygame import Surface, Vector2

from .actor import Actor
from .environment import Environment
from .typeutils import SupportsRichComparison

ActorT = TypeVar("ActorT", bound=Actor)


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
        self.observations: dict[type[Actor], set[Actor]] = {}

    def look(
        self,
        actor_type: type[ActorT],
    ) -> list[ActorT]:
        """
        Look for actors of a specific type.

        Args:
            actor_type: Type of the actors to look for.

        Returns:
            Actors of the specified type.
        """

        if actor_type not in self.observations:
            return []

        return cast(list[ActorT], list(self.observations[actor_type]))

    def look_where(
        self,
        actor_type: type[ActorT],
        condition: Callable[[ActorT], bool],
    ) -> list[ActorT]:
        """
        Look for actors where a condition is satisifed.

        Args:
            actor_type: Type of the actors to look for.
            condition: Condition the actors must satisfy.

        Returns:
            Actors that satisfy the condition.
        """

        # Actors of the specified type.
        candidates = self.look(actor_type)

        # Actors that satisfy the condition.
        return [candidate for candidate in candidates if condition(candidate)]

    def look_id(
        self,
        actor_type: type[ActorT],
        uuid: UUID,
    ) -> ActorT | None:
        """
        Look for actor that has the given id.

        Args:
            actor_type: Type of the actor.
            uuid: ID of the actor.

        Returns:
            Actor with the ID, if it was found.
        """

        candidates = self.look_where(actor_type, lambda actor: actor.uuid == uuid)

        # Ensure that we did not find more than one actor with the ID.
        assert (
            len(candidates) <= 1
        ), "Environment should only contain a single actor with the specified ID."

        return candidates[0] if candidates else None

    def look_min(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Look for the actor that has the the minimum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of minimum value.
        """

        candidates = self.look(actor_type)
        return min(candidates, key=selector) if candidates else None

    def look_max(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Look for the actor that has the the maximum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of maximum value.
        """

        candidates = self.look(actor_type)
        return max(candidates, key=selector) if candidates else None

    def look_closest(
        self,
        actor_type: type[ActorT],
    ) -> ActorT | None:
        """
        Look for the closest actor.

        Args:
            actor_type: Type of the actor.

        Returns:
            The closest actor.
        """

        return self.look_min(
            actor_type,
            lambda actor: self.position.distance_to(actor.position),
        )

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
            if type(actor) not in self.observations:
                self.observations[type(actor)] = set()
            if actor in self.observations[type(actor)]:
                self.observations[type(actor)].remove(actor)
            self.observations[type(actor)].add(actor)

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
