Controller
=====================================
The controller is responsible for providing set points for the assets in the simulator.
The ESDL is parsed in the mapper functions to controller objects. This will result in a controller
class object which can be called each time step. The controller will then calculate the set points
for this time step. It will then pass back the set points to the simulator.
This is done via a dict, where the key is the id of the asset and the value is another dict.
This dict contains the set points for the asset. The key of this dict is the property which needs
to be set (e.g. supply temperature, heat demand). The value is the set point for this property.

The current controller implementation works based on the priority of the source.
The controller will first allocate capacity of the source with the priority of 1.
If more capacity is required, the sources with priority 2 will be used etc. If the demand is
lower then the available capacity of the observed sources, the remaining demand will be equally
distributed over the source at the observed priority. In the case the demand is higher then the
available source capacity, a message is passed to the user and the demand is downscaled to match
the available capacity.

The controller consists of the following classes:

#. :ref:`main_controller_class`: Main controller class, used to store the assets and calculate the
control value for a time step.
#. :ref:`consumer_controller_class`: Class to control consumers in the network
#. :ref:`producer_controller_class`: Class to control producers in the network

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    main_controller_class
    assets/consumer
    assets/producer

