Modeling Accelerator with Lattice File
======================================

``FLAME`` [#f1]_ is a new envelope tracking code developed by FRIB for the 
purpose of modeling (ion) accelerator efficiently, especially cases
of multi-charge states could be right handled, now it is still under 
development.

``FLAME`` itself has Python interface with the package name of ``flame``.
Another Python package so-called ``flame_utils`` [#f2]_,
which used to be one of
the modules of ``phantasy`` is under developing, not only to make the
``flame`` Python interface more friendly and clear, but also to
better support the entire high-level physics applications,
which is a part of high-level control system.

Getting started
---------------

Here is the simplest way to model an accelerator from FLAME lattice file.

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

The lattice file used here could be downloaded from
:download:`here <../../snippets/test.lat>`.

The 9th line is to create a general FLAME beam state object, which
is a super class of FLAME interal state, one can use this object as
the same API as the FLAME interal state (except ``show()`` method).

The 12th line is to create a ``ModelFlame`` object, after that, ``machine``
and ``bmstate`` should be assigned to make it alive. The ``machine``
attribute is just the FLAME machine object, ``bmstate`` could accept
both FLAME interal state or ``BeamState``, for the possible
user-customized states, the ``BeamState`` is recommanded to
include all the operations upon the machine states object.

The advantage of re-invent the new :class:`BeamState` is to
improve the user experience in the Python CLI environment that
support auto-completion, e.g. `ipython`, then all properties that 
``BeamState`` has could be reached by double hitting ``<TAB>``; moreover,
additional attributes could be defined in ``BeamState`` to make the
higher level interface more clear and clean, see details at :ref:`api`
and :ref:`bmstate`.

The ``run()`` method of ``ModelFlame`` is used to simulate the model, and
``collect_data()`` could be used to extract the data-of-interest from the
simulation results, then other operations could be done, e.g. data plotting.

.. note::
    Method ``run()`` does not change ``BeamState`` inplace, 
    instead one can get the updated ``BeamState`` from the 
    second element of the returned tuple, see 18\ :sup:`th` line.

.. _bmstate:

General FLAME beam state
------------------------

FLAME beam state is the most essential object in modeling an
accelerator. The Python interface of ``FLAME`` represents the state 
as ``_internal.State``, could be created by ``allocState()`` method,
however, there are only two methods (``clone()`` and ``show()``) that
are exposed explicitly, one of the reasons is that ``_internal.State`` is
designed for not only ``MomentMatrix`` simulation type.

In order to make it more user-friendly, ``BeamState`` class is
created specifically for the case of ``MomentMatrix`` simulation type,
and exposing as many attributes as possible, since 
*Explicit is better than implicit* [#f3]_.

For a typical ``BeamState`` object, the following attributes could 
be reached at the moment:

- ``pos``,
- ``ref_beta``, ``ref_bg``, ``ref_gamma``, ``ref_IonEk``, ``ref_IonEs``,
  ``ref_IonQ``, ``ref_IonW``, ``ref_IonZ``, ``ref_phis``,
  ``ref_SampleIonK``,
- ``beta``, ``bg``, ``gamma``, ``IonEk``, ``IonEs``, ``IonQ``, ``IonW``,
  ``IonZ``, ``phis``, ``SampleIonK``,
- ``moment0``, ``moment0_rms``, ``moment0_env``, ``moment1``
- ``x0``, ``xp0``, ``y0``, ``yp0``, ``phi0``, ``dEk0``
- ``x0_env``, ``xp0_env``, ``y0_env``, ``yp0_env``, ``phi0_env``, ``dEk0_env``
- ``x0_rms``, ``xp0_rms``, ``y0_rms``, ``yp0_rms``, ``phi0_rms``, ``dEk0_rms``

.. todo::
    More attributes, that could be calculated from ``_internal.State``
    could be added to ``BeamState`` class.

Create BeamState object
^^^^^^^^^^^^^^^^^^^^^^^

Basically, there are several ways to initialize the ``BeamState``, slight
differences should be aware of.

.. note::
    ``BeamState`` needs FLAME machine information (got from ``machine`` 
    or ``latfile`` keyword parameter) to do further initialization,
    especially, for the case of the beam state is composed of pure zeros.

Approach 1: Initialize with pre-defined ``flame._internal.State`` object
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Fist create machine and state object by FLAME Python package::

    >>> import flame_utils
    >>> from flame import Machine
    >>> 
    >>> latfile = 'test.lat'
    >>> m = Machine(open(latfile, 'rb'))
    >>> s = m.allocState({})
    >>> m.propagate(s, 0, 1)

Then, ``BeamState`` can be created by::

    >>> bs = flame_utils.BeamState(s)

or::

    >>> bs = flame_utils.BeamState()
    >>> bs.state = s

Now, one can use ``bs`` object just the same way as ``_internal.State``,
e.g. ``bs`` can be passed as the first argument of ``m`` machine object's
``propagate()`` method; ``bs`` also can duplicated by ``clone()`` method;
and even the represetation of ``bs`` itself is much similar as ``s``,i.e.
``print(bs)`` would gives ``BeamState: moment0 mean=[7](-0.0007886,1.08371e-05,0.0133734,6.67853e-06,-0.000184773,0.000309995,1)``


Approach 2: Initialize with pre-defined FLAME machine object
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This approach will initialize a ``BeamState`` object with the initial
attributes' values from the pre-defined FLAME machine object, e.g.::

    >>> bs = flame_utils.BeamState(machine=m)
    >>> print(bs)
    BeamState: moment0 mean=[7](-0.0007886,1.08371e-05,0.0133734,6.67853e-06,-0.000184773,0.000309995,1)

Also can do this by assigning ``latfile`` keyword parameter::

    >>> bs = flame_utils.BeamState(latfile=latfile)


Approach 3: Initialize with another ``BeamState`` object
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

For example::

    >>> bs1 = flame_utils.BeamState(latfile=latfile)
    >>> bs2 = flame_utils.BeamState(bmstate=bs1)

.. note::
    ``clone()`` could be used to create a copy, e.g. ``bs2 = bs1.clone()``.


Configure BeamState object
^^^^^^^^^^^^^^^^^^^^^^^^^^

To confiugre ``BeamState`` is to set new values to attributes,
which could be done through properties setter methods, e.g. the initial
kinetic energy of reference charge state can be adjusted by::

    >>> bs.ref_IonEk = 100000

The same rule applies to the scalar properties, however different rule
should be applied when updating array properties, e.g. ``moment0``,
whose value is a numpy array, if even only one element of that array
needs to be changed, one should create a new array and assign to ``moment0``,
rather than updating inplace, here is the example::

    >>> # before adjustment
    >>> print(bs.moment0)
    array([[ -7.88600000e-04],
           [  1.08371000e-05],
           [  1.33734000e-02],
           [  6.67853000e-06],
           [ -1.84773000e-04],
           [  3.09995000e-04],
           [  1.00000000e+00]])
    >>> # right way to change the first element of moment0
    >>> m0_val = bs.moment0
    >>> m0_val[0] = 0
    >>> bs.moment0 = b0_val
    >>> print(bs.moment0)
    array([[  0.00000000e+00],
           [  1.08371000e-05],
           [  1.33734000e-02],
           [  6.67853000e-06],
           [ -1.84773000e-04],
           [  3.09995000e-04],
           [  1.00000000e+00]])

Use BeamState object
^^^^^^^^^^^^^^^^^^^^

Different ``BeamState`` represent different initial conditions for
modeling processes, here are the possible cases:

Scan initial kinetic energy
"""""""""""""""""""""""""""

.. literalinclude:: ../../snippets/mf2.py
    :language: python
    :lines: 1-23

Final reference ion kinetic energy v.s. initial input values could be
shown as the following figure:

.. image:: ../../images/scan_refIonEk.png
    :align: center
    :width: 600px

.. Tip::
    To disable logging messages from ``flame_utils``::
        
        from flame_utils import disable_warnings
        disable_warnings()

    To disable logging messages from ``flame``::
             
        import logging                                     
        logging.getLogger('flame.machine').disabled = True


.. Modeling accelerator with ModelFlame
.. ------------------------------------
.. TBA

.. Data visulization
.. -----------------
.. TBA

.. only:: html

  .. rubric:: Footnotes

.. [#f1] https://github.com/frib-high-level-controls/FLAME
.. [#f2] https://github.com/frib-high-level-controls/flame-utils
.. [#f3] https://www.python.org/dev/peps/pep-0020/
