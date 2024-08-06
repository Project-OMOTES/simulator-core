.. _main_controller_class:

Network controller class
=====================================
The network controller class is hte basic controller class. It stores lists of the controllable
assets. The method run_time_step is used to get the controller settings for the given time step.
For developers if you want to implement a new controller a class can be created with its own logic
as long as there is a method run_time_step that returns the controller settings.

.. autoclass:: simulator_core.entities.network_controller.NetworkController
    :members:
    :no-index:
