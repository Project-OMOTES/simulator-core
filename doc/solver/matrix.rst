.. _matrix-class:

Matrix class
+++++++++++++++++++++++++++++++++++++++++++++
The matrix class stores the matrix of the system of equations. It is used to solve the system of equations.
The user can add unknowns to the matrix, the matrix solver will then pass the index in the matrix back.
This index should be used in creating equation objects. For solving the standard matrix solver as available in `numpy`_ is used.

.. autoclass:: omotes_simulator_core.solver.matrix.matrix.Matrix
   :members:

