#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Test PV datasource module

Location: phantasy.library.pv

Tong Zhang <zhangt@frib.msu.edu>
2017-01-05 15:55:03 EST
"""

import unittest
import os
import pickle
from fnmatch import fnmatch

from phantasy.library.pv import DataSource


curdir = os.path.dirname(__file__)

# test data is generated by gen_datasource.py

def load_data(fname):
    with open(fname, 'rb') as f:
        data = pickle.load(f)
    return data


class TestDataSource(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        self.db = os.path.join(self.config_dir, 
                'FRIB1/baseline_channels_bak.sqlite')
        self.url = 'https://127.0.0.1:8181/ChannelFinder'
        self.file1 = 'cfd_data_1.pkl'
        self.file2 = 'cfd_data_2.pkl'
        self.file3 = 'cfd_data_3.pkl'

    def test_get_data_1(self):
        ds = DataSource()
        ds.source = self.db
        data = ds.get_data()
        data_0 = load_data(self.file1)
        self.assertEqual(data, data_0)

    def test_get_data_2(self):
        ds = DataSource()
        ds.source = self.db
        data = ds.get_data(tag_filter='phyutil.sub.CB09',
                           prop_filter='elem*')
        data_0 = load_data(self.file2)
        self.assertEqual(data, data_0)

    def test_get_data_3(self):
        ds = DataSource()
        ds.source = self.db
        data = ds.get_data(prop_filter=['elem*', 
                            ('elemHandle', 'setpoint')])
        data_0 = load_data(self.file3)
        self.assertEqual(data, data_0)

    def test_get_data_4(self):
        ds = DataSource()
        ds.source = self.db
        data = ds.get_data(name_filter='*',
                           prop_filter=['elem*', 
                            ('elemHandle', 'setpoint')])
        data_0 = load_data(self.file3)
        self.assertEqual(data, data_0)

    def test_get_data_5(self):
        ds = DataSource()
        ds.source = self.db
        data = ds.get_data(name_filter='*BPM*',
                           prop_filter=['elem*', 
                            ('elemHandle', 'setp int')])
        for d in data:
            self.assertTrue(fnmatch(d['name'], '*BPM*'))
            self.assertTrue(
                    {'name':'elemHandle', 'value':'setpoint'} in 
                    d['properties'])

    def test_get_data_6(self):
        ds = DataSource()
        ds.source = self.db
        data1 = ds.get_data(name_filter='*PM*')
        data2 = ds.get_data(name_filter='*BPM*', raw_data=data1)

        self.assertTrue(len(data2)<=len(data1))
        for d in data1:
            self.assertTrue(fnmatch(d['name'], '*PM*'))
        for d in data2:
            dp = {p['name']:p['value'] for p in d['properties']}
            self.assertTrue(dp.get('elemType'), 'BPM')
        



