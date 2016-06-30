# encoding: UTF-8

"""
Physics and High-Level Controls library

.. moduleauthor:: Dylan Maxwell <maxwelld@frib.msu.edu>
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import logging

# Configure the root logger with the default format. This function does
# nothing if the root logger already has handlers configured for it.
logging.basicConfig(format="%(levelname)s: %(asctime)s: %(name)s: %(message)s")
