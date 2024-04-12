Solver architecture
=========================
To solve one time step of the simualtion the solver is used.
This solver is solving both the hydraulic and thermo dynamic equations.
As unknown the following quantities are solved:

#. Mass flow rate [kg/s]
#. Total pressure [Pa]
#. Specific internal energy [J/kg]

The later is depending on the temperature and specifies the amount of energy needed to change the
temperature form one to another. Basically it is the specific heat of a fluid integrated
over temperature.
These quantities are solved for all the connect point of components, but also for all the nodes
between components. This results in a system of equation, for which part are non-linear.
To solve them these equations are linearized via the Newton-Raphson method.
The resulting matrix is solved with the numpy matrix solver.
This has been implemented in een object oriented way. We have the following classes:

#. Matrix class: This class houses the matrix and methods to solve it.
#. Equation object class: This class is used to store the equations.
#. Network class: This class stores the different assets which are in the network and the connecting nodes.
#. Asset classes: this comprises of different classes to simulate the physics of different assets.
#. Solver class: main class, which stores the network and the matrix and is
responsible for the communication between the two.

Next to this there are several utility modules and class, which are use to support all the classes.




