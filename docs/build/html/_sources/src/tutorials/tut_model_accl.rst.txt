=============================
Modeling Accelerator Facility
=============================

One of the key features of ``phantasy`` is to abstract the accelerator
devices into hierarchical structure, which opens the portal for the
high-level object-oriented controls way, and based on which, modularized
high-level controls software could be developed.

Configuration Files
-------------------

Currently, ``phantasy`` uses (at most) seven (7) types of configuration
files to describe the entire accelerator, including device abstraction,
online-modeling, controls PV management, etc., among which, the
file to integrate the EPICS channels or PV names with accelerator layout
is very important. The full list of configuration file types are:

+----------------------------+------------------+-------------------------------------------------------+
| Type Name                  | File name [#f1]_ | Description                                           |
+============================+==================+=======================================================+
| Machine configuration      | phantasy.ini     | Global configuration for loading specific machine     |
+----------------------------+------------------+-------------------------------------------------------+
| Device/Model configuration | phantasy.cfg     | Configuration for physics models and devices          |
+----------------------------+------------------+-------------------------------------------------------+
| Channels configuration     | channels.csv     | Includes EPICS PV names and device properties         |
+----------------------------+------------------+-------------------------------------------------------+
| Layout configuration       | layout.csv       | Devices geometrical layout configuration              |
+----------------------------+------------------+-------------------------------------------------------+
| Settings configuration     | settings.csv     | Initial settings for physics models                   |
+----------------------------+------------------+-------------------------------------------------------+
| Unit scaling configuration | unicorn.xlsx     | Scaling laws for physics/engineering units conversion |
+----------------------------+------------------+-------------------------------------------------------+

Machine configuration
^^^^^^^^^^^^^^^^^^^^^

Machine configuration file (typical name: *phantasy.ini*) is the main file that
used by ``phantasy`` ``MachinePortal`` class to instantiate the seleted accelerator
and specific segment, which is ``machine`` and ``segment`` parameter of
``MachinePortal`` initialization method, respectively.

Channels configuration
^^^^^^^^^^^^^^^^^^^^^^
Generally, each device can have one or more than one PV names, which depends on
the number of fields to be controlled, please note for this high-level physics
controls framework, the only interested fields are physics related, e.g.
one solenoid usually only has one field to control (read and write), that is
the current applied on the device, while the RF cavity should have both phase
and amplitude of electric field to control. In this configuration file, all
these information should be included, togther with other general meta-information
as device position, length, type, etc.

Simple Example
--------------

Here is a simple example of *channels.csv* (:download:`HERE <simple_machine/channels.csv>`)
to describe the PV names in a
machine named *simple_machine*, of segment name *TEST*:

.. csv-table:: Table Title
   :file: simple_machine/channels.csv
   :header-rows: 1

While the machine configuration for this example is:

.. literalinclude:: simple_machine/phantasy.ini


The typical snippet to abstract the whole segment could be:

.. code-block:: python
    
    >>> from phantasy import MachinePortal
    >>> mp = MachinePortal(machine='simple_machine', segment='TEST')
    >>> lat = mp.work_lattice_conf
    >>> for e in lat:
    >>>     print(e)
    0001 | FE_SCS1:SOLR_D0704   SOL       0.00  [m] 0.399800 [m]
    0002 | FE_SCS1:QHE_D0726    EQUAD     2.32  [m] 0.205200 [m]


All the devices could be reached via `mp.work_lattice_conf`.


.. Building high-level lattices
.. ----------------------------

.. Model-based machine tunning
.. ---------------------------

.. Online machine tunning
.. ----------------------


.. only:: html

  .. rubric:: Footnotes

.. [#f1] Typical file names used by *phantasy-machines* package, see `here <https://stash.frib.msu.edu/projects/PHYAPP/repos/phantasy-machines/browse>`_ for the details of each file.
