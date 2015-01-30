# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import xlf

from config import Configuration

def build_accel(xlfpath, confpath=None, config=None):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """
    
    if config == None:
        config = Configuration.read(confpath)     

    config = Configuration.read(confpath)

    accel_factory = xlf.AccelFactory(xlfpath, config=config)

    return accel_factory.build()
