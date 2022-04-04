# -*- coding: utf-8 -*-

# always use Qt5Agg for mpl < 2.0
import matplotlib
if matplotlib.__version__ < "2.0.0":
    matplotlib.use("Qt5Agg")
#

import logging

logging.getLogger(__name__).setLevel(logging.INFO)
logging.basicConfig(
        format="[%(asctime)s.%(msecs)03d] %(levelname)s: %(name)s: %(message)s",
        datefmt="%H:%M:%S"
)

from phantasy.library import channelfinder
from phantasy.library import lattice
from phantasy.library import layout
from phantasy.library import misc
from phantasy.library import model
from phantasy.library import operation
from phantasy.library import parser
from phantasy.library import physics
from phantasy.library import pv
from phantasy.library import scan
from phantasy.library import settings
from phantasy.library import data

from phantasy.library import *


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2021, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = "2.1.7"

__doc__ = \
"""PHANTASY: [P]hysics [H]igh-level [A]pplications a[N]d [T]oolkit for
[A]ccelerator [SY]stem.

PHANTASY features:

- EPICS-based virtual accelerators system environment
- Online modeling, integrating physics and engineering units scaling laws
- Device abstraction and configuration management
- Interactive Python scripting controls to the accelerator system
- GUI apps for commissioning and operation (see phantasy-apps)

For Debian 8 and 9, meta package: `phantasy' contain all the software
product from this development. Debian 8 support is deprecated.

:version: %s
:authors: %s
""" % (__version__, __authors__)

__all__ = ['MachinePortal']
