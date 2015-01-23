# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import xlf

def read_xlf(xlfpath, cdfpath):
    """
    Convenience method for reading FRIB Expanded Lattice File.
    """
    return xlf.read_add(xlfpath, cdfpath)
