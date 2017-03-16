#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unittest for flameutils module.
"""

import unittest
import numpy as np
from phantasy.library.model import flame as flameutils
from flame import Machine
import os
from cStringIO import StringIO
import random

#from nose.tools import nottest

curdir = os.path.dirname(__file__)

FLAME_DATA = os.path.join(curdir, "lattice/flame_data")


def make_latfile(latfile1):
    f1 = latfile1
    f1_pathname = os.path.dirname(f1)
    f1_filename = os.path.basename(f1)
    f2_filename = f1_filename.replace('0', '1')
    f2_pathname = f1_pathname
    f2 = os.path.join(f2_pathname, f2_filename)
    fp2 = open(f2, 'w')
    for line in open(f1, 'r'):
        if line.startswith('Eng'):
            name, _ = line.split('=')
            line = '{0} = "{1}";\n'.format(name.strip(),
                                           os.path.abspath(FLAME_DATA))
        fp2.write(line)
    fp2.close()
    return f2


class TestGenerateLatfile(unittest.TestCase):
    def setUp(self):
        testfile = os.path.join(curdir, 'lattice/test_0.lat')
        out1file = os.path.join(curdir, 'lattice/out1_0.lat')
        out2file = os.path.join(curdir, 'lattice/out2_0.lat')
        self.testfile = make_latfile(testfile)
        self.out1file = make_latfile(out1file)
        self.out2file = make_latfile(out2file)

        ftest = open(self.testfile)
        self.m = Machine(ftest)
        s0 = self.m.allocState({})
        self.r = self.m.propagate(s0, 0, len(self.m), range(len(self.m)))
        self.s = s0
        k = ['beta', 'bg', 'gamma', 'IonEk', 'IonEs', 'IonQ', 'IonW', 
             'IonZ', 'phis', 'SampleIonK']
        self.keys = [i for i in k]
        self.ref_keys = ['ref_{}'.format(i) for i in k] + ['pos']
        self.keys_ps = ['moment0', 'moment0_env', 'moment0_rms', 'moment1']

        self.fout1_str = open(self.out1file).read().strip()
        self.fout2_str = open(self.out2file).read().strip()

        self.latfile1 = os.path.join(curdir, 'lattice/out1_org.lat')
        self.latfile2 = os.path.join(curdir, 'lattice/out1_mod.lat')

    def tearDown(self):
        for f in [self.latfile1, self.latfile2]:
            if os.path.isfile(f):
                os.remove(f)

    def test_generate_latfile_original1(self):
        sio = StringIO()
        sioname = flameutils.generate_latfile(self.m, out=sio)
        self.assertEqual(sioname, 'string')
        self.assertEqual(sio.getvalue().strip(), self.fout1_str)
        
    def test_generate_latfile_original2(self):
        # TEST LATFILE
        fout1_file = flameutils.generate_latfile(self.m, self.latfile1)
        lines1 = [line.strip() for line in open(fout1_file).read().strip().split('\n')]
        lines0 = [line.strip() for line in self.fout1_str.split('\n')]
        self.assertEqual(lines1, lines0)
        
        m = Machine(open(fout1_file))
        s = m.allocState({})
        r = m.propagate(s, 0, len(m), range(len(m)))
        
        # TEST RESULTS
        for i in range(len(m)):
            s1, s0 = r[i][1], self.r[i][1]
            for k in self.ref_keys:
                self.assertEqual(getattr(s1, k), getattr(s0, k))

            for k in self.keys:
                self.assertEqual(getattr(s1, k).tolist(), 
                                 getattr(s0, k).tolist())

            for k in self.keys_ps:
                self.assertEqual(getattr(s1, k).tolist(), 
                                 getattr(s0, k).tolist())
    
    def test_generate_latfile_update(self):
        idx = 80
        self.m.reconfigure(idx, {'theta_x': 0.1})
        fout2_file = flameutils.generate_latfile(self.m, self.latfile2)
        self.assertEqual(open(fout2_file).read().strip(), self.fout2_str)
        
        m = Machine(open(fout2_file))
        self.assertEqual(m.conf(idx)['theta_x'], 0.1)


class TestModelFlame(unittest.TestCase):
    def setUp(self):
        testfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.testfile = make_latfile(testfile)
        self.fm = flameutils.ModelFlame(self.testfile)

    def test_set_latfile(self):
        fm_none = flameutils.ModelFlame()
        self.assertIsNone(fm_none.latfile)
        fm_none.latfile = self.testfile
        self.assertEqual(fm_none.latfile, self.testfile)

    def test_set_machine(self):
        fm_none = flameutils.ModelFlame()
        self.assertIsNone(fm_none.machine)
        m = Machine(open(self.testfile, 'r'))
        fm_none.machine = m
        self.assertEqual(fm_none.machine, m)

    def test_set_mstates(self):
        fm_none = flameutils.ModelFlame()
        self.assertIsNone(fm_none.mstates)
        m = Machine(open(self.testfile, 'r'))
        s = m.allocState({})
        m.propagate(s, 0, 1)
        fm_none.mstates = s
        self.assertEqual(fm_none.mstates, s)

    def test_init_machine(self):
        fm_none = flameutils.ModelFlame()
        m, s = fm_none.init_machine(self.testfile)
        fm_none.machine, fm_none.mstates = m, s
        self.assertEqual(fm_none.machine, m)
        self.assertEqual(fm_none.mstates, s)

    def test_get_all_types(self):
        fm = flameutils.ModelFlame(self.testfile)
        etypes = ['quadrupole', 'bpm', 'drift', 'source', 'rfcavity',
                  'sbend', 'orbtrim', 'solenoid', 'stripper']
        self.assertEqual(fm.get_all_types(), etypes)
    
    def test_get_index_by_name(self):
        fm = flameutils.ModelFlame(self.testfile)
        m = fm.machine
        all_names = fm.get_all_names()
        for n in range(2, 20):
            enames = [random.choice(all_names) for _ in range(n)]
            e = fm.get_index_by_name(name=enames)
            e0 = {n: m.find(name=n) for n in enames}
            self.assertEqual(e, e0)

    def test_get_index_by_type(self):
        fm = flameutils.ModelFlame(self.testfile)
        m = fm.machine
        all_types = fm.get_all_types()
        for n in range(2, len(all_types)):
            etyps = [random.choice(all_types) for _ in range(n)]
            e = fm.get_index_by_type(type=etyps)
            e0 = {t: m.find(type=t) for t in etyps}
            self.assertEqual(e, e0)

    def test_run_1(self):
        """ test_run_1: propagate from the first to last, monitor None
        """ 
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        m0.propagate(s0, 0, -1)
        fm = flameutils.ModelFlame(latfile)
        r,s = fm.run()
        self.assertEqual(r, [])
        self.iter_all_attrs(s, s0)

    def test_run_2(self):
        """ test_run_2: propagate from the first to last, monitor all BPMs
        """
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        fm = flameutils.ModelFlame(latfile)
        obs = fm.get_index_by_type(type='bpm')['bpm']
        r0 = m0.propagate(s0, 0, -1, observe=obs)
        r,s = fm.run(monitor=obs)
        rs0 = [ts for (ti,ts) in r0] 
        rs = [ts for (ti,ts) in r] 
        for (is1, is2) in zip(rs0, rs):
            self.iter_all_attrs(is1, is2)
        self.iter_all_attrs(s, s0)

    def test_run_3(self):
        """ test run_3: test initial states
        """
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        m0.propagate(s0, 0, 1)
        fm = flameutils.ModelFlame(latfile)
        r, s = fm.run(from_element=0, to_element=0)
        self.iter_all_attrs(s0, s)

    def test_run_4(self):
        """ test_run_4: run and monitor from element index of 10 to 20
        """
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        m0.propagate(s0, 0, 1)
        r0 = m0.propagate(s0, 10, 11, observe=range(10, 21))

        fm = flameutils.ModelFlame(latfile)
        r, s = fm.run(from_element=10, to_element=20, monitor=range(10,21))
        self.iter_all_attrs(s0, s)
        rs0 = [ts for (ti,ts) in r0] 
        rs = [ts for (ti,ts) in r] 
        for (is1, is2) in zip(rs0, rs):
            self.iter_all_attrs(is1, is2)

    def test_run_5(self):
        """ test_run_5: using MachineStates object
        """
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        ms = flameutils.MachineStates(machine=m0) 

        fm = flameutils.ModelFlame()
        fm.mstates = ms
        fm.machine = m0
        obs = fm.get_index_by_type(type='bpm')['bpm']
        r,s = fm.run(monitor=obs)

        s0 = m0.allocState({})
        m0.propagate(s0, 0, 1)
        r0 = m0.propagate(s0, 1, -1, observe=obs)
        rs0 = [ts for (ti,ts) in r0] 
        rs = [ts for (ti,ts) in r] 
        for (is1, is2) in zip(rs0, rs):
            self.iter_all_attrs(is1, is2)
        self.iter_all_attrs(s, s0)

    def test_collect_data(self):
        """ test_collect_data: get pos, x0, IonEk
        """
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        r0 = m0.propagate(s0, 0, 100, observe=range(100))

        data0 = flameutils.collect_data(r0, pos=True, x0=True, IonEk=True)

        fm = flameutils.ModelFlame(latfile)
        r, s = fm.run(from_element=1, to_element=99, monitor=range(100))
        data = fm.collect_data(r, pos=True, x0=True, IonEk=True)

        self.assertEqual(data0['pos'][1:].tolist(), data['pos'].tolist())
        self.assertEqual(data0['x0'][1:].tolist(), data['x0'].tolist())
        self.assertEqual(data0['IonEk'][1:].tolist(), data['IonEk'].tolist())
 
    def iter_all_attrs(self, ms, s):
        k = ['beta', 'bg', 'gamma', 'IonEk', 'IonEs', 'IonQ', 'IonW', 
             'IonZ', 'phis', 'SampleIonK']
        all_keys = [i for i in k]
        all_keys.extend(['ref_{}'.format(i) for i in k] + ['pos'])
        all_keys.extend(['moment0', 'moment0_env', 'moment0_rms', 'moment1'])
        for attr in all_keys:
            left_val, right_val = getattr(ms, attr), getattr(s, attr)
            if isinstance(left_val, np.ndarray):
                #self.assertTrue((np.allclose(left_val, right_val, equal_nan=True) | (np.isnan(left_val) & np.isnan(right_val))).all())
                self.assertTrue(((left_val == right_val) | (np.isnan(left_val) & np.isnan(right_val))).all())
            else:
                self.assertAlmostEqual(left_val, right_val)

    def test_configure(self):
        latfile = self.testfile
        m0 = Machine(open(latfile, 'r'))
        s0 = m0.allocState({})
        e_cor_idx = 10
        m0.reconfigure(10, {'theta_x': 0.005})
        m0.propagate(s0, 0, 1)
        r0 = m0.propagate(s0, 1, -1, range(len(m0)))

        fm = flameutils.ModelFlame(latfile)
        e = fm.get_element(index=10)[0]
        e['properties']['theta_x'] = 0.005
        fm.configure(e)
        r, s = fm.run(monitor=range(len(m0)))

        rs0 = [ts for (ti,ts) in r0] 
        rs = [ts for (ti,ts) in r] 
        for (is1, is2) in zip(rs0, rs):
            self.iter_all_attrs(is1, is2)


class TestMachineStates(unittest.TestCase):
    def setUp(self):
        latfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.latfile = make_latfile(latfile)

    def test_init_with_s1(self):
        """ test_init_with_s1: s it not None
        """
        m = Machine(open(self.latfile, 'r'))
        s0 = m.allocState({})
        s1 = s0.clone()
        m.propagate(s1, 0, 1)

        ms0 = flameutils.MachineStates(s0)
        self.iter_all_attrs(ms0, s0)

        ms1 = flameutils.MachineStates(s0, machine=m)
        self.iter_all_attrs(ms1, s1)

        ms1_1 = flameutils.MachineStates(s0, latfile=self.latfile)
        self.iter_all_attrs(ms1_1, s1)

    def test_init_with_s2(self):
        """ test_init_with_s2: s it None
        """
        m = Machine(open(self.latfile, 'r'))
        s = m.allocState({})
        ms = flameutils.MachineStates()
        ms.mstates = s
        m.propagate(s, 0, 1)
        self.iter_all_attrs(ms, s)
    
    def test_init_with_machine(self):
        m = Machine(open(self.latfile, 'r'))
        ms = flameutils.MachineStates(machine=m)
        s = m.allocState({})
        m.propagate(s, 0, 1)
        self.iter_all_attrs(ms, s)
 
    def test_init_with_latfile(self):
        m = Machine(open(self.latfile, 'r'))
        ms = flameutils.MachineStates(latfile=self.latfile)
        s = m.allocState({})
        m.propagate(s, 0, 1)
        self.iter_all_attrs(ms, s)

    def test_init_with_mix(self):
        m = Machine(open(self.latfile, 'r'))
        ms = flameutils.MachineStates(machine=m, latfile=self.latfile)
        s = m.allocState({})
        m.propagate(s, 0, 1)
        self.iter_all_attrs(ms, s)

    def iter_all_attrs(self, ms, s):
        k = ['beta', 'bg', 'gamma', 'IonEk', 'IonEs', 'IonQ', 'IonW', 
             'IonZ', 'phis', 'SampleIonK']
        all_keys = [i for i in k]
        all_keys.extend(['ref_{}'.format(i) for i in k] + ['pos'])
        all_keys.extend(['moment0', 'moment0_env', 'moment0_rms', 'moment1'])
        for attr in all_keys:
            left_val, right_val = getattr(ms, attr), getattr(s, attr)
            if isinstance(left_val, np.ndarray):
                #self.assertTrue((np.allclose(left_val, right_val, equal_nan=True) | (np.isnan(left_val) & np.isnan(right_val))).all())
                self.assertTrue(((left_val == right_val) | (np.isnan(left_val) & np.isnan(right_val))).all())
            else:
                self.assertAlmostEqual(left_val, right_val)


class TestInspectLattice(unittest.TestCase):
    def setUp(self):
        latfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.latfile = make_latfile(latfile)
        self.inslat = os.path.join(curdir, 'data/inslat.out')

    def test_wrong_file(self):
        retval = flameutils.inspect_lattice('')
        self.assertEqual(retval, None)

    def test_right_file(self):
        sio = StringIO()
        flameutils.inspect_lattice(self.latfile, out=sio)
        outstr = open(self.inslat).read()
        line1 = [line.strip() for line in sio.getvalue().split('\n')]
        line0 = [line.strip() for line in outstr.split('\n')]
        self.assertEqual(line1, line0)
    

class TestGetElement(unittest.TestCase):
    def setUp(self):
        latfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.latfile = make_latfile(latfile)
        self.m = Machine(open(self.latfile, 'r'))

    def test_one_name(self):
        ename = 'LS1_CA01:CAV4_D1150'
        e0 = [{'index': 27, 'properties': {'L': 0.24, 'aper': 0.017,
              'cavtype': '0.041QWR', 'f': 80500000.0, 
              'name': 'LS1_CA01:CAV4_D1150', 'phi': 325.2, 
              'scl_fac': 0.819578, 'type': 'rfcavity'}}]
        e1 = flameutils.get_element(name=ename, latfile=self.latfile)
        e2 = flameutils.get_element(name=ename, _machine=self.m)
        e3 = flameutils.get_element(name='', _machine=self.m)
        self.assertEqual(e1, e2)
        self.assertEqual(e1, e0)
        self.assertEqual(e3, [])

    def test_multi_names(self):
        enames = [ 
                    'LS1_CA01:SOL1_D1131_1', 
                    'LS1_CA01:CAV4_D1150',
                    'LS1_WB01:BPM_D1286',
                    'LS1_CA01:GV_D1124',
                    'LS1_CA01:BPM_D1144',
                ]
        e0 = [
                {'index': 8, 
                 'properties': {'aper': 0.02, 'B': 5.34529, 
                                'type': 'solenoid', 'L': 0.1, 
                                'name': 'LS1_CA01:SOL1_D1131_1'}}, 
                {'index': 1, 
                 'properties': {'aper': 0.02, 'type': 'drift', 
                                'L': 0.072, 'name': 'LS1_CA01:GV_D1124'}},
                {'index': 154, 
                 'properties': {'type': 'bpm', 
                                'name': 'LS1_WB01:BPM_D1286'}},
                {'index': 27, 
                 'properties': {'aper': 0.017, 
                                'name': 'LS1_CA01:CAV4_D1150', 
                                'f': 80500000.0, 'cavtype': '0.041QWR',
                                'L': 0.24, 'phi': 325.2, 
                                'scl_fac': 0.819578, 
                                'type': 'rfcavity'}},
                {'index': 18, 
                 'properties': {'type': 'bpm', 
                                'name': 'LS1_CA01:BPM_D1144'}}
              ]

        e1 = flameutils.get_element(name=enames, latfile=self.latfile)
        self.assertEqual(e1, e0)
    
    def test_one_index(self):
        idx = 10
        e0 = [{'index': 10,
               'properties': {'name': 'LS1_CA01:DCV_D1131',
               'theta_y': 0.0, 'type': 'orbtrim'}}]
        e1 = flameutils.get_element(index=idx, latfile=self.latfile)
        self.assertEqual(e1, e0)
    
    def test_multi_indice(self):
        idx = range(3)
        e0 = [
                {'index': 0,
                 'properties': {'matrix_variable': 'S',
                 'name': 'S',
                 'type': 'source',
                 'vector_variable': 'P'}},
                {'index': 1,
                 'properties': {'L': 0.072,
                 'aper': 0.02,
                 'name': 'LS1_CA01:GV_D1124',
                 'type': 'drift'}},
                {'index': 2,
                 'properties': {'L': 0.135064,
                 'aper': 0.02,
                 'name': 'DRIFT_1',
                 'type': 'drift'}}
            ]
        e1 = flameutils.get_element(index=idx, latfile=self.latfile)
        self.assertEqual(e1, e0)

    def test_multi_filters(self):
        eidx, etyp = range(20), 'bpm'
        e0 = [
              {'index': 18, 
               'properties': {'name': 'LS1_CA01:BPM_D1144', 'type': 'bpm'}},
              {'index': 5, 
               'properties': {'name': 'LS1_CA01:BPM_D1129', 'type': 'bpm'}}
              ]
        e1 = flameutils.get_element(index=eidx, type=etyp, latfile=self.latfile)
        self.assertEqual(e1, e0)
        
        e2 = flameutils.get_element(index=eidx, type=etyp, latfile=self.latfile, name='LS1_CA01:BPM_D1144')
        self.assertEqual(e2, [e0[0]])

    def test_name_pattern(self):
        name_pattern = 'FS1_BBS:DH_D2394_.?$'
        e1 = flameutils.get_element(_pattern=name_pattern, latfile=self.latfile)
        names = ['FS1_BBS:DH_D2394_{}'.format(i) for i in range(1,10)]
        e2 = flameutils.get_element(name=names, latfile=self.latfile)
        self.assertEqual(e1, e2)


class TestGetIndexByType(unittest.TestCase):
    def setUp(self):
        latfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.latfile = make_latfile(latfile)
        self.m = Machine(open(self.latfile, 'r'))

    def test_wrong_type(self):
        etyp = ''
        e = flameutils.get_index_by_type(type=etyp, latfile=self.latfile)
        self.assertEqual(e, {etyp: []})

        etyp1 = 'no_exist_type'
        e1 = flameutils.get_index_by_type(type=etyp1, latfile=self.latfile)
        self.assertEqual(e1, {etyp1: []})
    
    def test_one_type(self):
        for etyp in flameutils.get_all_types(latfile=self.latfile):
            e = flameutils.get_index_by_type(type=etyp, latfile=self.latfile)
            self.assertEqual(e, {etyp: self.m.find(type=etyp)})

    def test_multi_types(self):
        all_types = flameutils.get_all_types(latfile=self.latfile)
        for n in range(2, len(all_types)):
            etyps = [random.choice(all_types) for _ in range(n)]
            e = flameutils.get_index_by_type(type=etyps, 
                                             latfile=self.latfile)
            e0 = {t: self.m.find(type=t) for t in etyps}
            self.assertEqual(e, e0)


class TestGetIndexByName(unittest.TestCase):
    def setUp(self):
        latfile = os.path.join(curdir, 'lattice/test_0.lat')
        self.latfile = make_latfile(latfile)
        self.m = Machine(open(self.latfile, 'r'))

    def test_wrong_name(self):
        ename = ''
        e = flameutils.get_index_by_name(name=ename, latfile=self.latfile)
        self.assertEqual(e, {ename: []})
        
        ename1 = 'no_exist_name'
        e = flameutils.get_index_by_name(name=ename1, latfile=self.latfile)
        self.assertEqual(e, {ename1: []})

    def test_one_name(self):
        """ test_one_name: repeat for 10 times, each with random name
        """
        all_names = flameutils.get_all_names(latfile=self.latfile)
        for n in range(10):
            ename = random.choice(all_names)
            e = flameutils.get_index_by_name(name=ename, latfile=self.latfile)
            self.assertEqual(e, {ename: self.m.find(name=ename)})

    def test_multi_names(self):
        """ test_multi_names: test names list length of 2~10
        """
        all_names = flameutils.get_all_names(latfile=self.latfile)
        for n in range(2, 10):
            enames = [random.choice(all_names) for _ in range(n)]
            e = flameutils.get_index_by_name(name=enames, 
                                             latfile=self.latfile)
            e0 = {n: self.m.find(name=n) for n in enames}
            self.assertEqual(e, e0)


def t_set0(index=None, name=None, type=None):
    index_v = [] if index is None else index
    name_v = [] if name is None else name
    type_v = [] if type is None else type
    s = set()
    for li in [index_v, name_v, type_v]:
        if s == set() or li == []:
            s = s.union(li)
        else:
            s = s.intersection(li)
    return s


def t_set(**kws):
    s = set()
    for k in kws:
        v = kws.get(k, [])
        if s == set() or v == []:
            s = s.union(v)
        else:
            s = s.intersection(v)
    return s


def tt_set():
    index, name, type = [], [], []
    print(t_set(index=index,name=name,type=name))

    index, name, type = [1], [], []
    print(t_set(index=index,name=name,type=name))

    index, name, type = [], [1], []
    print(t_set(index=index,name=name,type=name))

    index, name, type = [], [], [1]
    print(t_set(index=index,name=name,type=name))

    index, name, type = [1,2], [2], [1,3]
    print(t_set(index=index,name=name,type=name))


def t_modelflame():
    #import logging
    #logging.getLogger().setLevel(logging.INFO)

    latfile0 = 'lattice/test_0.lat'
    latfile = make_latfile(latfile0)
    # latfile is None
    fm1 = flameutils.ModelFlame()
    #print(fm1.latfile)
    #print(fm1.machine)
    #print(fm1.mstates)
    fm1.inspect_lattice()

    m = Machine(open(latfile))
    fm1.latfile = latfile
    fm1.machine = m
    fm1.mstates = m.allocState({})
    #fm1.machine, fm1.mstates = fm1.init_machine(latfile)

    print(fm1.latfile)
    #print(fm1.machine)
    print(fm1.mstates)
    print('-'*70)
    
    # latfile is not None
    fm2 = flameutils.ModelFlame(lat_file=latfile)
    #print(fm2.latfile)
    #print(fm2.machine)
    #print(fm2.mstates)


    # inspection
    fm2.inspect_lattice()
    print(fm2.get_element(type='stripper'))
    #sio = StringIO()
    #flameutils.inspect_lattice(latfile, out=sio)
    #print(sio.getvalue())
    

    # get index by name
    names = [
             'LS1_CA01:SOL1_D1131_1', 
             'LS1_CA01:CAV4_D1150',
             'LS1_WB01:BPM_D1286',
             'LS1_CA01:GV_D1124',
             'LS1_CA01:BPM_D1144'
             ]
    print flameutils.get_index_by_name(name=names, latfile=latfile)
    print flameutils.get_index_by_name(name=names, _machine=m)
    print flameutils.get_index_by_name(name=names, _machine=m, rtype='list')
    print('-'*70)
    print(flameutils.get_element(name=names, latfile=latfile))
    print('-'*70)

    #names = ''
    #print flameutils.get_index_by_name(name=names, latfile=latfile)


    types = ['stripper', 'source']
    print flameutils.get_index_by_type(type=types, latfile=latfile)
    print flameutils.get_index_by_type(type=types, _machine=m)


    insres1 = flameutils.get_element(name=names, type=['source','bpm'], latfile=latfile)
    print(insres1)

    insres2 = flameutils.get_element(type='stripper', latfile=latfile)
    print(insres2)
    

    print(flameutils.get_all_types(latfile=latfile))
    

def t_machinestates():
    latfile0 = os.path.join(curdir, 'lattice/test_0.lat')
    latfile = make_latfile(latfile0)
    m = Machine(open(latfile, 'r'))
    s0 = m.allocState({})
    s1 = s0.clone()
    m.propagate(s1, 0, 1)
    
    ms0 = flameutils.MachineStates(s0)
    iter_all_attrs(ms0, s0)
    #a, b = ms0.moment1, s0.moment1
    #print ((a == b) | (np.isnan(a) & np.isnan(b))).all()
    
    #np.testing.assert_allclose(a,b)

    ms1 = flameutils.MachineStates(s0, machine=m)
    iter_all_attrs(ms1, s1)
    print ms1.moment0_env
    print s1.moment0_env

    ms2 = flameutils.MachineStates(s0, latfile=latfile)
    iter_all_attrs(ms2, s1)
    

def iter_all_attrs(ms, s):
    k = ['beta', 'bg', 'gamma', 'IonEk', 'IonEs', 'IonQ', 'IonW', 
         'IonZ', 'phis', 'SampleIonK']
    all_keys = [i for i in k]
    all_keys.extend(['ref_{}'.format(i) for i in k] + ['pos'])
    all_keys.extend(['moment0', 'moment0_env', 'moment0_rms', 'moment1'])
    for attr in all_keys:
        left_val, right_val = getattr(ms, attr), getattr(s, attr)
        if isinstance(left_val, np.ndarray):
            #print(attr, (np.allclose(left_val, right_val, equal_nan=True) | (np.isnan(left_val) & np.isnan(right_val))).all())
            print(attr, ((left_val == right_val) | (np.isnan(left_val) & np.isnan(right_val))).all())
        else:
            print(attr, left_val==right_val)


if __name__ == '__main__':
    #t_modelflame()
    t_machinestates()
    #tt_set()
