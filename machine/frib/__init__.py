# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import xlf

def build_accel(xlfpath, config):
    """
    Convenience method for building ADD from Expanded Lattice File.
    """

    accel_factory = xlf.AccelFactory(xlfpath, config)

    return accel_factory.build()
