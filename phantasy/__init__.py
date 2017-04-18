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
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = "0.2.2"

__doc__ = """PHANTASY:
Physics high-level applications and toolkits for accelerator system.

:version: %s
:authors: %s
""" % (__version__, __authors__)

__all__ = ['flameutils', 'MachinePortal']

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")
