Getting Started
===============

Here is the simplest way to model a FLAME machine.

.. only:: latex

    .. literalinclude:: ../../snippets/mf1.py
        :language: python
        :emphasize-lines: 9,12,14
        :linenos:

.. only:: html
    
    .. literalinclude:: ../../snippets/mf1.py
        :language: python
        :emphasize-lines: 9,12,14
        :linenos:

The lattice file used here could be found from
:download:`here <../../snippets/test.lat>`.

The 9th line is to create a general FLAME machine states object, which
is a super class of FLAME interal states, one can use this object as
the same API as the FLAME interal states (except ``show()`` method).

The 12th line is to create a ``ModelFlame`` object, after that, ``machine``
and ``mstates`` should be assigned to make it alive. The ``machine`` 
attribute is just the FLAME machine object, ``mstates`` could accept 
both FLAME interal states or ``MachineStates``, for the possible 
user-customized states, the ``MachineStates`` is recommanded to 
including all the operations upon the machine states object.

The advantage of re-invent the new :class:`MachineStates` is to
improve the user experience in the python command line interfaces that
support auto-completion, e.g. ipython, then all properties that 
``MachineStates`` has could be reached by hitting ``<TAB>`` twice; moreover,
additional attributes could be defined in ``MachineStates`` to make the
higher level interface more clear and clean, see details at :ref:`api`
and :ref:`mstates`.

The ``run()`` method of ``ModelFlame`` is used to simulate the model, and
``collect_data()`` could be used to extract the interest data from 
simulation results, then other operations could be done, e.g. data plotting.

.. note::
    Method ``run()`` does not change ``MachineStates`` inplace, 
    instead one can get the updated ``MachineStates`` from the 
    second element of the returned tuple, see 18th line.
