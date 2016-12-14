#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unittest for flowutils module.
"""

import unittest
import numpy as np
import os
import random

from phyapps import flowutils

curdir = os.path.dirname(__file__)

class TestMachinePortal(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        mpath = os.path.join(self.config_dir, 'FRIB1')
        mp = flowutils.MachinePortal(facility=mpath)
        self.mp = mp
        self.facility = mpath

    def tearDown(self):
        pass

    #def test_init_with_environpath(self):
    #    val_bak = os.environ.get('PHYUTIL_CONFIG_DIR')
    #    os.environ['PHYUTIL_CONFIG_DIR'] = self.config_dir
    #    mp = flowutils.MachinePortal(facility='FRIB1')
    #    self.assertEqual(mp.last_machine_name, 'FRIB1')
    #    os.environ['PHYUTIL_CONFIG_DIR'] = val_bak

    def test_init_with_machinepath(self):
        mpath = os.path.join(self.config_dir, 'FRIB1')
        mp = flowutils.MachinePortal(facility=mpath)
        self.assertEqual(mp.last_machine_name, 'FRIB1')
        self.assertEqual(mp.last_machine_path, os.path.realpath(mpath))
        self.assertEqual(mp.last_lattice_name, 'LINAC')
        self.assertEqual(mp.work_lattice_name, 'LINAC')

    def test_load_lattice(self):
        mp = self.mp
        self.assertEqual(mp.lattice_names, ['LINAC'])
        mp.load_lattice(facility=self.facility, segment='LS1')
        self.assertEqual(mp.lattice_names, ['LINAC', 'LS1'])
        self.assertEqual(mp.work_lattice_name, 'LS1')
        self.assertEqual(mp.last_lattice_name, 'LS1')

        mp.use_lattice('LINAC')
        self.assertEqual(mp.work_lattice_name, 'LINAC')
        self.assertEqual(mp.last_lattice_name, 'LS1')

        mp.use_lattice('LS1')
        self.assertEqual(mp.work_lattice_name, 'LS1')
        self.assertEqual(mp.last_lattice_name, 'LS1')

        mp.load_lattice(segment='LINAC')
        self.assertEqual(mp.work_lattice_name, 'LINAC')

        mp.reload_lattice(segment='LS1')
        self.assertEqual(mp.work_lattice_name, 'LS1')

    def test_get_elements_names_exact(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        
        self.assertEqual(mp.get_elements(name='NOEXISTS'), [])

        all_names = mp.get_all_names()
        for name in all_names:
            self.assertEqual(mp.get_elements(name=name)[0].name, name)

        for i in range(10):
            name = [random.choice(all_names) for _ in range(3)]
            names_get = [e.name for e in mp.get_elements(name=name,
                                                        sort_key='name')]
            self.assertEqual(names_get, sorted(name))

    def test_get_elements_names_pattern(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')

        p1, p2 = 'FS1_B?*D266?', 'LS1_B*DCV*'
        e1 = [e.name for e in mp.get_elements(name=p1, sort_key='pos')]
        e2 = [e.name for e in mp.get_elements(name=p2, sort_key='pos')]
        n1 = ['FS1_BMS:DCV_D2662', 'FS1_BMS:DCH_D2662',
              'FS1_BMS:BPM_D2664', 'FS1_BMS:QH_D2666']
        n2 = ['LS1_BTS:DCV_D1937', 'LS1_BTS:DCV_D1964',
              'LS1_BTS:DCV_D1997', 'LS1_BTS:DCV_D2024', 
              'LS1_BTS:DCV_D2061', 'LS1_BTS:DCV_D2114']
        self.assertEqual(e1, n1)
        self.assertEqual(e2, n2)

        e12 = [e.name for e in mp.get_elements(name=(p1, p2),
                                                    sort_key='name')]
        n12 = sorted(n1+n2)
        self.assertEqual(e12, n12)

    def test_get_elements_types_exact(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')

        self.assertEqual(mp.get_elements(type='NOEXISTS'), [])

        self.assertEqual(
                mp.get_elements(name='*BPM*', sort_key='name'),
                mp.get_elements(type='BPM', sort_key='name')
                )

        self.assertEqual(
                mp.get_elements(name=['*BPM*', '*DCH*'], sort_key='name'),
                mp.get_elements(type=['BPM', 'HCOR'], sort_key='name')
                )

    def test_get_elements_types_pattern(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')

        self.assertEqual(
                mp.get_elements(type=['*PM'], sort_key='pos'),
                mp.get_elements(name='*PM*', sort_key='pos')
                )

    def test_get_elements_srange(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        lat = mp.work_lattice_conf

        s0, s1 = 10, 20
        line01 = mp.get_elements(srange=(s0, s1))
        self.assertTrue(line01[0].sb >= s0)
        self.assertTrue(line01[-1].sb <= s1)

    def test_get_elements_hybrid(self):
        mp = self.mp
        el1 = mp.get_elements(name=['FS1_B?*D266?', 'LS1_B*DCV*'],
                             type=['BPM','QUAD'], 
                             srange=(154,155), latname='LINAC')
        el2 = mp.get_elements(name='FS1_BMS:QH_D2666')
        self.assertEqual(el1, el2)

    def test_next_elements_count(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        lat = mp.work_lattice_conf
        all_e = sorted([e for e in lat if e.virtual==0], key=lambda e:e.sb)
        
        ref_elem = all_e[5]
        self.assertEqual(mp.next_elements(ref_elem), [all_e[6]])
        self.assertEqual(mp.next_elements(ref_elem, count=1), [all_e[6]])
        self.assertEqual(mp.next_elements(ref_elem, count=-1), [all_e[4]])
        self.assertEqual(mp.next_elements(ref_elem, count=2), [all_e[7]])

    def test_next_elements_range(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        lat = mp.work_lattice_conf
        all_e = sorted([e for e in lat if e.virtual==0], key=lambda e:e.sb)
        
        ref_elem = all_e[5]
        self.assertEqual(
                mp.next_elements(ref_elem, count=2, range='0::1'),
                all_e[6:8]
                )
        self.assertEqual(
                mp.next_elements(ref_elem, count=10, range='0:-1:2'),
                all_e[6:16:2]
                )

        self.assertEqual(
                mp.next_elements(ref_elem, count=-4, range='0::1'),
                all_e[4:0:-1][::-1]
                )

    def test_next_elements_type(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        lat = mp.work_lattice_conf
        all_e = sorted([e for e in lat if e.virtual==0], key=lambda e:e.sb)
        
        ref_elem = all_e[5]

        names1 = ['LS1_CA01:CAV2_D1135',
                  'LS1_CA01:BPM_D1144',
                  'LS1_WA01:BPM_D1155']
        self.assertEqual(
                mp.next_elements(ref_elem, count=2, type=['BPM'],
                                 ref_include=True, range='0::1'),
                mp.get_elements(name=names1)
                )
        names2 = ['LS1_WA01:BPM_D1155',
                  'LS1_CA01:CAV3_D1143',
                  'LS1_CA01:CAV4_D1150',
                  'LS1_CA01:BPM_D1144']
        # hybrid types
        self.assertEqual(
                mp.next_elements(ref_elem, count=2, type=['BPM', 'CAV'],
                                 range='0::1'),
                mp.get_elements(name=names2)
                )

    def test_next_elements_more_types(self):
        mp = self.mp
        lat_name = mp.work_lattice_name
        self.assertEqual(lat_name, 'LINAC')
        lat = mp.work_lattice_conf
        all_e = sorted([e for e in lat if e.virtual==0], key=lambda e:e.sb)
        
        ref_elem = all_e[5]
 

    
        



