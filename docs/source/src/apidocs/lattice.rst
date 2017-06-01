.. raw:: latex
    
    \newpage

lattice
=======

*import* interface:

.. code-block:: python

    from phantasy import lattice

Within the namespace of *lattice*, the following could be reached:
``build_flame_lattice``, ``build_impact_lattice``, ``read_impact_lattice``,
``run_impact_lattice``, ``AbstractElement``, ``CaElement``, ``FlameLattice``,
``FlameLatticeFactory``, ``ImpactLattice``, ``ImpactLatticeElement``,
``ImpactLatticeFactory``, ``ImpactLatticeField``, ``Lattice``.

*func_class* may be imported this way, though it is not recommanded:

.. code-block:: python

    from phantasy import <func_class>

or

.. code-block:: python

    from phantasy.library.lattice import <func_class>


element module
--------------

.. automodule:: phantasy.library.lattice.element
    :members:
    :show-inheritance:

flame module
------------

.. automodule:: phantasy.library.lattice.flame
    :members:
    :show-inheritance:

impact module
-------------

.. automodule:: phantasy.library.lattice.impact
    :members:
    :show-inheritance:

lattice module
--------------

.. automodule:: phantasy.library.lattice.lattice
    :members:
    :show-inheritance:
