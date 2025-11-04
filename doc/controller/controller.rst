Controller
=====================================
The controller manages set points for assets in the simulator. 
ESDL data is parsed by mapper functions into controller objects. 
These objects are stored in an overarching controller class, 
which splits the district heating system into sub networks.
This split is done on the heat transfer assets (heat pump and heat exchangers). Each network holds the production,
consumption and storage assets hydraulic connected to that assets, together with a heat transfer asset, which is
either the primary side or the secondary side.
The overarching class is invoked at each time step to calculate and return the set points for that step.
The set points are passed back to the simulator in a dictionary format,
where the key is the asset ID, and the value is another dictionary. 
This inner dictionary holds the set points, with the keys being properties (e.g., supply temperature, heat demand) 
and the values being their corresponding set points.

The overarching controller class prioritizes source allocation based on a priority system. 
To cope with heat transfer assets it calculates a conversion factor to transfer heat from on sub network to another.
For heat exchangers this factor is 1 (assuming no loss) and for heat pumps it is equal to the COP, for now it is
constant, but it can be update each time step.
All heat demand, source power, charge and discharge rate of storage is converted to a value in the first sub network.
This is done be following the path each network has to take to go from the sub network to the first network and multiplying
all conversion factors.
Then the controller can start assigning capacity from priority 1 sources. If more capacity is needed, it moves to priority 2,
and so on. If demand is lower than the available capacity at a given priority, the excess is equally distributed across the sources.
If demand exceeds capacity, a message is sent to the user, and demand is downscaled to match available resources.

When storage is present, the controller first allocates source capacity to meet consumer demand.
Any remaining capacity is used to charge the storage. If source capacity is insufficient, 
the controller taps into the storage to meet the remaining demand.
In the assign step the set points are converted back to their respective sub networks.
This basic control strategy may be extended with more complex strategies in the future.

The controller consists of the following classes:

#. :ref:`main_controller_class`: Main controller class, used to store the assets and calculate the control value for a time step.
#. :ref:`sub_network_class`: Subnetwork class, which stores a sub network of the district heating system. This is part of the network which is hydrualicly connected.
#. :ref:`consumer_controller_class`: Class to control consumers in the network
#. :ref:`producer_controller_class`: Class to control producers in the network
#. :ref:`ates_controller_class`: Class to control Ates cluster in the network

**Contents**

.. toctree::
    :maxdepth: 1
    :glob:

    main_controller_class
    sub_network_class
    assets/consumer
    assets/producer
    assets/ates


