import logging

#
from phantasy.library.model import flame as flameutils

#
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


#
__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = "0.6.6"

__doc__ = \
"""PHANTASY: [P]hysics [H]igh-level [A]pplications a[N]d [T]oolkits for
[A]ccelerator [SY]stem.

Main features of ``phantasy``:

- Creating virtual accelerators, EPICS controls environment;
- Modeling and tuning accelerator on high-level computing stage;
- General interface for physics applications;

Physics applications built on top of ``phantasy`` are developed as another
repo: ``phantasy-apps``, whose names in Debian repo are prefixed with
``python-``, i.e. ``python-phantasy`` and ``python-phantasy-apps``.

More details see documentation at https://controls.frib.msu.edu/phantasy/.

:version: %s
:authors: %s
""" % (__version__, __authors__)

__all__ = ['flameutils', 'MachinePortal']

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")
