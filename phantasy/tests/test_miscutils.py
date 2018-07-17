#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unittest for miscutils module

:author: Tong Zhang <zhangt@frib.msu.edu>
:date: 2016-11-22 11:52:21 AM EST
"""

import unittest
import numpy as np
from phantasy.library.misc import miscutils
import os

curdir = os.path.abspath(os.path.dirname(__file__))

class TestMiscUtils(unittest.TestCase):
    def test_flatten_gen(self):
        l0 = [1,2,3]
        self.assertEqual(list(miscutils._flatten(l0)), [1,2,3])

        l0 = [1,2,[3]]
        self.assertEqual(list(miscutils._flatten(l0)), [1,2,3])

        l0 = (1,2,[3])
        self.assertEqual(list(miscutils._flatten(l0)), [1,2,3])

        l0 = (1,2,(3,[4,5]))
        self.assertEqual(list(miscutils._flatten(l0)), [1,2,3,4,5])

        l0 = [1,2,3,[4,5],[6,[7,8,[9,10,['x',['y']]]]]]
        l1 = list(miscutils._flatten(l0))
        l2 = [1,2,3,4,5,6,7,8,9,10,'x','y']
        self.assertEqual(l1, l2)

    def test_flatten_list(self):
        l0 = [1,2,3]
        self.assertEqual(miscutils.flatten(l0), [1,2,3])

        l0 = [1,2,[3]]
        self.assertEqual(miscutils.flatten(l0), [1,2,3])

        l0 = (1,2,[3])
        self.assertEqual(miscutils.flatten(l0), [1,2,3])

        l0 = (1,2,(3,[4,5]))
        self.assertEqual(miscutils.flatten(l0), [1,2,3,4,5])

        l0 = [1,2,3,[4,5],[6,[7,8,[9,10,['x',['y']]]]]]
        l1 = miscutils.flatten(l0)
        l2 = [1,2,3,4,5,6,7,8,9,10,'x','y']
        self.assertEqual(l1, l2)

    def test_get_interset(self):
        a, b, c = [], [], []
        self.assertEqual(miscutils.get_intersection(a, b, c), [])

        a, b, c = [1], [2], []
        self.assertEqual(miscutils.get_intersection(a, b, c), [])
        
        a, b, c = [1,2], [2], []
        self.assertEqual(miscutils.get_intersection(a, b, c), [2])
        
        a, b, c = [1,2], [2], [2,3]
        self.assertEqual(miscutils.get_intersection(a, b, c), [2])
        
        a, b, c = [1,2], [3,4], [2,3]
        self.assertEqual(miscutils.get_intersection(a, b, c), [])
  
def t_1():
    l0 = [1,2,3]
    l1 = miscutils.flatten(l0)
    print(l1)
     
    l0 = [1,2,3, (4,5)]
    l1 = miscutils.flatten(l0)
    print(l1)

    l0 = [1,2,3,[4,5],[6,[7,8,[9,10,['x',['y']]]]]]
    l1 = miscutils.flatten(l0)
    print(l1)

if __name__ == '__main__':
    t_1()
