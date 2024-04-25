.. _solver-class:

Solver class
+++++++++++++++++++++++++++++++
This class is the main class which is called when you want to simulate a district heating system.
It stores the :ref:`network-class` and it creates and stores the :ref:`matrix-class`.
Furthermore it is responsible for the communication between the two.
The solver will get the equations from the network and pass them to the matrix to be solved.
The solution is passed back to the network.

.. autoclass:: simulator_core.solver.solver.Solver
   :members: