#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unittest for parseutils module

:author: Tong Zhang <zhangt@frib.msu.edu>
:date: 2016-11-15 18:08:30 PM EST
"""

import unittest
#import numpy as np
from phyapps import parseutils
#from flame import Machine
import os

curdir = os.path.dirname(__file__)

class TestIniParser(unittest.TestCase):
    def setUp(self):
        self.inifile = os.path.join(curdir, 'config/phyutil.ini')
        self.inifile_sample = os.path.join(curdir, 'config/sample.ini')
        self.inip = parseutils.IniParser(self.inifile)
        #self.maxDiff = None

    def test_todict(self):
        confd = self.inip.to_dict()
        d = {
                'COMMON':{
                    'submachines': 'LINAC LS1',
                    'default_submachine': 'LINAC',
                    'output_dir': '~/Development/tools/data',
                    }, 
                'LINAC':{
                    'controls_protocol': 'EPICS',
                    's_begin': '0.0', 
                    's_end': '158.094',
                    'loop': '0',
                    'model': 'impact',
                    'cfs_url': 'baseline_channels.sqlite',
                    'cfs_tag': 'phyutil.sys.LINAC',
                    'ss_url': 'http://localhost:4810',
                    'physics_data': 'linac.hdf5',
                    'unit_conversion': 'linac_unitconv.hdf5, UnitConversion',
                    'settings_file': 'baseline_settings.json',
                    'layout_file': 'baseline_layout.csv',
                    'config_file': 'phyutil.cfg',
                    'impact_map': 'ls1_fs1.map',
                    },
                'LINAC_CF':{
                      'controls_protocol': 'EPICS',
                      's_begin': '0.0',
                      's_end': '158.094',
                      'loop': '0',
                      'model': 'impact',
                      'cfs_url': 'baseline_channels.sqlite',
                      'cfs_url': 'https://localhost:8080/ChannelFinder',
                      'cfs_tag': 'phyutil.sys.LINAC',
                      'ss_url': 'http://localhost:4810',
                      'physics_data': 'linac.hdf5',
                      'unit_conversion': 'linac_unitconv.hdf5, UnitConversion',
                      'settings_file': 'baseline_settings.json',
                      'layout_file': 'baseline_layout.csv',
                      'config_file': 'phyutil.cfg',
                      'impact_map': 'ls1_fs1.map',
                      },
                'LS1':{'controls_protocol': 'EPICS',
                       's_begin': '0.0',
                       's_end': '80.000',
                       'loop': '1',
                       'model': 'impact',
                       'cfs_url': 'ls1_fs1.sqlite',
                       'cfs_tag': 'phyutil.sys.LS1',
                       'ss_url': 'None',
                       'physics_data': 'linac.hdf5',
                       'unit_conversion': 'linac_unitconv.hdf5, UnitConversion',
                       'settings_file': 'ls1_settings.json',
                       'layout_file': 'ls1_layout.csv',
                       'config_file': 'phyutil.cfg',
                       }
                }
        self.assertEqual(confd, d)



