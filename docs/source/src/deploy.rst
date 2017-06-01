Deployment
==========

Deploy ``phantasy`` to different operating systems is quite simple, both 
online and offline approaches are provided. Before installing this package
into system, there may be packages/libraries dependence issues to be
resolved first (if installing by ``pip install``, dependence issues will be
automatically resolved).

Prerequisites
-------------

Required Python packages: ``numpy``, ``scipy``, ``matplotlib``, ``cothread``,
``xlrd``, ``tornado``, ``motor``, ``jinja2``, ``humanize``, ``jsonschema``.

Other home-made packages:

- Python (cannot resolve by ``pip``): ``flame``, ``genopt`` 
- C++: ``flame``, ``impact`` (FRIB-version), ``dakota-drivers``


Installation
------------

**Offline approach**

Download ``.whl`` package of ``phantasy`` from `HERE <https://stash.frib.msu.edu/projects/PHYAPP/repos/python-phantasy/browse/dist>`_,
select the newest version, and install it by:

.. code-block:: bash
    
    pip install <phantasy.VERSION.whl>

Or upgrade from earlier version by:

.. code-block:: bash
    
    pip install <phantasy.VERSION.whl> --upgrade --no-deps

**Online approach** (FRIB)

For Debian-8 (jessie) OS, ``phantasy`` could be deployed via ``apt install``,
add the following line to file ``/etc/apt/sources.list``:

``deb http://nsclmirror.nscl.msu.edu/controls/debian/ jessie fc1 unstable`` 

issue ``sudo apt update`` and ``sudo apt install python-phantasy`` to install.

See also: http://ci.frib.msu.edu/

*FRIB controls network case:*

.. image:: ../images/packages.png
    :align: center
    :width: 600px
