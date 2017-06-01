.. _mstates:

General FLAME Machine States
============================

FLAME machine states is the most essential object in modeling an
accelerator. The python interface of ``FLAME`` represents the state 
as ``_internal.State``, could be created by ``allocState()`` method,
however, there are only two methods (``clone()`` and ``show()``) that
exposes explicitly, one of the reasons is that ``_internal.State`` is
designed for not only ``MomentMatrix`` simulation type.

In order to make it more user-friendly, ``MachineStates`` class is
created specifically for the case of ``MomentMatrix`` simulation type,
and exposing as many attributes as possible, since 
*Explicit is better than implicit*.

For a typical ``MachineStates`` object, the following attributes could 
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
    More attributes, that variables could be calculated from ``_internal.State``
    could be added to ``MachineStates`` class.

Create MachineStates object
---------------------------

Basically, there are many ways to initialize the ``MachineStates``, slightly
differences should be aware of.

.. note::
    ``MachineStates`` needs machine information (get from ``machine`` 
    or ``latfile`` keyword parameter) to do further initialization,
    especially for the case of the machine state is composed of zeros.

**Approach 1**

Initialize with defined ``flame._internal.State``:

Fist create machine and state object by FLAME python package:

.. code-block:: python

    >>> from phyapps import flameutils
    >>> from flame import Machine
    >>> 
    >>> latfile = 'test.lat'
    >>> m = Machine(open(latfile, 'r'))
    >>> s = m.allocState({})
    >>> m.propagate(s, 0, 1)

Then, ``MachineStates`` can be created by:

.. code-block:: python

    >>> ms = flameutils.MachineStates(s)

or:

.. code-block:: python

    >>> ms = flameutils.MachineStates()
    >>> ms.mstates = s

Now, one can use ``ms`` object just the same way as ``_internal.State``,
e.g. ``ms`` can be passed as the first argument of ``m`` machine object's
``propagate()`` method; ``ms`` also can duplicated by ``clone()`` method;
and even the represetation of ``ms`` itself is the same like ``s``, i.e.
``print(ms)`` would gives ``State: moment0 mean=[7](-0.0007886,1.08371e-05,0.0133734,6.67853e-06,-0.000184773,0.000309995,1)``


**Approach 2**

Initialize with FLAME machine object, this approach will initialize
a ``MachineStates`` object with the initial attributes' values of
the machine defined ones, e.g.:

.. code-block:: python

    >>> ms = flameutils.MachineStates(machine=m)
    >>> print(ms)
    State: moment0 mean=[7](-0.0007886,1.08371e-05,0.0133734,6.67853e-06,-0.000184773,0.000309995,1)

Also can do by assigning ``latfile`` keyword parameter:

.. code-block:: python
    
    >>> ms = flameutils.MachineStates(latfile=latfile)


**Approach 3**

Initialize with another ``MachineStates`` object, e.g.

.. code-block:: python
    
    >>> ms1 = flameutils.MachineStates(latfile=latfile)
    >>> ms2 = flameutils.MachineStates(mstates=ms1)

.. note::
    ``clone()`` could be used to create a copy, e.g. ``ms2 = ms1.clone()``.


Configure MachineStates object
------------------------------

To confiugre ``MachineStates`` is to set new values to some attributes,
which could be done through properties setter methods, e.g. the initial
kinetic energy of reference charge state can be adjusted by:

.. code-block:: python

    >>> ms.ref_IonEk = 100000

The same rule applies to the scalar properties, however different rule
should be applied when updating array properties, e.g. ``moment0``,
whose value is a numpy array, if even only one element of that array
is to be changed, one should create a new array and assign to ``moment0``,
rather than updating inplace, here is the example:

.. code-block:: python
    
    >>> # before adjustment
    >>> print(ms.moment0)
    array([[ -7.88600000e-04],
           [  1.08371000e-05],
           [  1.33734000e-02],
           [  6.67853000e-06],
           [ -1.84773000e-04],
           [  3.09995000e-04],
           [  1.00000000e+00]])
    >>> # right way to change the first element of moment0
    >>> m0_val = ms.moment0
    >>> m0_val[0] = 0
    >>> ms.moment0 = m0_val
    >>> print(ms.moment0)
    array([[  0.00000000e+00],
           [  1.08371000e-05],
           [  1.33734000e-02],
           [  6.67853000e-06],
           [ -1.84773000e-04],
           [  3.09995000e-04],
           [  1.00000000e+00]])

Use MachineStates object
------------------------

Different ``MachineStates`` represent different initial conditions for
modeling processes, here is the possible cases:

1. Start simulations from different initial kinetic energies

.. literalinclude:: ../../snippets/mf2.py
    :language: python
    :lines: 1-23

Final reference ion kinetic energy v.s. initial input values could be
shown as the following figure:

.. image:: ../../images/scan_refIonEk.png
    :align: center
    :width: 600px

2. to be added.
