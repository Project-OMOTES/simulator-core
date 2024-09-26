Controller
=====================================
The controller is responsible for providing set points for the assets in the simulator.
The controller parses the ESDL and creates objects of the assets it is providing set points for.
When a time step is calculated the controller passes back a dict of the set points
for the controllable assets in the network. The key of this dict is the id of the asset.
The value is another dict. The key of this dict is the property which needs to be set
(e.g. supply temperature, heat demand). The value is the set point for this property.
The controller works based on the priority of the source. The controller will first allocate
capacity of the source with the priority of 1. If more capacity is required, the sources with
priority 2 will be used etc. If the demand is lower then the available capacity of the observed
sources, the remaining demand will be equally distributed over the source at the observed priority.
In the case the demand is higher then the available source capacity, a message is passed to the user
and the demand is downscaled to match the available capacity.
The controller consists of the following classes:

#. :ref:`main_controller_class`: Main controller class
#. :ref:`consumer_controller_class`: Class to control consumers in the network
#. :ref:`producer_controller_class`: Class to control producers in the network

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    main_controller_class
    assets/consumer
    assets/producer

