# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import lattice

def build_lattice(accel, confpath=None, setpath=None, config=None, settings=None):

    lat_factory = lattice.LatticeFactory()



    return lat_factory.build()