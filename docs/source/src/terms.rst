Glossary
========

:machine:
    Accelerator facility, defined by a string name, should have configuration
    files (usually hosted in a folder with machine name as folder name) to
    describe how the machine is structured, including EPICS control related
    data source, lattice generation rules, etc.

:segment:
    Part of machine, a collection of sequential devices, could be represented
    as lattice file if written into file for simulations.

:lattice:
    Lattice file for simulation, e.g. FLAME lattice ,IMPACT lattice.

:layout:
    Geometry-related description of the machine/segment devices arrangement.

:settings:
    Setup of devices.

:high-level lattice:
    Instantiated from ``phantasy.lattice.Lattice``, which will created a
    ``Lattice`` object to represent the real accelerator based on the machine
    configurations. Concreted devices will be established as high-level
    elements that allow users to manipulate interactively.
    High-level lattice is managed by ``phantasy.MachinePortal`` instance,
    model-based machine tunning and online tunning approaches are supported
    for specific high-level lattice.

:viewer element:
    Element type or family is one of the following: ``BPM``, ``PM``, etc.,
    which could only be used as readonly devices for diagnostics.

