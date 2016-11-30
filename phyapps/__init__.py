import logging

from .utils import flameutils
from .utils import parseutils
from .utils import miscutils
from .utils import pvutils
from .apps import ocapp


__version__ = "0.0.1"
__author__ = "Tong Zhang <zhangt@frib.msu.edu>"

__doc__ = """High-level physics application for FRIB,

:version: %s
:author: %s

:Example:

>>>
>>>
""" % (__version__, __author__)

__all__ = [
           'flameutils', 'parseutils', 'miscutils', 'pvutils', 
           'ocapp',
           ]

logging.basicConfig(
        format="%(levelname)s: %(asctime)s: %(name)s: %(message)s"
        )
