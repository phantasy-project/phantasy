PHANTASY
========

Physics High-level Applications and Toolkit for Accelerator SYstem.

Main features of ``phantasy``:

- Creating virtual accelerators, EPICS controls environment;
- Modeling and tuning accelerator on high-level computing stage;
- General interface for physics applications;

Physics applications built on top of ``phantasy`` are developed as another
repo: ``phantasy-apps``, whose names in Debian repo are prefixed with
``python-``, i.e. ``python-phantasy`` and ``python-phantasy-apps``.

``phantasy`` was originally refactored from two repos: ``phyapps`` and ``phyhlc``
since the mid December of 2016, the major changes are:

- Create a new name for this project;
- Refactor software framework;
- Redesigned physics application framework;
- Get rid of global variables;
- Rebuild API systematically;
- Follow PEP-8 coding rules;
- Follow Numpy-style docstring rules;
- Add docs and examples;
- Add packages/modules upon this new framework;
- Add unittests;
- Test and deploy with CI.

More details see documentation at https://archman.github.io/phantasy/
