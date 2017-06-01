.. raw:: latex
    
    \newpage

pv
==

*import* interface:

.. code-block:: python

    from phantasy import pv

Within the namespace of *pv*, the following could be reached:
``caget``, ``caput``, ``camonitor``, ``cainfo``, ``connect``,
``get_readback``, ``dump_data``, ``Popen``, ``CABatch``, ``DataSource``.

*func_class* may be imported this way, though it is not recommanded:

.. code-block:: python

    from phantasy import <func_class>

or

.. code-block:: python

    from phantasy.library.pv import <func_class>


datasource module
-----------------

.. automodule:: phantasy.library.pv.datasource
    :members:
    :show-inheritance:

