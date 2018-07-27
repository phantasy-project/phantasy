Work with Device
================

This note demonstrates how to get work with the device, the device
usually can be reached by accessing the abstracted Python object,
specifically, the instance of :class:`~phantasy.CaElement`, in which
fundamental APIs are created to make the device operation easy and
functional.

Assuming the following :class:`~phantasy.MachinePortal` instance `mp`
has already been created, otherwise please see :ref:`machine_portal`.

The generic device operation procedure is:

1. Locate the interested device(s) or element(s);
2. Control the device(s) by calling methods or accessing attributes;
3. Post-processing the for other consumers.

Locate Device
-------------

Just as the name implies, `mp` is the entry to all the configurations of
the loaded machine, the following snippet shows how can we locate the
interested device(s). All valid device types can be known by
:meth:`~phantasy.MachinePortal.get_all_types`:

.. ipython:: python
    
    from phantasy import MachinePortal
    mp = MachinePortal(machine="LEBT", segment="LEBT")
    mp.get_all_types()

The method :meth:`~phantasy.MachinePortal.get_elements` is created for
the general purpose of element searching, e.g. all the solenoid could be
located by passing the ``type`` parameter with the value of ``SOL`` (
which is one member of the list returned from `get_all_types()` method),
the returned result is a list, so if the first one is wanted, simply
referring by ``[0]``.

.. ipython:: python

    all_sols = mp.get_elements(type='SOL')
    all_sols
    first_sol = all_sols[0]
    first_sol

Inspect Device
--------------

Each one within the list returned from
:meth:`~phantasy.MachinePortal.get_elements` is the instance of
:class:`~phantasy.CaElement`, which is bundled of various information,
represented as attributes of the Python object [#f1]_, simply by
hitting ``<TAB>`` button after dot (`.`), list of possible methods,
attributes will be pop out, select any of them to get the execution
results.


.. only:: html

  .. rubric:: Footnotes

.. [#f1] The valid common attributes and element specific ones, as well as the valid methods attched to element is detailed in :ref:`this page <arch_element>`.
