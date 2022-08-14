"""Chairman meta-agent."""

from enum import Enum
from random import choice

from pygame import Surface, Vector2
from pygame.font import Font

from ...agent import Agent
from ...environment import Environment
from .assembly import Assembly
from .worker import Worker


class Chairman(Agent):
    """Chairman meta-agent."""

    class ReassignmentPolicy(Enum):
        """Reassignment policy enumeration."""

        NONE = 0
        RANDOM = 1
        MOST_IDLE = 2

    def __init__(
        self,
        image: Surface,
        position: Vector2,
        observable_distance: int,
        interactable_distance: int,
        reassignment_interval: float,
        reassignment_policy: ReassignmentPolicy,
    ) -> None:
        """
        Initialize the chairman meta-agent.

        Args:
            image: Image used to visualize the chairman.
            position: Position of the chairman.
            observable_distance: Observable distance.
            interactable_distance: Interactible distance.
            reassignment_interval: How often the chairman reassigns workers.
            reassignment_policy: Policy to use for worker reassignment.
        """

        Agent.__init__(self, image, position, observable_distance, interactable_distance)

        # Time between meetings.
        self.reassignment_interval = reassignment_interval

        # Time until next meeting.
        self.reassignment_timer = reassignment_interval

        # Reassignment policy used by the chairman.
        self.reassginment_policy = reassignment_policy

        # Most recently reassigned worker.
        self.debug_recent_assignee: Worker | None = None

    def policy_random(self, worker: Worker) -> None:
        """
        Assign a worker to work at a random assembly.
        """

        # Assemblies observed by the chairman.
        assemblies = self.observations.find(Assembly)

        # Return if the chairman observed no assemblies.
        if not assemblies:
            return

        # Choose a random assembly.
        assembly = choice(assemblies)

        # Assign the worker to work at the chosen assembly.
        worker.assigned_assembly = assembly.uuid

    def policy_most_idle(self, worker: Worker) -> None:
        """
        Assign a worker to work at the assembly that spent the most time idle.
        """

        # The assembly that has spent the most time waiting.
        assembly = self.observations.find_max(Assembly, lambda assembly: assembly.total_idle_time)

        # Return if the chairman observed no assemblies.
        if assembly is None:
            return

        # Assign the worker to work at the assembly with the most idle time.
        worker.assigned_assembly = assembly.uuid

    def update(self, environment: Environment, delta: float) -> None:
        Agent.update(self, environment, delta)

        # Update reassigment timer.
        self.reassignment_timer -= delta

        # Return if it is not time to reassign a worker yet.
        if self.reassignment_timer > 0:
            return

        # Reset the reassignment timer.
        self.reassignment_timer = self.reassignment_interval

        # All workers observed by the chairman.
        workers = self.observations.find(Worker)

        # Return if the chairman observed no workers.
        if not workers:
            return

        # Chose a random worker to reassign.
        worker = choice(workers)
        self.debug_recent_assignee = worker

        # Employ the chosen policy for reassigning a worker.
        match self.reassginment_policy:
            case self.ReassignmentPolicy.NONE:
                # Do not reassign the worker.
                pass
            case self.ReassignmentPolicy.RANDOM:
                # Randomly assign the worker to a new assembly unit.
                self.policy_random(worker)
            case self.ReassignmentPolicy.MOST_IDLE:
                # Assign the worker to the most idle assembly unit.
                self.policy_most_idle(worker)

    def draw(self, font: Font, surface: Surface) -> None:
        Agent.draw(self, font, surface)
