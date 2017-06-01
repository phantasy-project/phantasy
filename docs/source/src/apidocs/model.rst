.. raw:: latex
    
    \newpage

model
=====

*import* interface:

.. code-block:: python

    from phantasy import model

Within the namespace of *model*, the following could be reached:
``collect_data``, ``configure``, ``convert_results``, ``generate_latfile``,
``get_all_names``, ``get_all_types``, ``get_element``, ``get_index_by_name``,
``get_index_by_type``, ``get_names_by_pattern``, ``inspect_lattice``,
``propagate``, ``MachineStates``, ``Model``, ``ModelFlame``.

*func_class* may be imported this way, though it is not recommanded:

.. code-block:: python

    from phantasy import <func_class>

or

.. code-block:: python

    from phantasy.library.model import <func_class>


flame module
------------

.. automodule:: phantasy.library.model.flame
    :members:
    :show-inheritance:

