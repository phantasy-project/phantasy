#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Test CFC database

Location: phantasy.library.channelfinder

Tong Zhang <zhangt@frib.msu.edu>
2017-01-09 14:23:59 EST
"""

import unittest
import os

from phantasy.library.channelfinder import CFCDatabase


curdir = os.path.abspath(os.path.dirname(__file__))

class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.config_dir = os.path.join(curdir, 'config')
        self.db = os.path.join(self.config_dir, 
                'FRIB_TEST/baseline_channels_bak.sqlite')

    def test_init_valid(self):
        cfcd = CFCDatabase()
        self.assertEqual(cfcd.db_name, None)
        cfcd.db_name = self.db
        self.assertEqual(cfcd.db_name, self.db)
    
    def test_init_invalid(self):
        cfcd = CFCDatabase()
        self.assertEqual(cfcd.db_name, None)
        cfcd.db_name = 'INVALID_DBNAME'
        self.assertEqual(cfcd.db_name, None)

        cfcd.db_name = self.db
        self.assertEqual(cfcd.db_name, self.db)

        cfcd.db_name = 'INVALID_DBNAME'
        self.assertEqual(cfcd.db_name, self.db)



