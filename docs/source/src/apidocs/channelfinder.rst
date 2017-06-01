.. raw:: latex
    
    \newpage

channelfinder
=============

*import* interface:

.. code-block:: python

    from phantasy import channelfinder

Within the namespace of *channelfinder*, the following could be reached:
``init_db``, ``write_db``, ``write_tb``, ``write_cfs``, ``write_json``,
``write_csv``, ``read_csv``, ``get_data_from_tb``, ``get_data_from_db``,
``get_data_from_cf``, ``CFCDatabase``, ``CFCTable``.

*func_class* may be imported this way, though it is not recommanded:

.. code-block:: python

    from phantasy import <func_class>

or

.. code-block:: python

    from phantasy.library.channelfinder import <func_class>


database module
---------------

.. automodule:: phantasy.library.channelfinder.database
    :members:
    :show-inheritance:

table module
------------

.. automodule:: phantasy.library.channelfinder.table
    :members:
    :show-inheritance:

io module
---------

.. automodule:: phantasy.library.channelfinder.io
    :members:
    :show-inheritance:


