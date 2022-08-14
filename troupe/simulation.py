"""Simulation module."""

import pygame
from pygame.font import Font

from .environment import Environment


class Simulation:
    """Simulation class for simulating environments."""

    # Initialize pygame.
    pygame.init()
    pygame.display.set_caption("Simulation!", "Simulation")

    # Background color.
    background = pygame.Color(0, 0, 0)

    # Tickrate.
    tickrate = 60

    # Font for displaying FPS.
    font = Font(None, 30)

    @classmethod
    def run(
        cls,
        environment: Environment,
    ) -> None:
        """
        Begins the simulation.
        Each iteration of the simulation loop
        represents a single tick in the environment.

        Args:
            environment: The environment to simulate.
        """

        # Initialize clock.
        clock = pygame.time.Clock()

        # Initialize screen.
        screen = pygame.display.set_mode(
            environment.bounds.size,
            pygame.SRCALPHA,
        )

        while True:
            # Handle events from the event queue.
            for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):

                # Quit event.
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return
                    # sys.exit()

            # Clear the screen.
            screen.fill(cls.background)

            # Limit tickrate.
            delta = clock.tick(cls.tickrate) / 1000

            # Update all actors in environment.
            environment.update(delta)

            # Draw all actors in environment
            environment.draw(screen)

            # Display FPS.
            screen.blit(
                cls.font.render(
                    str(int(clock.get_fps())),
                    True,
                    (255, 255, 255, 255),
                ),
                (0, 0),
            )

            # Update the display.
            pygame.display.update()
