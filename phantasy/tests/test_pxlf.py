# -*- coding: utf-8 -*-

import unittest
import os
import csv

from phantasy.facility.frib.layout import fribxlf
from phantasy.library.parser import Configuration

curdir = os.path.abspath(os.path.dirname(__file__))

TEST_MACH = "FRIB_XLF"
MACH_PATH = os.path.join(curdir, 'config', TEST_MACH)
XLF_PATH = os.path.join(MACH_PATH, 'T30102-CM-000155-R001_20170724.xlsx')
CONFIG_PATH = os.path.join(MACH_PATH, 'phantasy.cfg')
LAYOUT_PATH = os.path.join(MACH_PATH, 'layout_bak.csv')
CHANNELS_PATH = os.path.join(MACH_PATH, 'channels_bak.csv')
TEST_PATH = "/tmp"


class TestXLFParser(unittest.TestCase):
    def setUp(self):
        self.layout_file = os.path.join(TEST_PATH, 'layout.csv')
        self.channels_file = os.path.join(TEST_PATH, 'channels.csv')
        self.start_elem = 'FE_ISRC1:ACC_DFT_D0700_1'
        self.end_elem = 'FE_LEBT:GV_DFT_D0999_3'

    def tearDown(self):
        for f in [self.layout_file, self.channels_file]:
            if os.path.isfile(f):
                os.remove(f)

    def test_layout(self):
        config = Configuration(CONFIG_PATH)
        layout = fribxlf.build_layout(xlfpath=XLF_PATH, config=config)
        with open(self.layout_file, 'w') as f:
            layout.write(f, start=self.start_elem, end=self.end_elem)

        compare_csvfiles(self, LAYOUT_PATH, self.layout_file)


def compare_csvfiles(tobj, file1, file2):
    """Compare two csv files.
    """
    NPRC = 6  # assertAlmostEqual(x, y, places=NPRC)
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        csv1, csv2 = csv.reader(f1), csv.reader(f2)
        header1, header2 = next(csv1), next(csv2)
        tobj.assertEqual(sorted(header1), sorted(header2))
        for line1, line2 in zip(csv1, csv2):
            row1 = dict(zip(header1, line1))
            row2 = dict(zip(header2, line2))
            for k in row1:
                try:
                    v1, v2 = float(row1[k]), float(row2[k])
                    tobj.assertAlmostEqual(v1, v2, places=NPRC)
                except ValueError:
                    tobj.assertEqual(row1[k], row2[k])
