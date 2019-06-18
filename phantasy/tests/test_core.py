#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import pytest

from phantasy import MachinePortal


curdir = os.path.abspath(os.path.dirname(__file__))
config_dir = os.path.join(curdir, 'config')

TEST_MACH = 'VA_LS1FS1'


@pytest.fixture
def mp_from_config():
    """Return tuple of machine config path and MachinePortal instance.
    machine name: VA_LS1FS1
    """
    mpath = os.path.join(config_dir, TEST_MACH)
    mp = MachinePortal(machine=mpath)
    return mpath, mp


def test_mp_init_with_mpath(mp_from_config):
    mpath, mp = mp_from_config
    assert mp.last_machine_name == TEST_MACH
    assert mp.last_machine_path == os.path.realpath(mpath)
    assert mp.last_lattice_name == 'LINAC'
    assert mp.work_lattice_name == 'LINAC'


def test_mp_load_lattice(mp_from_config):
    mpath, mp = mp_from_config
    assert mp.lattice_names == ['LINAC']

    mp.load_lattice(machine=mpath, segment='LS1')
    assert mp.lattice_names == ['LINAC', 'LS1']
    assert mp.work_lattice_name == 'LS1'
    assert mp.last_lattice_name == 'LS1'

    mp.use_lattice('LINAC')
    assert mp.work_lattice_name == 'LINAC'
    assert mp.last_lattice_name == 'LS1'

    mp.use_lattice('LS1')
    assert mp.work_lattice_name == 'LS1'
    assert mp.last_lattice_name == 'LS1'

    mp.load_lattice(segment='LINAC')
    assert mp.work_lattice_name == 'LINAC'

    mp.reload_lattice(segment='LS1')
    assert mp.work_lattice_name == 'LS1'


def test_get_elements_names_exact(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name

    assert lat_name == 'LINAC'
    assert mp.get_elements(name='NOEXISTS') == []

    all_names = mp.get_all_names()
    for name in all_names:
        assert mp.get_elements(name=name)[0].name == name

    for i in range(10):
        name = list(set([random.choice(all_names) for _ in range(3)]))
        names_get = [e.name for e in mp.get_elements(name=name,
                                                     sort_key='name')]
        assert names_get == sorted(name)


def test_get_elements_types_exact(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'

    assert mp.get_elements(type='NOEXISTS') == []

    assert mp.get_elements(name='*BPM*', sort_key='name') == \
           mp.get_elements(type='BPM', sort_key='name')

    assert mp.get_elements(name=['*BPM*', '*DCH*'], sort_key='name') == \
           mp.get_elements(type=['BPM', 'HCOR'], sort_key='name')


def test_get_elements_types_pattern(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'

    assert mp.get_elements(type=['*PM'], sort_key='pos') == \
           mp.get_elements(name='*PM*', sort_key='pos')


def test_get_elements_srange(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'

    s0, s1 = 10, 20
    line01 = mp.get_elements(srange=(s0, s1))
    assert line01[0].sb >= s0
    assert line01[-1].sb <= s1


def test_get_elements_hybrid(mp_from_config):
    _, mp = mp_from_config
    el1 = mp.get_elements(name=['FS1_B?*D26??', 'LS1_B*DCV*'],
                          type=['BPM', 'QUAD'],
                          srange=(152, 152.5), latname='LINAC')
    el2 = mp.get_elements(name='FS1_BMS:QH_D2645')
    assert el1 == el2


def test_next_elements_count(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'
    lat = mp.work_lattice_conf
    all_e = sorted([e for e in lat if e.virtual == 0], key=lambda e: e.sb)

    ref_elem = all_e[5]
    assert mp.next_elements(ref_elem) == [all_e[6]]
    assert mp.next_elements(ref_elem, count=1) == [all_e[6]]
    assert mp.next_elements(ref_elem, count=-1) == [all_e[4]]
    assert mp.next_elements(ref_elem, count=2) == [all_e[7]]


def test_next_elements_range(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'
    lat = mp.work_lattice_conf
    all_e = sorted([e for e in lat if e.virtual == 0], key=lambda e: e.sb)

    ref_elem = all_e[5]
    assert mp.next_elements(ref_elem, count=2, range='0::1') == \
           all_e[6:8]

    assert mp.next_elements(ref_elem, count=10, range='0:-1:2') == \
           all_e[6:16:2]

    assert mp.next_elements(ref_elem, count=-4, range='0::1') == \
           all_e[4:0:-1][::-1]


def test_next_elements_type(mp_from_config):
    _, mp = mp_from_config
    lat_name = mp.work_lattice_name
    assert lat_name == 'LINAC'
    lat = mp.work_lattice_conf
    all_e = sorted([e for e in lat if e.virtual == 0], key=lambda e: e.sb)

    ref_elem = all_e[5]

    names1 = ['LS1_CA01:CAV2_D1136',
              'LS1_CA01:BPM_D1144',
              'LS1_WA01:BPM_D1155']
    assert mp.next_elements(ref_elem, count=2, type=['BPM'],
                            ref_include=True, range='0::1') == \
           mp.get_elements(name=names1)

    names2 = ['LS1_CA01:CAV3_D1142',
              'LS1_CA01:CAV4_D1150',
              'LS1_WA01:BPM_D1155',
              'LS1_CA01:BPM_D1144']
    # hybrid types
    assert mp.next_elements(ref_elem, count=2, type=['BPM', 'CAV'],
                            range='0::1') == \
           mp.get_elements(name=names2)


def test_inspect_mconf(mp_from_config):
    _, mp = mp_from_config
    mconf = mp.inspect_mconf()
    assert mconf.get('machine') == TEST_MACH
    assert mconf.get('path') == \
           os.path.join(config_dir, TEST_MACH, 'phantasy.ini')
    assert mconf.get('lattices') == ['LINAC', 'LS1', 'FS1']


def test_get_pv_names(mp_from_config):
    _, mp = mp_from_config
    elem = mp.get_elements(type='BPM')
    pv1 = mp.get_pv_names(elem)
    pv_x = [e.pv(field='X', handle='readback')[0] for e in elem]
    pv_y = [e.pv(field='Y', handle='readback')[0] for e in elem]
    assert pv1['X'] == pv_x
    assert pv1['Y'] == pv_y

    e0 = elem[0]
    pv2 = mp.get_pv_names(e0)
    for k, v in pv2.items():
        assert v == e0.pv(field=k, handle='readback')


def test_get_all_types(mp_from_config):
    _, mp = mp_from_config
    all_types = sorted([u'BPM', u'HCOR', u'CAV', u'SOL', u'VCOR', u'SEXT',
                        u'BEND', u'QUAD', u'PM'])
    assert sorted(mp.get_all_types()) == all_types
