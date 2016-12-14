import logging

from .utils import flameutils
from .utils import parseutils
from .utils import miscutils
from .utils import pvutils
from .utils import flowutils
from .apps import ocapp

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

__doc__ = """High-level physics application for FRIB,

:version: %s
:authors: %s

:Example:

>>>
>>>
""" % (__version__, __authors__)

__all__ = [
           'flameutils', 'parseutils', 'miscutils', 'pvutils', 'flowutils',
           'ocapp',
           ]

logging.basicConfig(
        format="%(levelname)s: %(asctime)s: %(name)s: %(message)s"
        )

