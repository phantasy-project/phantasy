#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test settings.

Tong Zhang <zhangt@frib.msu.edu>
2019-06-18 11:27:15 AM EDT
"""
import os
from phantasy import snp2dict
from phantasy import get_element_settings
from phantasy import generate_settings
from phantasy import MachinePortal
from phantasy import Settings
import pytest

CURDIR = os.path.abspath(os.path.dirname(__file__))
TEST_MACH = "TEST_CA"

DATADIR = os.path.join(CURDIR, 'data')
snpfile = os.path.join(DATADIR, 'sppv.snp')

config_dir = os.path.join(CURDIR, 'config')
mpath = os.path.join(config_dir, TEST_MACH)
mp = MachinePortal(machine=mpath)
lat = mp.work_lattice_conf

@pytest.fixture
def equad_element():
    """Return an EQUAD element.
    """
    elem = mp.get_elements(type='EQUAD')[0]
    return elem

@pytest.fixture
def sol_element():
    """Return a SOL element.
    """
    elem = mp.get_elements(type='SOL')[0]
    return elem

@pytest.fixture
def dict_from_snp():
    return snp2dict(snpfile)


# snp2dict test
def test_snp2dict(dict_from_snp):
    s = dict_from_snp
    assert s['FE_SCS1:PSQ1_D0726:V_CSET'] == '-3072.0'
    assert s['FE_SCS1:PSQ2_D0726:V_CSET'] == '3072.0'


def test_element_get_settings(equad_element, dict_from_snp):
    assert equad_element.get_settings('V', dict_from_snp) == 3072.0


def test_get_element_settings_1(equad_element, dict_from_snp):
    s = dict_from_snp
    assert get_element_settings(s, equad_element) == {
                'V': 3072.0, 'VOLT': 3072.0}


def test_get_element_settings_2(sol_element, dict_from_snp):
    s = dict_from_snp
    assert get_element_settings(s, sol_element) == {'B': 0.1, 'I': 0.1}
    assert get_element_settings(s, sol_element, only_physics=True) == {'B': 0.1}


def test_generate_settings():
    assert generate_settings(snpfile, lat) == dict([
            ('FE_SCS1:SOLR_D0704', {'B': 0.1, 'I': 0.1}),
            ('FE_SCS1:QHE_D0726', {'V': 3072.0, 'VOLT': 3072.0})])
    assert generate_settings(snpfile, lat, only_physics=True) == dict([
            ('FE_SCS1:SOLR_D0704', {'B': 0.1}),
            ('FE_SCS1:QHE_D0726', {'VOLT': 3072.0})])
