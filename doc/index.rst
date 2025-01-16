.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OMOTES simulator-core documentation!
==============================================================
This is the documentation for the OMOTES simulator. This simulator can be used the simulate
thermo-hydraulics of a district heating system. This simulator is developed as part of the
Dutch Nieuwe Warmte Nu program. More info can be found the  `NWN website`_.
The simulator is written in Python.
As input it use the `ESDL`_ format. The results are passed back as a pandas dataFrame.
This documentation is divided in the following sections:

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   architecture/architecture
   solver/solver_main
   assets/assets
   controller/controller


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _NWN website: https://www.nwn.nu/
.. _ESDL: https://www.esdl.nl/
