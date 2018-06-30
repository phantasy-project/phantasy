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

Install via PIP
---------------

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
