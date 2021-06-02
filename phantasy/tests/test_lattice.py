#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test lattice.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-23 10:48:04 AM EDT
"""

import unittest
import os

from phantasy import MachinePortal
from phantasy import Settings

curdir = os.path.abspath(os.path.dirname(__file__))

TEST_MACH = 'VA_LS1FS1'
TEST_CA = "TEST_CA"
SETTINGS_FILE = os.path.join(curdir, 'config/FRIB_XLF/settings.json')


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
        all_types = sorted([u'BPM', u'HCOR', u'CAV', u'SOL', u'VCOR', u'SEXT',
                            u'BEND', u'QUAD', u'PM'])
        self.assertEqual(sorted(lat.get_all_types()), all_types)
        self.assertEqual(sorted(list(lat.group.keys())),
                         sorted(lat.get_all_types()))

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


class TestLatSettings(unittest.TestCase):
    def setUp(self):
        config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(config_dir, TEST_CA)
        mp = MachinePortal(mpath)
        self.mp = mp

    def test_settings_1(self):
        """test initial settings is None"""
        mp = self.mp
        lat = mp.work_lattice_conf

        for elem in lat:
            self.assertEqual(set(elem.fields).issubset(elem.design_settings), True)
            self.assertEqual(set(elem.fields).issubset(elem.last_settings), True)
            self.assertEqual(set(elem.last_settings).issubset(elem.design_settings), True)

        elem0 = lat[0]
        self.assertEqual(elem0.last_settings['I'], None)
        self.assertEqual(elem0.last_settings['B'], None)
        self.assertEqual(elem0.design_settings['I'], None)
        self.assertEqual(elem0.design_settings['B'], 0.0)

    def test_settings_2(self):
        """test load settings"""
        mp = self.mp
        lat = mp.work_lattice_conf
        elem0 = lat[0]
        elem1 = lat[1]
        settings = Settings(SETTINGS_FILE)

        lat.load_settings(settings, stype='design')
        self.assertEqual(elem0.design_settings, {'I': None, 'B': 0.0})
        self.assertEqual(elem1.design_settings, {'V': None, 'VOLT': 3985.557698574019})

        lat.load_settings(settings, stype='last')
        self.assertEqual(elem0.last_settings, {'I': None, 'B': 0.0})
        self.assertEqual(elem1.last_settings, {'V': None, 'VOLT': 3985.557698574019})
