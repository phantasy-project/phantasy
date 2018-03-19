# -*- coding: utf-8 -*-

import unittest
import os

from phantasy.facility.frib.layout import fribxlf
from phantasy.library.parser import Configuration

curdir = os.path.dirname(__file__)

TEST_MACH = "FRIB_XLF"
MACH_PATH = os.path.join(curdir, 'config', TEST_MACH)
XLF_PATH = os.path.join(MACH_PATH, 'T30102-CM-000155-R001_20170724.xlsx')
CONFIG_PATH = os.path.join(MACH_PATH, 'phantasy.cfg')
LAYOUT_PATH = os.path.join(MACH_PATH, 'layout_bak.csv')
CHANNELS_PATH = os.path.join(MACH_PATH, 'channels_bak.csv')


class TestXLFParser(unittest.TestCase):
    def setUp(self):
        self.layout_file = os.path.join(MACH_PATH, 'layout.csv')
        self.channels_file = os.path.join(MACH_PATH, 'channels.csv')
        self.start_elem = 'FE_ISRC1:ACC_DFT_D0700_1'
        self.end_elem = 'FE_LEBT:GV_DFT_D0999_3'

    def tearDown(self):
        for f in [self.layout_file, self.channels_file]:
            if os.path.isfile(f):
                os.remove(f)

    def test_layout(self):
        config = Configuration(CONFIG_PATH)
        layout = fribxlf.build_layout(xlfpath=XLF_PATH, config=config)
        with open(self.layout_file, 'wb') as f:
            layout.write(f, start=self.start_elem, end=self.end_elem)
        
        with open(LAYOUT_PATH, 'rb') as f:
            f_str0 = f.read().strip().decode()
        with open(self.layout_file, 'rb') as f:
            f_str1 = f.read().strip().decode()
        
        self.assertEqual(f_str0, f_str1)
