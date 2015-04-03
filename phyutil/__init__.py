# encoding: UTF-8

"""Physics Applications Utility"""

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"

__version__ = "0.0.1"


import logging

# configure the root logger
logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")

import machine
import phylib

__all__ = ['__version__']

__all__.extend(phylib.__all__)
__all__.extend(machine.__all__)