Controller
=====================================
The controller manages set points for assets in the simulator. 
ESDL data is parsed by mapper functions into controller objects. 
These objects are stored in an overarching controller class, 
which is invoked at each time step to calculate and return the set points for that step. 
The set points are passed back to the simulator in a dictionary format, 
where the key is the asset ID, and the value is another dictionary. 
This inner dictionary holds the set points, with the keys being properties (e.g., supply temperature, heat demand) 
and the values being their corresponding set points.

The overarching controller class prioritizes source allocation based on a priority system. 
It first assigns capacity from priority 1 sources. If more capacity is needed, it moves to priority 2, 
and so on. If demand is lower than the available capacity at a given priority, the excess is equally distributed across the sources. 
If demand exceeds capacity, a message is sent to the user, and demand is downscaled to match available resources.

When storage is present, the controller first allocates source capacity to meet consumer demand. 
Any remaining capacity is used to charge the storage. If source capacity is insufficient, 
the controller taps into the storage to meet the remaining demand. 
This basic control strategy may be extended with more complex strategies in the future.

The controller consists of the following classes:

#. :ref:`main_controller_class`: Main controller class, used to store the assets and calculate the control value for a time step.
#. :ref:`consumer_controller_class`: Class to control consumers in the network
#. :ref:`producer_controller_class`: Class to control producers in the network
#. :ref:`ates_controller_class`: Class to control Ates cluster in the network

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    main_controller_class
    assets/consumer
    assets/producer
    assets/ates

