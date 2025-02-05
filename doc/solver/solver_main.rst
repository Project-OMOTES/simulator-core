Solver architecture
=========================
To solve one time step of the simulation, the solver is used. This solver handles both the hydraulic 
and thermodynamic equations. The following quantities are solved as unknowns:

#. Mass flow rate [kg/s]
#. Total pressure [Pa]
#. Specific internal energy [J/kg]

The latter depends on the temperature and specifies the amount of energy needed to change the 
temperature from one value to another. Essentially, it is the specific heat of a fluid integrated 
over temperature. These quantities are solved for all the connection points of components, as well 
as for all the nodes between components. This results in a system of equations, some of which are 
non-linear. To solve them, these equations are linearized via the Newton-Raphson method. The 
resulting matrix is solved with the numpy matrix solver. This has been implemented in an object-
oriented way. We have the following classes:

#. :ref:`solver-class`: Main class, which stores the network and the matrix and is responsible for 
   communication between the two.
#. :ref:`matrix-class`: This class houses the matrix and methods to solve it.
#. :ref:`equation-object-class`: This class is used to store the equations.
#. :ref:`network-class`: This class stores the different assets in the network and the connecting 
   nodes.
#. :ref:`main-assets`: This comprises different classes to simulate the physics of various assets.
#. :ref:`solver-utility`: Module with utility functions used by the solver.

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    solver.rst
    matrix.rst
    equation_object.rst
    network.rst
    asset_main.rst
    solver_utility.rst





