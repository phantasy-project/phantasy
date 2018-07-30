#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Element.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-23 10:49:33 AM EDT
"""

import unittest
import os
import json
import time

from phantasy import MachinePortal
from phantasy import CaElement

curdir = os.path.abspath(os.path.dirname(__file__))

TEST_MACH = 'VA_LS1FS1'
TEST_CA = 'TEST_CA'
TEST_CA_1 = 'TEST_CA_1'


class TestElement(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(self.config_dir, TEST_MACH)
        mp = MachinePortal(machine=mpath, segment='LINAC')
        self.mp = mp
        self.machine = mpath

    def tearDown(self):
        pass

    def test_init_with_default(self):
        elem = CaElement()
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, None)
        self.assertEqual(elem.name, None)
        self.assertEqual(elem.index, -1)
        self.assertEqual(elem.length, 0.0)
        self.assertEqual(elem.sb, float('inf'))
        self.assertEqual(elem.se, float('inf'))
        self.assertEqual(elem.virtual, False)
        self.assertEqual(elem.fields, list())
        self.assertEqual(elem.tags, dict())
        self.assertEqual(elem.group, set())

    def test_init_with_data_dict(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_name = pv_record['pv_name']
        pv_props = pv_record['pv_props']
        pv_tags = pv_record['pv_tags']
        elem = CaElement(pv_data=pv_record)
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})
        self.assertEqual(elem.pv(), [pv_name])
        self.assertEqual(elem.tags[pv_name], set(pv_tags))

    def test_init_with_data_list(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_name = pv_record['pv_name']
        pv_props = pv_record['pv_props']
        pv_tags = pv_record['pv_tags']
        elem = CaElement(pv_data=[pv_name, pv_props, pv_tags])
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})
        self.assertEqual(elem.pv(), [pv_name])
        self.assertEqual(elem.tags[pv_name], set(pv_tags))

    def test_init_with_data_props(self):
        with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
            pv_record = json.load(f)
        pv_props = pv_record['pv_props']
        elem = CaElement(**pv_props)
        self.assertEqual(elem.name, pv_props['name'])
        self.assertEqual(elem.index, int(pv_props['index']))
        self.assertEqual(elem.length, float(pv_props['length']))
        self.assertEqual(elem.active, True)
        self.assertEqual(elem.family, pv_props['family'])
        self.assertEqual(elem.sb, float(pv_props['sb']))
        self.assertEqual(elem.se, float(pv_props['se']))
        self.assertEqual(elem.group, {pv_props['family']})


class TestCaElement(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(self.config_dir, TEST_CA)
        mp = MachinePortal(machine=mpath)
        self.mp = mp

    def tearDown(self):
        lat = self.mp.work_lattice_conf
        fld0 = lat[0].get_field('B')
        fld0.reset_policy()
        fld0.set(0.1, 'setpoint')
        fld1 = lat[1].get_field('V')
        fld1.reset_policy()
        fld1.set([-0.1, 0.1], 'setpoint')
        time.sleep(1.5)

    def test_channel_props(self):
        """Set channel properties to elem*"""
        lat = self.mp.work_lattice_conf
        elem0 = lat[0]
        for k in ('name', 'family', 'index', 'se', 'length', 'sb'):
            self.assertEqual(hasattr(elem0, k), True)
        for k in ('phy_type', 'phy_name', 'machine'):
            self.assertEqual(hasattr(elem0, k), False)

    def test_channel_props_1(self):
        """Set channel properties to elem*, physics*"""
        mpath = os.path.join(self.config_dir, TEST_CA_1)
        mp = MachinePortal(mpath)
        lat = mp.work_lattice_conf
        elem0 = lat[0]
        for k in ('name', 'family', 'index', 'se', 'length', 'sb',
                  'phy_type', 'phy_name'):
            self.assertEqual(hasattr(elem0, k), True)
        for k in ('machine',):
            self.assertEqual(hasattr(elem0, k), False)

    def test_channel_ca_1(self):
        """Each CA handle only has one PV"""
        lat = self.mp.work_lattice_conf
        elem = lat[0]
        fld_name = 'B'
        self.assertEqual(len(elem.pv()), 3)
        self.assertEqual(elem.fields, [fld_name])
        self.assertEqual(elem.B, 0.1)
        fld = elem.get_field(fld_name)
        self.assertEqual(fld.get()['mean'], fld.get('readback')['mean'])
        self.assertEqual(fld.get()['mean'], fld.get(timeout=1.0)['mean'])
        self.assertEqual(list(fld.get(timeout=1)['mean']), [fld.value])
        self.assertEqual(fld.value, 0.1)
        elem.B = 0.5
        time.sleep(1.5)
        self.assertEqual(fld.value, 0.5)
        self.assertEqual(list(fld.get(timeout=1)['mean']), [0.5])
        fld.set(0.2, handle='setpoint')
        time.sleep(1.5)
        self.assertEqual(fld.value, 0.2)
        self.assertEqual(elem.B, 0.2)
        elem.B = 0.1
        time.sleep(1.5)

    def test_channel_ca_2(self):
        """Each CA handle has two PVs"""
        lat = self.mp.work_lattice_conf
        elem = lat[1]
        fld_name = 'V'
        self.assertEqual(len(elem.pv()), 6)
        self.assertEqual(elem.fields, [fld_name])
        self.assertEqual(elem.V, 0.1)
        fld = elem.get_field(fld_name)
        self.assertEqual(list(fld.get(timeout=1.0)['mean']),
                         [-fld.value, fld.value])
        self.assertEqual(fld.value, 0.1)
        elem.V = 0.5
        time.sleep(1.5)
        self.assertEqual(fld.value, 0.5)
        self.assertEqual(list(fld.get(timeout=1.0)['mean']), [-0.5, 0.5])
        fld.set(0.2, handle='setpoint')
        time.sleep(1.5)
        self.assertEqual(fld.value, 0.15)
        self.assertEqual(elem.V, 0.15)
        fld.set([0.2, 0.2], handle='setpoint')
        time.sleep(1.5)
        self.assertEqual(fld.value, 0)
        self.assertEqual(elem.V, 0)
        elem.V = 0.1
        time.sleep(1.5)

    def test_read_write_policy(self):
        """Test read & write policy for QHE(+): PSQ1(-), PSQ2(+)"""
        lat = self.mp.work_lattice_conf
        elem = lat[1]
        fld = elem.get_field('V')
        fld.read_policy = lambda x,**kws: (-x[0].value + x[1].value) * 0.5
        fld.write_policy = lambda x,v,**kws: [x[0].put(-v, **kws), x[1].put(v, **kws)]
        elem.V = 0.5
        time.sleep(1.5)
        self.assertEqual(list(fld.get('readback', timeout=1.0)['mean']),
                         [-0.5, 0.5])
        self.assertEqual(list(fld.get('setpoint', timeout=1.0)['mean']),
                         [-0.5, 0.5])
        self.assertEqual(list(fld.get('readset', timeout=1.0)['mean']),
                         [-0.5, 0.5])
        fld.reset_policy('read')
        self.assertEqual(elem.V, 0.5)
        fld.reset_policy('write')
        elem.V = 0.1
        time.sleep(1.5)
        self.assertEqual(fld.value, 0.1)
        self.assertEqual(list(fld.get('readback', timeout=1.0)['mean']),
                         [-fld.value, fld.value])
