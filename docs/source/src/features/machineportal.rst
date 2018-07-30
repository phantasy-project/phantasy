.. _machine_portal:

=======================
Work with MachinePortal
=======================

Set Up Testing Environment
--------------------------

Install Docker
^^^^^^^^^^^^^^
Please ref to https://docs.docker.com/install/ for all platforms.

Start IOC container
^^^^^^^^^^^^^^^^^^^
Start the test IOC by:

.. code-block:: bash

    docker run -d --name phantasy-ioc tonyzhang/phantasy-ioc:jessie

After that, bunch of PVs are alive and ready to control, among which the
PV named ``fac`` could be used to control the random noise level,
set it with ``0`` (``caput fac 0``) will totally disable noise, i.e. all
PVs serve with the constant value (``0.1``).

Physics High-level Controls
---------------------------
Instantiate ``MachinePortal`` class with the machine configuration named
as ``FRIB`` and segment named as ``LEBT``:

.. ipython:: python
    
    # import packages and modules
    from phantasy import MachinePortal

    # create MachinePortal instance
    mp = MachinePortal(machine='FRIB', segment='LEBT')
