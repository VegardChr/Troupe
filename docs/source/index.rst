Welcome to Troupe!
===================

Troupe is a framework for simulating multi-agent environments.
To get a better understanding of how to use Troupe, it is recommended that you check out the :doc:`examples <troupe.examples>`.
The :doc:`miners <troupe.examples.miners>` example is a good place to start.

| To run an example from the command-line, use: ``python -m troupe -e {example}``

Actors
-------------------
In Troupe, all environments consist of actors.

:doc:`Actors <troupe.actor>` primarily exist to give agents the ability to interact with them.
Agents do not interact with other actors,
they may however blindly traverse the environment independently,
occasionally bumping into others unknowingly.

Agents
-------------------

:doc:`Agents <troupe.agent>` are `intelligent agents <https://en.wikipedia.org/wiki/Intelligent_agent>`_
that inherit the behavior of actors. Agents observe their environment and use reasoning before acting.

BDI Agents
-------------------

:doc:`BDI Agents <troupe.bdi_agent>` are intelligent agents with desires and beliefs.
Troupe implements a very simplified `BDI model <https://en.wikipedia.org/wiki/Belief%E2%80%93desire%E2%80%93intention_software_model>`_.
In Troupe, the strongest desire of a BDI agent, becomes its intention.
The intention is the desire which the BDI agent will work towards fulfilling.
In order to achieve their desires, BDI agents specify plans for how to act.
Plans contain instructions which lead the BDI agent to fulfilling their desire.
Once a desire is adopted as the BDI agent's intention, the plan associated with the desire is executed.

BDI agents implement common plans such as "Explore" and "Travel".
To quickly set the intention of a BDI agent to explore an environment or travel to a location.
See methods ``action_explore`` and ``action_travel`` in :doc:`BDIAgent <troupe.bdi_agent>`.

Index
===================

.. toctree::
   :maxdepth: 4
   :caption: Modules

   troupe.actor
   troupe.agent
   troupe.bdi_agent
   troupe.environment
   troupe.simulation
   troupe.troupe
   troupe.quadtree
   troupe.typeutils

.. toctree::
   :maxdepth: 1
   :caption: Examples

   troupe.examples.boids
   troupe.examples.predators
   troupe.examples.miners
   troupe.examples.factory
