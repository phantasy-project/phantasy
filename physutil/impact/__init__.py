# encoding: UTF-8

"""Utilities for FRIB specific data formats, etc."""

import lattice

def build_lattice(accel, config, settings):

    lattice_factory = lattice.LatticeFactory(accel, config, settings, start="LS1")

    return lattice_factory.build()
