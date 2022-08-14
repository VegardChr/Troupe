from copy import copy
from typing import Callable, Iterator, TypeVar, cast
from uuid import UUID

from .actor import Actor
from .typeutils import SupportsRichComparison

ActorT = TypeVar("ActorT", bound=Actor)


class Troupe:
    """A collection of actors."""

    def __init__(self, actors: list[Actor] | None = None) -> None:
        self._actors: dict[type[Actor], set[Actor]] = {}
        if actors is None:
            return

        for actor in actors:
            self.add(actor)

    def add(self, actor: Actor) -> None:
        """Add an actor to the troupe."""

        # If a set for the type of actor does not exist.
        if type(actor) not in self._actors:
            # Create a new set for the type of actor
            self._actors[type(actor)] = set()

        else:
            # Discard actor if it is already in the troupe.
            self.discard(actor)

        # Add the actor to the troupe.
        self._actors[type(actor)].add(actor)

    def remove(self, actor: Actor) -> None:
        """Remove an actor from the troupe."""

        self._actors[type(actor)].remove(actor)

    def discard(self, actor: Actor) -> None:
        """Discard an actor from the troupe."""

        self._actors[type(actor)].discard(actor)

    def clear(self) -> None:
        """Clear the troupe of all actors."""

        self._actors.clear()

    def find(
        self,
        actor_type: type[ActorT],
    ) -> list[ActorT]:
        """
        Find for actors of a specific type.

        Args:
            actor_type: Type of the actors to find for.

        Returns:
            Actors of the specified type.
        """

        if actor_type not in self._actors:
            return []

        return cast(list[ActorT], list(self._actors[actor_type]))

    def find_where(
        self,
        actor_type: type[ActorT],
        condition: Callable[[ActorT], bool],
    ) -> list[ActorT]:
        """
        Find for actors where a condition is satisifed.

        Args:
            actor_type: Type of the actors to find for.
            condition: Condition the actors must satisfy.

        Returns:
            Actors that satisfy the condition.
        """

        # Actors of the specified type.
        candidates = self.find(actor_type)

        # Actors that satisfy the condition.
        return [candidate for candidate in candidates if condition(candidate)]

    def find_id(
        self,
        actor_type: type[ActorT],
        uuid: UUID,
    ) -> ActorT | None:
        """
        Find for actor that has the given id.

        Args:
            actor_type: Type of the actor.
            uuid: ID of the actor.

        Returns:
            Actor with the ID, if it was found.
        """

        candidates = self.find_where(actor_type, lambda actor: actor.uuid == uuid)

        # Ensure that we did not find more than one actor with the ID.
        assert (
            len(candidates) <= 1
        ), "Environment should only contain a single actor with the specified ID."

        return candidates[0] if candidates else None

    def find_min(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Find for the actor that has the the minimum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of minimum value.
        """

        candidates = self.find(actor_type)
        return min(candidates, key=selector) if candidates else None

    def find_max(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Find for the actor that has the the maximum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of maximum value.
        """

        candidates = self.find(actor_type)
        return max(candidates, key=selector) if candidates else None

    def find_closest(
        self,
        actor: ActorT,
        actor_type: type[ActorT],
    ) -> ActorT | None:
        """
        Find for the closest actor.

        Args:
            actor: Look for closest actor to this actor.
            actor_type: Look for closest actor of this type.

        Returns:
            The closest actor.
        """

        return self.find_min(
            actor_type,
            lambda candidate: actor.position.distance_to(candidate.position),
        )

    def copy(self) -> "Troupe":
        """Create a shallow copy of the troupe."""

        return copy(self)

    def __contains__(self, __o: object) -> bool:
        return __o in self._actors[type(__o)] if isinstance(__o, Actor) else False

    def __iter__(self) -> Iterator[Actor]:
        return (belief for beliefs in self._actors.values() for belief in beliefs)
