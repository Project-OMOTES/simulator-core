.. _main_controller_class:

Network controller class
=====================================
The NetworkController class serves as the base controller, managing lists of controllable assets.
The update_setpoints method retrieves controller settings for a specific time step.

To create a custom controller, implement a new class with your desired logic and inherit from
the NetworkControllerAbstract class.

.. autoclass:: omotes_simulator_core.entities.network_controller_abstract.NetworkControllerAbstract
    :members:
    :no-index:

.. autoclass:: omotes_simulator_core.entities.network_controller.NetworkController
    :members:
    :no-index:
