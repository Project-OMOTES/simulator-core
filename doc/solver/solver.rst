.. _solver-class:

Solver class
+++++++++++++++++++++++++++++++
This class is the main class called when you want to simulate a district heating system. It stores 
the :ref:`network-class` and creates and stores the :ref:`matrix-class`. Furthermore, it is 
responsible for the communication between the two. The solver will get the equations from the 
network and pass them to the matrix to be solved. The solution is then passed back to the network.

.. autoclass:: omotes_simulator_core.solver.solver.Solver
   :members: