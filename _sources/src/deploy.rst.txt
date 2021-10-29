==========
Deployment
==========

Deploy ``phantasy`` to different operating systems is quite simple, both
online and offline approaches are provided. Before installation, there
may be packages/libraries dependency issues to be resolved first.

Prerequisites
-------------

Required Python packages: ``numpy``, ``scipy``, ``matplotlib``,
``cothread``, ``xlrd``,
Optional Python packages: ``tornado``, ``motor``, ``jinja2``,
``humanize``, ``jsonschema``,
Optional Python packages: ``pyCFClient``, ``scanclient``,
Suggested packages: ``phantasy-machines``,
``python-unicorn``, ``unicorn-webapp``,

Other home-made packages:
- Python: ``flame``, ``genopt``
- C++: ``flame``, ``impact`` (FRIB-version), ``dakota-drivers``


Install via APT
---------------

This is the recommended way to deploy ``phantasy``, however, the **APT**
way is **FRIB intranet only**.

The target workstation is running Debian 8, add the
following lines to ``/etc/apt/sources.list`` or save as a separated file
to the directory ``/etc/apt/sources.list.d``:

.. code-block:: bash

    deb http://ci.frib.msu.edu/debian/ jessie unstable
    deb-src http://ci.frib.msu.edu/debian/ jessie unstable

The public key can be imported by [#f1]_:

.. code-block:: bash

    wget http://ci.frib.msu.edu/debian/repo_key.gpg -O - | sudo apt-key add -

After that, in the terminal, issue ``sudo apt-get update`` and
``sudo apt-get install python-phantasy`` to install ``phantasy``, ``apt`` will
handle all the dependencies automatically.

.. For those cannot reach FRIB intranet, the ready-to-install Debian packages
.. can be found at the `following address <https://www.google.com>`_.

FRIB controls network case
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: ../images/packages.png
    :align: center
    :width: 600px


Install via PIP
---------------

Download ``.whl`` package of ``phantasy`` from `HERE <https://stash.frib.msu.edu/projects/PHYAPP/repos/phantasy/browse/dist>`_,
select the newest version, and install it by:

.. code-block:: bash

    pip install <phantasy.VERSION.whl>

Or upgrade from earlier version by:

.. code-block:: bash

    pip install <phantasy.VERSION.whl> --upgrade --no-deps

Or simply install by:

.. code-block:: bash

    pip install phantasy


Run Tests
---------

After installation, executing the command ``test_phantasy`` to run
the tests distributed with ``phantasy`` package.

Alternative way to do in Python terminal:

.. code-block:: python

    >>> from phantasy.tests import main
    >>> main()


.. only:: html

  .. rubric:: Footnotes

.. [#f1] Details see: http://ci.frib.msu.edu/
