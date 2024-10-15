.. _main_controller_class:

Network controller class
=====================================
The network controller class is the basic controller class. It stores lists of the controllable
assets. The method update_setpoints is used to get the controller settings for the given time step.

You can create your own controller class by implementing a new controller class with its own logic.
This class should inherit from the NetworkControllerAbstract class.

.. autoclass:: omotes_simulator_core.entities.network_controller_abstract.NetworkControllerAbstract
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.entities.network_controller.NetworkController
    :members:
    :no-index:
