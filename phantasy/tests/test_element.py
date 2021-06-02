#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test Element.

Tong Zhang <zhangt@frib.msu.edu>
2017-05-23 10:49:33 AM EDT
"""

import json
import os
import pytest
import time

from phantasy import CaElement
from phantasy import MachinePortal


curdir = os.path.abspath(os.path.dirname(__file__))

TEST_CA = 'TEST_CA'
TEST_CA_1 = 'TEST_CA_1'


@pytest.fixture
def default_element():
    """Return CaElement instance with empty params.
    """
    return CaElement()


@pytest.fixture
def pv_data_from_json():
    """Return tuple of PV data from json file,
    pv_record, pv_name, pv_props and pv_tags.
    """
    with open(os.path.join(curdir, 'data/pv_record.json'), 'r') as f:
        pv_record = json.load(f)
    pv_name = pv_record['pv_name']
    pv_props = pv_record['pv_props']
    pv_tags = pv_record['pv_tags']

    return pv_record, pv_name, pv_props, pv_tags


def test_element_init_with_default(default_element):
    elem = default_element
    assert elem.active == True
    assert elem.family == None
    assert elem.name == None
    assert elem.index == -1
    assert elem.length == 0.0
    assert elem.sb == float('inf')
    assert elem.se == float('inf')
    assert elem.virtual == False
    assert elem.fields == list()
    assert elem.tags == dict()
    assert elem.group == set()


def test_element_init_with_data_dict(pv_data_from_json):
    pv_record, pv_name, pv_props, pv_tags = pv_data_from_json
    elem = CaElement(pv_data=pv_record)

    assert elem.name == pv_props['name']
    assert elem.index == int(pv_props['index'])
    assert elem.length == float(pv_props['length'])
    assert elem.active == True
    assert elem.family == pv_props['family']
    assert elem.sb == float(pv_props['sb'])
    assert elem.se == float(pv_props['se'])
    assert elem.group == {pv_props['family']}
    assert elem.pv() == [pv_name]
    assert elem.tags[pv_name] == set(pv_tags)


def test_element_init_with_data_list(pv_data_from_json):
    _, pv_name, pv_props, pv_tags = pv_data_from_json
    elem = CaElement(pv_data=[pv_name, pv_props, pv_tags])

    assert elem.name == pv_props['name']
    assert elem.index == int(pv_props['index'])
    assert elem.length == float(pv_props['length'])
    assert elem.active == True
    assert elem.family == pv_props['family']
    assert elem.sb == float(pv_props['sb'])
    assert elem.se == float(pv_props['se'])
    assert elem.group == {pv_props['family']}
    assert elem.pv() == [pv_name]
    assert elem.tags[pv_name] == set(pv_tags)


def test_element_init_with_data_props(pv_data_from_json):
    _, _, pv_props, _ = pv_data_from_json
    elem = CaElement(**pv_props)

    assert elem.name == pv_props['name']
    assert elem.index == int(pv_props['index'])
    assert elem.length == float(pv_props['length'])
    assert elem.active == True
    assert elem.family == pv_props['family']
    assert elem.sb == float(pv_props['sb'])
    assert elem.se == float(pv_props['se'])
    assert elem.group == {pv_props['family']}


@pytest.fixture
def mp_from_config2():
    """Return tuple of machine config path and MachinePortal instance.
    machine name: TEST_CA
    """
    config_dir = os.path.join(curdir, 'config')
    mpath = os.path.join(config_dir, 'TEST_CA')
    mp = MachinePortal(machine=mpath)
    yield (mpath, mp)

    lat = mp.work_lattice_conf
    fld0 = lat[0].get_field('B')
    fld0.reset_policy()
    fld0.set(0.1, 'setpoint')
    fld1 = lat[1].get_field('V')
    fld1.reset_policy()
    fld1.set([-0.1, 0.1], 'setpoint')
    time.sleep(1.5)


@pytest.fixture
def mp_from_config3():
    """Return tuple of machine config path and MachinePortal instance.
    machine name: TEST_CA_1
    """
    config_dir = os.path.join(curdir, 'config')
    mpath = os.path.join(config_dir, 'TEST_CA_1')
    mp = MachinePortal(machine=mpath)
    return (mpath, mp)


def test_element_channel_props(mp_from_config2):
    """Set channel properties to elem*"""
    _, mp = mp_from_config2
    lat = mp.work_lattice_conf
    elem0 = lat[0]
    for k in ('name', 'family', 'index', 'se', 'length', 'sb'):
        assert hasattr(elem0, k) == True
    for k in ('phy_type', 'phy_name', 'machine'):
        assert hasattr(elem0, k) == False


def test_element_channel_props_1(mp_from_config3):
    """Set channel properties to elem*, physics*"""
    mpath, mp = mp_from_config3
    lat = mp.work_lattice_conf
    elem0 = lat[0]
    for k in ('name', 'family', 'index', 'se', 'length', 'sb',
              'phy_type', 'phy_name'):
        assert hasattr(elem0, k) == True
    for k in ('machine',):
        assert hasattr(elem0, k) == False


def test_element_channel_ca_1(mp_from_config2):
    """Each CA handle only has one PV"""
    _, mp = mp_from_config2
    lat = mp.work_lattice_conf
    elem = lat[0]
    fld_name = 'B'

    assert len(elem.pv()) == 6
    assert elem.fields == ['I', 'B']
    assert elem.B == 0.1

    fld = elem.get_field(fld_name)
    assert fld.get(timeout=2)['mean'] == fld.get('readback', timeout=2)['mean']
    assert fld.get(timeout=2)['mean'] == fld.get(timeout=1.0)['mean']
    assert list(fld.get(timeout=1)['mean']) == [fld.value]
    assert fld.value == 0.1

    elem.B = 0.5
    time.sleep(1.5)
    assert fld.value == 0.5
    assert list(fld.get(timeout=1)['mean']) == [0.5]

    fld.set(0.2, handle='setpoint')
    time.sleep(1.5)
    assert fld.value == 0.2
    assert elem.B == 0.2

    elem.B = 0.1
    time.sleep(1.5)


def test_element_channel_ca_2(mp_from_config2):
    """Each CA handle has two PVs"""
    _, mp = mp_from_config2
    lat = mp.work_lattice_conf
    elem = lat[1]
    fld_name = 'V'
    assert len(elem.pv()) == 12
    assert elem.fields == ['V', 'VOLT']
    assert elem.V == 0.1
    fld = elem.get_field(fld_name)
    assert list(fld.get(timeout=1.0)['mean']) == [-fld.value, fld.value]
    assert fld.value == 0.1

    elem.V = 0.5
    time.sleep(1.5)
    assert fld.value == 0.5
    assert list(fld.get(timeout=1.0)['mean']) == [-0.5, 0.5]

    fld.set(0.2, handle='setpoint')
    time.sleep(1.5)
    assert fld.value == 0.15
    assert elem.V == 0.15

    fld.set([0.2, 0.2], handle='setpoint')
    time.sleep(1.5)
    assert fld.value == 0
    assert elem.V == 0

    elem.V = 0.1
    time.sleep(1.5)


def test_read_write_policy(mp_from_config2):
    """Test read & write policy for QHE(+): PSQ1(-), PSQ2(+)"""
    _, mp = mp_from_config2
    lat = mp.work_lattice_conf
    elem = lat[1]
    fld = elem.get_field('V')

    fld.read_policy = lambda x,**kws: (-x[0].value * 1.1 + x[1].value * 0.8) * 0.5
    fld.write_policy = lambda x,v,**kws: [x[0].put(-v, **kws), x[1].put(v, **kws)]

    elem.V = 0.5
    time.sleep(1.5)

    assert list(fld.get('readback', timeout=1.0)['mean']) == [-0.5, 0.5]
    assert list(fld.get('setpoint', timeout=1.0)['mean']) == [-0.5, 0.5]
    assert list(fld.get('readset', timeout=1.0)['mean']) == [-0.5, 0.5]
    assert elem.V == pytest.approx(0.5 * 1.9 * 0.5)

    fld.reset_policy('read')
    assert elem.V == 0.5

    fld.reset_policy('write')
    elem.V = 0.1
    time.sleep(1.5)

    assert fld.value == 0.1
    assert list(fld.get('readback', timeout=1.0)['mean']) == [-fld.value, fld.value]
