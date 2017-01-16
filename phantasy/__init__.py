from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import logging

from .apps import lmapp
from .tools import phytool

from phantasy.library.model import flame as flameutils
from phantasy.library.operation import MachinePortal

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

__doc__ = """PHANTASY:
Physics high-level applications and toolkits for accelerator system.

:version: %s
:authors: %s
""" % (__version__, __authors__)

__all__ = ['flameutils', 'MachinePortal']

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")
