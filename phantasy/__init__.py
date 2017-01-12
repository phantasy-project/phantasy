from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import logging

from .apps import lmapp
from .tools import phytool

from phantasy.library.model import flame as flameutils

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

__doc__ = """PHANTASY:
Physics high-level applications and toolkits for accelerator system.

:version: %s
:authors: %s

:Example:

>>>
>>>
""" % (__version__, __authors__)

#__all__ = [
#           'flameutils', 'parseutils', 'miscutils', 'pvutils', 'flowutils',
#           'ocapp',
#           ]

logging.basicConfig(
        format="%(levelname)s: %(asctime)s: %(name)s: %(message)s"
        )
