.. _solver-pipe:

Solver pipe class
++++++++++++++++++++++++
The pipe class is a solver asset that represents a pipe in the network.
It is used to calculate the flow in the pipe and the pressure drop across the pipe.
It is derived from the fall type class, and extended with the heat loss over the pipeline.
The heat loss is calculated based on the actual physical properties of the pipe.

.. autoclass:: simulator_core.solver.network.assets.solver_pipe.SolverPipe
   :members: