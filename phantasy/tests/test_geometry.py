#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Test geometry module

Location: phantasy.library.physics.geometry

Tong Zhang <zhangt@frib.msu.edu>
2017-03-28 09:46:57 AM EDT
"""

import unittest
import numpy as np


from phantasy.library.physics import Point
from phantasy.library.physics import Line


class TestPoint(unittest.TestCase):
    def setUp(self):
        pass

    def test_init_none_none(self):
        # None, None
        p = Point()
        self.assertTrue(0 <= p[0] < 1)
        self.assertTrue(0 <= p[1] < 1)

    def test_init_int_none(self):
        # 1, None
        p = Point(1,)
        self.assertEqual(p[0], 1.0)
        self.assertTrue(0 <= p[1] < 1)

    def test_init_none_int(self):
        # None, 1
        p = Point(y=1)
        self.assertEqual(p[1], 1.0)
        self.assertTrue(0 <= p[0] < 1)

    def test_init_none_invalid(self):
        # None, INVALID
        p = Point(y='a')
        self.assertTrue(0 <= p[0] < 1)
        self.assertTrue(0 <= p[1] < 1)

    def test_init_invalid_invalid(self):
        # INVALID, INVALID
        p = Point('a', 'b')
        self.assertTrue(0 <= p[0] < 1)
        self.assertTrue(0 <= p[1] < 1)

    def test_init_invalid_none(self):
        # INVALID, None
        p = Point(x='a')
        self.assertTrue(0 <= p[0] < 1)
        self.assertTrue(0 <= p[1] < 1)

    def test_init_tuple(self):
        # tuple
        p = Point((1,2))
        self.assertEqual(p[0], 1.0)
        self.assertEqual(p[1], 2.0)

    def test_init_list(self):
        # list
        p = Point([1,2])
        self.assertEqual(p[0], 1.0)
        self.assertEqual(p[1], 2.0)

    def test_init_array(self):
        # array
        p = Point(np.array([1,2]))
        self.assertEqual(p[0], 1.0)
        self.assertEqual(p[1], 2.0)

    def test_init_Point(self):
        # Point instance
        p0 = Point(0, 1)
        p10 = Point(p0)
        self.assertEqual(p10[0], 0.0)
        self.assertEqual(p10[1], 1.0)
        
    def test_compare_equal(self):
        # equal compare
        self.assertTrue(Point(1, 2) == Point(x=1, y=2))
        self.assertTrue(Point(1, 2) == Point(1, y=2))
        self.assertTrue(Point(1, 2) == Point(*(1, 2)))
        self.assertTrue(Point(1, 2) == Point(Point(1, 2)))

    def test_add(self):
        self.assertTrue(Point(1, 2) == Point(0.5, 0.5) + Point(0.5, 1.5))
        self.assertTrue(
                Point(1, 2) == sum(
                    [Point(0.5, 0.5), Point(0.5, 1.5)], 
                    Point(0, 0))
                )
        self.assertTrue(
                Point(45, 45) == sum(
                    [Point(x, x) for x in range(10)], 
                    Point(0, 0))
                )
        self.assertTrue(
                Point(1, 2) == sum(
                    [Point(0.5, 0.5), Point(0.5, 1.5)])
                )

    def test_sub(self):
        self.assertTrue(Point(1, 1) == Point(3, 2) - Point(2, 1))

    def test_mul(self):
        self.assertTrue(Point(1, 1) == Point(2, 2) * 0.5)
    
    def test_div(self):
        self.assertTrue(Point(1, 1) == Point(2, 2) / 2)

    def test_abs(self):
        self.assertEqual(abs(Point(1, 1)), np.sqrt(2))

    def test_projection(self):
        # projection
        a = Point(1,1)
        b = Point(5,3)
        p = Point(2,5)
        p_ab = p.proj_point(a, b)

        # distance: point to point
        ds1 = p.distance_to_point(p_ab)

        # distance: point to line
        ds2 = p.distance_to_line(a, b)

        self.assertEqual(ds1, ds2)
        
        # inline test
        self.assertTrue(p_ab.is_in_line(a, b))

    def test_move(self):
        ## move
        p = Point(0, 0)
        direction1 = (30, 1)
        p_moveto1 = p.move(direction=direction1)
        direction2 = (45, 1)
        p_moveto2 = p.move(direction=direction2)
        direction3 = (60, 1)
        p_moveto3 = p.move(direction=direction3)
        
        self.assertAlmostEqual(p.distance_to_point(p_moveto1), 1.0)
        self.assertAlmostEqual(p.distance_to_point(p_moveto2), 1.0)
        self.assertAlmostEqual(p.distance_to_point(p_moveto3), 1.0)

        self.assertAlmostEqual(abs(p_moveto1), 1.0)
        self.assertAlmostEqual(abs(p_moveto2), 1.0)
        self.assertAlmostEqual(abs(p_moveto3), 1.0)

        x = Point(1, 0)
        o = Point(0, 0)
        ox = Line(o, x)
        op1 = Line(o, p_moveto1)
        op2 = Line(o, p_moveto2)
        op3 = Line(o, p_moveto3)
        self.assertAlmostEqual(op1.angle(ox), direction1[0])
        self.assertAlmostEqual(op2.angle(ox), direction2[0])
        self.assertAlmostEqual(op3.angle(ox), direction3[0])
    
    def test_rotate(self):
        p0 = Point(1, 0)
        angle = 90
        p1 = p0.rotate(angle)
        self.assertAlmostEqual(p1.x, 0)
        self.assertAlmostEqual(p1.y, 1)


class TestLine(unittest.TestCase):
    def test_rotate(self):
        angle = 31
        line1 = Line(Point(1, 1), Point(2, 4))
        line2 = line1.rotate(angle)
        self.assertAlmostEqual(angle, line2.angle(line1))

    def test_angle(self):
        line1 = Line(Point(0,0), Point(2,0))
        angle = line1.angle(direction=(45, 1))
        self.assertAlmostEqual(angle, 45)
        


