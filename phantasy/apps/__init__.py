# encoding: UTF-8
#
# Copyright (c) 2015-2016 Facility for Rare Isotope Beams
#

"""
Physics Applications
"""

from .latticemodel import lmapp

try:
    from phantasy_apps import *
except ImportError:
    print("Package 'python-phantasy-apps' is required.")
