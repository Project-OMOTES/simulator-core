.. _equation-object-class:

Equation object class
+++++++++++++++++++++++++++++++++++++++++++++
An equation object consists of three parts:

#. A list of the indices in the matrix of the coefficients of the equation
#. A list of the coefficients of the equation
#. The right-hand side of the equation

The index is the sum of the indices in the matrix, which is obtained by the assets by setting their 
unknowns in the matrix with the quantity to be solved. This can be easily obtained by making use of 
the CoreQuantIndex class. The coefficients are obtained by linearizing the equations. The same holds 
for the right-hand side. This linearization should be done via the Newton-Raphson method. More 
information can be found on this `website`_.

.. autoclass:: omotes_simulator_core.solver.matrix.equation_object.EquationObject
   :members:

.. _website: https://en.wikipedia.org/wiki/Newton%27s_method