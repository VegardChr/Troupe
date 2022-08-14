Miners
==============================

Brief
-----
Miners search the map for gemstones.
Gemstones can be found in mines spread across the map.
The goal of the miners is to collect gemstones from mines
and bring them to a camp.

Implementation
--------------

All :doc:`miners <troupe.examples.miners.miner>` have a desire to get work done.
This desire ``Work`` utilizes ``plan_work`` which handles creating new desires
to collect and deliver gemstones.

Collecting a gemstone from a mine can implemented using the method ``action_interact_closest``:

.. code-block:: python

   # Collect gemstone from closest mine we know about.
   self.action_interact_closest(Mine, self.collect_gemstone)

This method creates a new desire by taking the type of actor to interact with (``Mine``),
along with a function:

.. code-block:: python

   def collect_gemstone(self, mine: Mine) -> None:
      self.hands = mine.kind

This function will recieve what the agent believes to be the closest actor as an argument.

When the agent has found the actor which it believes to be the closest,
a desire using ``plan_interact`` is created and set as the agent's intention.

Gemstone delivery can be implemented similarly:

.. code-block:: python

   # Deliver held gemstone to a camp.
   self.action_interact_closest(Camp, self.deposit_gemstone)

Putting it all together:

.. code-block:: python

   def plan_work(self) -> None:
      # If the miner has no gemstone.
      if self.hands is None:
         # Collect gemstone.
         self.action_interact_closest(Mine, self.collect_gemstone)
         return

      # Deliver gemstone.
      self.action_interact_closest(Camp, self.deposit_gemstone)

Contents
--------

.. toctree::
   :maxdepth: 4

   troupe.examples.miners.camp
   troupe.examples.miners.director
   troupe.examples.miners.env
   troupe.examples.miners.gemstone
   troupe.examples.miners.mine
   troupe.examples.miners.miner
