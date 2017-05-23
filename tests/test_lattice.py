#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test lattice.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-23 10:48:04 AM EDT
"""

import unittest
import os

from phantasy import MachinePortal

curdir = os.path.dirname(__file__)

TEST_MACH = 'FRIB_FLAME'


class TestLattice(unittest.TestCase):
    def setUp(self):
        config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(config_dir, TEST_MACH)
        mp = MachinePortal(mpath)
        self.mp = mp
        self.mpath = mpath

    def tearDown(self):
        pass

    def test_get_all_types(self):
        mp = self.mp
        lat = mp.work_lattice_conf
        all_types = [u'BPM', u'HCOR', u'CAV', u'SOL', u'VCOR', u'SEXT',
                     u'BEND', u'QUAD', u'PM']
        self.assertEqual(lat.get_all_types(), all_types)
        self.assertEqual(lat.group.keys(), lat.get_all_types())

    def test_get_all_names(self):
        mp = self.mp
        lat = mp.work_lattice_conf
        names = lat.get_all_names()
        self.assertEqual(names, [e.name for e in lat._elements])

    def test_attributes(self):
        lat = self.mp.work_lattice_conf
        self.assertEqual(lat.mname, TEST_MACH)
        self.assertEqual(lat.mpath, self.mpath)
        self.assertEqual(lat.model, 'FLAME')



