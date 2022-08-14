"""BDIAgent module."""

from dataclasses import dataclass
from typing import Callable, TypeVar, cast
from uuid import UUID

from pygame import Surface, Vector2
from pygame.font import Font

from .actor import Actor
from .agent import Agent
from .environment import Environment
from .typeutils import SupportsRichComparison

ActorT = TypeVar("ActorT", bound=Actor)


class BDIAgent(Agent):
    """
    Belief-Desire-Intention (BDI) agents have desires which they would like to fulfill,
    each desire has an associated strength value. The desire with the highest strength,
    becomes the intention of the BDI agent.

    Each desire has an associated plan which the BDI agent uses to fulfill their desire.

    BDI agents can record previously made observations as beleifs and recall these from memory.
    """

    @dataclass
    class Desire:
        """BDI agent desire."""

        # Name of the desire. (What does the agent want to do?)
        name: str
        # Strength of the desire. (How much does the agent want to do it?)
        strength: int
        # Plan for achieving/fulfilling desire. (How does the agent want to achieve it?)
        plan: Callable[[], None]

        # Desires are considered idential if their names are the same.
        def __eq__(self, __o: object) -> bool:
            return self.name == __o.name if isinstance(__o, BDIAgent.Desire) else False

        def __hash__(self) -> int:
            return self.name.__hash__()

    # NOTE: Untested feature!
    # TODO: Perhaps give prey a reflex to flee if they see a predator? (Predator-Prey Simulation)
    @dataclass
    class Reflex:
        """BDI agent reflex."""

        # Name of the reflex. (What should the agent react to?)
        name: str
        # Reflex activation condition. (When should the agent react?)
        condition: Callable[[], bool]
        # Plan for reacting to reflex. (How should the agent react?)
        plan: Callable[[], None]

        def react(self) -> None:
            """Execute plan if condition equates to true."""

            if self.condition():
                self.plan()

        # Reflexes are considered idential if their names are the same.
        def __eq__(self, __o: object) -> bool:
            return self.name == __o.name if isinstance(__o, BDIAgent.Reflex) else False

        def __hash__(self) -> int:
            return self.name.__hash__()

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        observable_distance: float = 0.0,
        interactable_distance: float = 0.0,
        speed: float = 0.0,
        direction: Vector2 = Vector2(0, 1),
    ) -> None:
        """
        Initialize the BDI agent.

        Args:
            image: Image for visualizing the BDI agent.
            position: Initial position.
            observable_distance: Maximum distance at which BDI agent can observe other actors. Defaults to 0.0.
            speed: Speed of the actor. Defaults to 0.0.
            direction: Initial direction. Defaults to Vector2(0, 1).
        """

        Agent.__init__(
            self, image, position, observable_distance, interactable_distance, speed, direction
        )

        # Desires.
        self.desires: set["BDIAgent.Desire"] = {BDIAgent.Desire("Idle", 0, lambda: None)}

        # Reflexes.
        self.reflexes: set["BDIAgent.Reflex"] = set()

        # Beliefs about other actors in the simulation.
        self.beliefs: dict[type[Actor], set[Actor]] = {}

    @property
    def intention(self) -> Desire:
        """
        The intention of the agent.

        Returns:
            The desire with the highest strength.
        """

        return max(self.desires, key=lambda desire: desire.strength)

    @intention.setter
    def intention(self, desire: Desire) -> None:
        """
        Set the intention of the agent.

        Args:
            desire: The desire to set as the intention.
        """

        desire.strength = (
            desire.strength
            if desire.strength > self.intention.strength
            else self.intention.strength + 1
        )
        self.desires.add(desire)

    def set_intention(self, name: str, plan: Callable[[], None]) -> None:
        """
        Set the intention of the agent.

        Args:
            name: Name of the desire.
            plan: Plan for fulfilling desire.
        """

        # If the strength is less than the current intention's strength.
        # The intention setter will increase strength such that it becomes highest.
        self.intention = self.Desire(name, 0, plan)

    def recollect(
        self,
        actor_type: type[ActorT],
    ) -> list[ActorT]:
        """
        Recollect actors of a given type.

        Note that recollect returns copies of actors,
        as they were last observed and not the actors
        (that are part of the environment) themselves.

        Args:
            actor_type: Type of the actor.

        Returns:
            Actors of the specified type.
        """

        if actor_type not in self.beliefs:
            return []
        return cast(list[ActorT], list(self.beliefs[actor_type]))

    def recollect_where(
        self,
        actor_type: type[ActorT],
        condition: Callable[[ActorT], bool],
    ) -> list[ActorT]:
        """
        Recollect actors where a condition is satisfied.

        Args:
            actor_type: Type of the actor.
            condition: Condition the actor must satisfy.

        Returns:
            Actors that satisfy the condition.
        """

        # Actors of the specified type.
        candidates = self.recollect(actor_type)

        # Actors that satisfy the condition.
        return [candidate for candidate in candidates if condition(candidate)]

    def recollect_id(
        self,
        actor_type: type[ActorT],
        uuid: UUID,
    ) -> ActorT | None:
        """
        Recollect actor with the given id.

        Args:
            actor_type: Type of the actor.
            uuid: ID of the actor.

        Returns:
            Actor with the ID, if it was found.
        """

        candidates = self.recollect_where(actor_type, lambda actor: actor.uuid == uuid)

        # Ensure that we did not find more than one actor with the ID.
        assert (
            len(candidates) <= 1
        ), "Environment should only contain a single actor with the specified ID."

        return candidates[0] if candidates else None

    def recollect_min(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Recollect actor that has the the minimum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of minimum value.
        """
        candidates = self.recollect(actor_type)
        return min(candidates, key=selector) if candidates else None

    def recollect_max(
        self,
        actor_type: type[ActorT],
        selector: Callable[[ActorT], SupportsRichComparison],
    ) -> ActorT | None:
        """
        Recollect actor that has the the maximum value,
        using the selector function.

        Args:
            actor_type: Type of the actor.
            selector: Selector function.

        Returns:
            The actor of maximum value.
        """
        candidates = self.recollect(actor_type)
        return max(candidates, key=selector) if candidates else None

    def recollect_closest(
        self,
        actor_type: type[ActorT],
    ) -> ActorT | None:
        """
        Recollect the closest actor.

        Args:
            actor_type: Type of the actor.

        Returns:
            The closest actor.
        """

        return self.recollect_min(
            actor_type,
            lambda actor: self.position.distance_to(
                actor.position,
            ),
        )

    def action_travel(
        self,
        destination: Vector2,
        distance: float,
        name: str = "Travel",
    ) -> None:
        """
        Make the agent travel within a given distance of the destination.

        Args:
            destination: Destination to travel to.
            distance: Distance to travel within.
            name: Name for the desire. Defaults to "Travel".
        """

        self.intention = self.Desire(
            name,
            0,
            lambda: self.plan_travel(
                destination,
                distance,
            ),
        )

    def plan_travel(self, destination: Vector2, distance: float) -> None:
        """
        Plan for traveling within the given distance of the destination.

        Args:
            destination: Destination to travel to.
            distance: Distance to travel within.
        """

        # Keep turning towards the destination until we reach it.
        if not self.within_distance(destination, distance):
            self.steer_towards(destination)
            return

        # Remove current intention when we reach our destination.
        self.desires.remove(self.intention)

    def action_explore(
        self,
        goal: Callable[[], bool],
        name: str = "Explore",
    ) -> None:
        """
        Make agent explore until the goal is reached.

        Args:
            goal: Goal to reach before ceasing exploration.
            name: Name for the desire. Defaults to "Explore".
        """

        self.intention = self.Desire(
            name,
            0,
            lambda: self.plan_explore(goal),
        )

    def plan_explore(self, goal: Callable[[], bool]) -> None:
        """
        Plan for exploring the environment until goal is reached.

        Args:
            goal: Goal to reach before ceasing exploration.
        """

        # Turn randomly until we achieve our goal.
        if not goal():
            self.steer_random()
            return

        # Remove current intention when we achieve our goal.
        self.desires.remove(self.intention)

    def action_interact_any(
        self,
        target_type: type[ActorT],
        action: Callable[[ActorT], None],
        name: str = "Interact Any",
    ) -> None:
        """
        Make the agent perform an interaction with any actor of the specified type.

        NOTE: If no suitable actor was found,
        action will instead explore until one is found.

        Args:
            target_type: The type of agent to interact with.
            action: The interaction to perform.
            name: Name for the desire. Defaults to "Interact Any".
        """

        candidates = self.recollect(target_type)
        if not candidates:
            # Explore in search of actor.
            self.action_explore(
                lambda: bool(self.look(target_type)),
                name=f"Explore ({str(target_type.__name__)})",
            )
            return

        target = candidates.pop()

        # Interact with selected actor.
        self.action_interact_with(
            target,
            action,
            name=f"{name} ({str(target_type.__name__)})",
        )

    def action_interact_with(
        self,
        target: ActorT,
        action: Callable[[ActorT], None],
        name: str = "Interact With",
    ) -> None:
        """
        Make the agent perfrom an interaction with a target.

        Args:
            target: The target to interact with.
            action: The interaction to perform.
            name: Name for the desire. Defaults to "Interact With".
        """

        self.intention = self.Desire(
            name,
            0,
            lambda: self.plan_interact(target, action),
        )

    def action_interact_where(
        self,
        target_type: type[ActorT],
        condition: Callable[[ActorT], bool],
        action: Callable[[ActorT], None],
        name: str = "Interact Where",
    ) -> None:
        """
        Make the agent perform an interaction with an actor that satisfies the condition.

        Args:
            target_type: The type of agent to interact with.
            condition: The condition the actor must satisfy.
            action: The interaction to perform.
            name: Name for the desire. Defaults to "Interact Where".
        """

        if candidates := self.recollect_where(target_type, condition):

            # Interact with one of the candidates.
            self.action_interact_with(
                candidates.pop(),
                action,
                name=f"{name} ({str(target_type.__name__)})",
            )

    def action_interact_min(
        self,
        target_type: type[ActorT],
        action: Callable[[ActorT], None],
        selector: Callable[[ActorT], SupportsRichComparison],
        name: str = "Interact Min",
    ) -> None:
        """
        Uses the selector function to select the actor
        of minimum value to perform the interaction with.

        Args:
            target_type: The type of agent to interact with.
            action: The interaction to perform.
            selector: Selector function.
            name: name: Name for the desire. Defaults to "Interact Min".
        """

        # Find closest actor.
        target = self.recollect_min(target_type, selector)

        # If prey does not know about any actor of the specified type.
        if target is None:
            # Rely on action_interact_any to explore until a suitable actor is found.
            self.action_interact_any(
                target_type,
                action,
                name=f"Interact Any ({str(target_type.__name__)})",
            )
            return

        # Interact with selected actor.
        self.action_interact_with(
            target,
            action,
            name=f"{name} ({str(target_type.__name__)})",
        )

    def action_interact_max(
        self,
        target_type: type[ActorT],
        action: Callable[[ActorT], None],
        selector: Callable[[ActorT], SupportsRichComparison],
        name: str = "Interact Max",
    ) -> None:
        """
        Uses the selector function to select the actor
        of maximum value to perform the interaction with.

        Args:
            target_type: The type of agent to interact with.
            action: The interaction to perform.
            selector: Selector function.
            name: name: Name for the desire. Defaults to "Interact Max".
        """

        # Find closest actor.
        target = self.recollect_max(target_type, selector)

        # If prey does not know about any actor of the specified type.
        if target is None:
            # Rely on action_interact_any to explore until a suitable actor is found.
            self.action_interact_any(
                target_type,
                action,
                name=f"Interact Any ({str(target_type.__name__)})",
            )
            return

        # Interact with selected actor.
        self.action_interact_with(
            target,
            action,
            name=f"{name} ({str(target_type.__name__)})",
        )

    def action_interact_closest(
        self,
        target_type: type[ActorT],
        action: Callable[[ActorT], None],
    ) -> None:
        """
        Make the agent perform an interaction with the closest target of a type.

        Args:
            target_type: The type of agent to interact with.
            action: The interaction to perform.
        """

        self.action_interact_min(
            target_type,
            action,
            lambda actor: self.position.distance_to(
                actor.position,
            ),
            "Interact Closest",
        )

    def plan_interact(self, target: ActorT, action: Callable[[ActorT], None]) -> None:
        """
        Plan for perfroming an interaction with a target.

        Args:
            target: The target to interact with.
            action: The interaction to perform.
        """

        # If agent no longer has any knowledge about the target,
        # we should stop trying to intract with it.
        if self.recollect_id(type(target), target.uuid) is None:
            # NOTE: Excessive amounts of this warning MIGHT be an
            # indication that you are doing something wrong.
            # Feel free to comment out line if you know what you are doing!
            self.log(f"WARNING: Impossible to interact with {target} (no knowledge).")
            self.desires.remove(self.intention)
            return

        # If target is a belief.
        if target.is_belief:
            # If target can not be observed.
            if (actor := self.look_id(type(target), target.uuid)) is None:
                # Travel within observable distance of the target.
                self.action_travel(
                    target.position,
                    self.observable_distance,
                    name=f"Travel-O ({type(target).__name__})",
                )
                return

            # Set target to the observed actor.
            target = actor

        # If unable to interact with the target.
        if not self.can_interact(target):
            # Travel within interactible distance of the target.
            self.action_travel(
                target.position,
                self.interactable_distance,
                name=f"Travel-I ({type(target).__name__})",
            )
            return

        # Perfrom the interaction with the target.
        action(target)

        # Remove intention after having performed the interaction.
        self.desires.remove(self.intention)

    def invalidate_beliefs(self) -> None:
        """
        Remove beliefs that are known to be invalid.
        """

        # Beliefs about actors that should have been observed this tick.
        beliefs = {
            belief
            for beliefs in self.beliefs.values()
            for belief in beliefs
            if self.within_distance(belief.position, self.observable_distance)
        }

        # All actors that were observed this tick.
        observations = [
            observation
            for observations in self.observations.values()
            for observation in observations
        ]

        # Actors that were not observed,
        # although our beliefs tell us that we should have.
        difference = beliefs.difference(observations)

        # Remove invalid beliefs.
        for actor in difference:
            self.beliefs[type(actor)].remove(actor)

    def update_beliefs(self) -> None:
        """
        Update agent beliefs.
        Records/Remembers all actors that were observed.
        """

        # NOTE: This does not work very well for actors that move.
        # Sometimes the actor does not maintain a belief about observed actor.

        for actor_type, observations in self.observations.items():

            # Add key-value pair, if key (actor_type) does not exist in beliefs.
            # (Ensure that there exists a belief set for every actor type.)
            if actor_type not in self.beliefs:
                self.beliefs[actor_type] = set()

            # Update belief sets with newly aquired beliefs.
            for observation in observations:
                # Create a copy of the observed actor.
                actor_copy = observation.copy()
                actor_copy.is_belief = True

                # Discard any existing belief.
                self.beliefs[actor_type].discard(actor_copy)
                # Add the new belief.
                self.beliefs[actor_type].add(actor_copy)

        # Invalidate beliefs that are not accurate.
        self.invalidate_beliefs()

    def update(self, environment: Environment, delta: float) -> None:
        Agent.update(self, environment, delta)

        # Remember what has been observed.
        self.update_beliefs()

        # Reflexes.
        for reflex in self.reflexes:
            reflex.react()

        # Execute the plan.
        self.intention.plan()

    def draw(self, font: Font, surface: Surface) -> None:
        Agent.draw(self, font, surface)
        surface.blit(
            font.render(
                f"{str(self.uuid)[:4]} - {self.intention.name}",
                True,
                (255, 255, 255, 255),
            ),
            self.position,
        )
