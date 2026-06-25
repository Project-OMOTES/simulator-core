.. _asset_factory:

Asset factories
===============

Overview
--------

This page is a contributor-facing map of the ESDL asset factory layer. Use it when you need to see
what each concrete mapper adds on top of ``EsdlMapperAbstract`` during ESDL-to-entity conversion.

The key distinction is small but important: the abstract contract only declares the conversion
methods, while each concrete mapper implements simulator-specific construction logic in
``to_entity``. In the current codebase, every mapper on this page leaves ``to_esdl``
unimplemented and raises ``NotImplementedError``.

For the broader orchestration path that uses these mappers, see :doc:`architecture`.

Abstract mapper contract
------------------------

``EsdlMapperAbstract`` defines exactly two abstract methods:

* ``to_esdl(entity)`` for mapping a simulator entity back to an ESDL asset object.
* ``to_entity(model)`` for mapping an ESDL asset object into a simulator entity.

The base class does not provide shared field extraction, defaults, validation, or branching
behavior. Those responsibilities are entirely delegated to each concrete mapper. In the current
implementation, the concrete mappers on this page only specialize ``to_entity`` and intentionally
leave ``to_esdl`` unavailable.

Concrete mapper comparison
--------------------------

.. list-table::
     :header-rows: 1

     * - Mapper
         - Entity returned
         - ESDL data read
         - Defaults, branching, or validation
     * - ``EsdlAssetProducerMapper``
         - ``ProductionCluster``
         - Asset ``name``, ``id``, and port ids
         - No extra defaults or validation
     * - ``EsdlAssetConsumerMapper``
         - ``DemandCluster``
         - Asset ``name``, ``id``, and port ids
         - No extra defaults or validation
     * - ``EsdlAssetAtesMapper``
         - ``AtesCluster``
         - Asset ``name``, ``id``, port ids, aquifer and well properties
         - Falls back to ``ATES_DEFAULTS`` for every ATES-specific property it reads
     * - ``EsdlAssetHeatPumpMapper``
         - ``HeatPump`` or ``AirToWaterHeatPump``
         - Asset ``name``, ``id``, port ids, ``COP``, and optional ``power``
         - Branches on port count and raises on unsupported counts
     * - ``EsdlAssetHeatExchangerMapper``
         - ``HeatExchanger``
         - Asset ``name``, ``id``, port ids, and ``Efficiency``
         - Falls back to ``HeatExchangerDefaults`` when ``Efficiency`` is absent
     * - ``EsdlIdealHeatStorageMapper``
         - ``IdealHeatStorage``
         - Asset ``name``, ``id``, port ids, ``volume``, ``fillLevel``, and port temperatures
         - Falls back to ``HeatBufferDefaults`` for ``volume``/``fillLevel``; temperatures have no static default
     * - ``EsdlAssetPipeMapper``
         - ``Pipe``
         - Asset ``name``, ``id``, port ids, hydraulic and thermal properties
         - Mixes direct properties, defaults, helper-derived values, and EDR fallback logic

Per-mapper notes
----------------

Producer mapper
~~~~~~~~~~~~~~~

``EsdlAssetProducerMapper`` is the simplest specialization of the abstract contract. Its
``to_entity`` method constructs a ``ProductionCluster`` from only three inputs:
``esdl_asset.esdl_asset.name``, ``esdl_asset.esdl_asset.id``, and ``esdl_asset.get_port_ids()``.
It does not inspect any producer-specific ESDL properties, apply defaults, or perform validation.

Consumer mapper
~~~~~~~~~~~~~~~

``EsdlAssetConsumerMapper`` mirrors the producer mapper, but returns a ``DemandCluster``.
Its ``to_entity`` method also reads only the asset name, asset id, and port ids. No extra
consumer-specific properties are interpreted, and there is no branching or fallback logic.

ATES mapper
~~~~~~~~~~~

``EsdlAssetAtesMapper`` extends the minimal name/id/ports pattern by reading a larger property set
before constructing an ``AtesCluster``. In addition to the shared asset metadata, it reads these
ESDL properties, each falling back to ``ATES_DEFAULTS`` when absent:

.. list-table::
     :header-rows: 1

     * - ESDL property
         - Internal field
         - Default
         - Unit
     * - ``aquiferTopDepth``
         - ``aquifer_depth``
         - ``300.0``
         - m
     * - ``aquiferThickness``
         - ``aquifer_thickness``
         - ``45.0``
         - m
     * - ``aquiferMidTemperature``
         - ``aquifer_mid_temperature``
         - ``17.0``
         - degrees Celsius
     * - ``aquiferNetToGross``
         - ``aquifer_net_to_gross``
         - ``1.0``
         - fraction (-)
     * - ``aquiferPorosity``
         - ``aquifer_porosity``
         - ``0.3``
         - fraction (-)
     * - ``aquiferPermeability``
         - ``aquifer_permeability``
         - ``10000.0``
         - millidarcy (mD)
     * - ``aquiferAnisotropy``
         - ``aquifer_anisotropy``
         - ``4.0``
         - dimensionless (-)
     * - ``salinity``
         - ``salinity``
         - ``10000.0``
         - parts per million (ppm)
     * - ``wellCasingSize``
         - ``well_casing_size``
         - ``13.0``
         - inch
     * - ``wellDistance``
         - ``well_distance``
         - ``150.0``
         - m

The mapper does not add extra branching logic; its specialization is that it always tries to
populate the ATES-specific constructor arguments, even when the ESDL asset omits them.

``aquiferMidTemperature`` is the one property in this set mapped in degrees Celsius. Every other
temperature-like property mapped elsewhere on this page (for example the pipe mapper's
``external_temperature``) uses Kelvin; this is an existing inconsistency in the source data, noted
here for contributor awareness rather than something this page changes.

Heat pump mapper
~~~~~~~~~~~~~~~~

``EsdlAssetHeatPumpMapper`` adds the first substantive construction branch. It checks
``esdl_asset.get_number_of_ports()`` and chooses the returned entity type from that port count:

* ``4`` ports produces a ``HeatPump`` for the water-to-water case.
* ``2`` ports produces an ``AirToWaterHeatPump``.

.. list-table::
     :header-rows: 1

     * - ESDL property
         - Internal field
         - Default
         - Unit
         - Applies to
     * - ``COP``
         - ``coefficient_of_performance``
         - ``HeatPumpDefaults.coefficient_of_performance`` = ``4.0``
         - dimensionless (-)
         - both branches
     * - ``power``
         - ``maximum_electrical_power``
         - ``None``
         - W
         - four-port branch only

Any other port count raises ``NotImplementedError`` with a message that documents the supported
two-port and four-port shapes.

Heat exchanger mapper
~~~~~~~~~~~~~~~~~~~~~

``EsdlAssetHeatExchangerMapper`` reads a single property beyond the shared asset metadata before
constructing a ``HeatExchanger``:

.. list-table::
     :header-rows: 1

     * - ESDL property
         - Internal field
         - Default
         - Unit
     * - ``Efficiency``
         - ``heat_transfer_efficiency``
         - ``HeatExchangerDefaults.heat_transfer_efficiency`` = ``1.0``
         - dimensionless (-)

There is no branching or validation beyond this single fallback lookup.

Ideal heat storage mapper
~~~~~~~~~~~~~~~~~~~~~~~~~

``EsdlIdealHeatStorageMapper`` constructs an ``IdealHeatStorage`` from two defaulted properties and
two port-derived temperatures:

.. list-table::
     :header-rows: 1

     * - ESDL property
         - Internal field
         - Default
         - Unit
     * - ``volume``
         - ``volume``
         - ``HeatBufferDefaults.volume`` = ``1.0``
         - m3
     * - ``fillLevel``
         - ``initial_fill_level``
         - ``HeatBufferDefaults.fill_level`` = ``0.5``
         - fraction, 0-1 (-)
     * - port ``In``/``Supply`` profile
         - ``temperature_in``
         - none; read via ``esdl_asset.get_temperature("In", "Supply")``
         - K
     * - port ``Out``/``Return`` profile
         - ``temperature_out``
         - none; read via ``esdl_asset.get_temperature("Out", "Return")``
         - K

Unlike every other property on this page, the two temperatures have no static default: if the
ESDL port temperature profile does not supply a value, ``get_temperature`` raises rather than
falling back to a constant.

Pipe mapper
~~~~~~~~~~~

``EsdlAssetPipeMapper`` performs the richest property mapping on this page. Its ``to_entity``
method constructs a ``Pipe`` from direct properties, helper-derived values, and multiple
fallbacks:

.. list-table::
     :header-rows: 1

     * - ESDL property
         - Internal field
         - Default
         - Unit
     * - ``length``
         - ``length``
         - ``PIPE_DEFAULTS.length`` = ``1.0``
         - m
     * - ``roughness``
         - ``roughness``
         - ``PIPE_DEFAULTS.roughness`` = ``1e-3``
         - m
     * - ``minor_loss_coefficient``
         - ``minor_loss_coefficient``
         - ``PIPE_DEFAULTS.minor_loss_coefficient`` = ``0.0``
         - dimensionless (-)
     * - ``external_temperature``
         - ``external_temperature``
         - ``PIPE_DEFAULTS.external_temperature`` = ``293.15``
         - K
     * - ``qheat_external``
         - ``qheat_external``
         - ``PIPE_DEFAULTS.qheat_external`` = ``0.0``
         - W

Two further fields are derived rather than read with a single direct default:

* Inner diameter: ``_get_diameter()`` first reads ``innerDiameter`` (m). If that value is
  zero, it tries ``diameter`` as a nominal DN value. When a DN value is available, the mapper
  looks up the corresponding EDR object with the default schedule from ``PIPE_DEFAULTS`` and
  returns its ``innerDiameter`` (m). If neither source is available, it falls back to
  ``PIPE_DEFAULTS.diameter`` = ``1.2`` m.
* Heat-transfer coefficient: ``_get_heat_transfer_coefficient()`` uses
  ``get_thermal_conductivity_table()`` and ``calculate_inverse_heat_transfer_coefficient()`` to
  derive an ``alpha_value`` in W/(m2 K). If no conductivity table can be built, it falls back to
  ``PIPE_DEFAULTS.alpha_value`` = ``0.0``.

This mapper also contains the main failure path in the group. If DN-based diameter lookup requires
EDR access and ``_get_esdl_object_from_edr()`` cannot retrieve the expected object, it raises
``RuntimeError`` rather than silently accepting an invalid diameter.

Related documentation
---------------------

For the broader architecture that instantiates and consumes these factories, see
:doc:`architecture`. For the curated reference index that places this page alongside the other
implementation-oriented architecture pages, see :doc:`../reference/architecture_reference`.