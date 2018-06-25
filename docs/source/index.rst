phantasy - Physics High-level Applications and Toolkit for Accelerator System
=============================================================================

.. only:: latex

    .. sidebar:: phantasy Python package
        
        ``phantasy``: Physics High-level Applications aNd Toolkits for Accelerator SYstem

        :Author: Tong Zhang
        :E-mail: zhangt@frib.msu.edu
        :Copyright: 2016-2018, Facility for Rare Isotope Beams, Michigan State University

.. raw:: latex
    
    \newpage

``phantasy`` is the name of a Python package, which is created for the high-level
physics controls on the accelerator facilities. The users (typically are
accelerator physicists, scientists) could build complex higher-level physics
applications based on the high-level physics controls environment that
provided by ``phantasy``, rather than disturbing by the trivial lower-level
controls system. Also, the following highlighted features are included in this
package [#f1]_:

* Device configuration management
* Device abstraction
* Online modeling
* Python interactive scripting environment for high-level controls
* Virtual accelerator based on EPICS control environment
* Web service integration

.. toctree::
    :maxdepth:1
    :caption: Documentation

    src/intro
    src/deploy

.. toctree::
    :maxdepth:1
    :caption: Tutorials

    src/tut
..    src/nb

.. toctree::
    :maxdepth:1
    :caption: API Documentation
    
    src/api
    src/terms

.. only:: html

 PDF documentation: :download:`Download <../build/latex/phantasy.pdf>`


.. only:: html

  .. rubric:: Footnotes

.. [#f1] The feature list may grow or change as the development moving forward.
