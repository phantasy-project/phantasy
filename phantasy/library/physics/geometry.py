#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data simulation, geometrical resources.

Tong Zhang <zhangt@frib.msu.edu>
2017-03-27 11:29:39 AM EDT
"""

import numpy as np

EPS = np.finfo(float).eps


class Point(object):
    """Points in 2D Cartesian coordinate system, if invalid input is detected,
    return ``Point(x,y)``, ``x``, ``y`` is random number between 0 and 1.

    Initialization approaches:

    Examples
    --------
    The following ways are the same:

    >>> Point(x=1, y=2)
    >>> Point(1, y=2)
    >>> Point(1, 2)
    >>> Point((1, 2))
    >>> Point([1, 2])
    >>> Point(Point(1, 2))
    """
    __slot__ = ['_x', '_y']

    def __init__(self, x=None, y=None):
        self.point = (x, y)

    @property
    def x(self):
        """float: x coordinate."""
        return self._x

    @property
    def y(self):
        """float: y coordinate."""
        return self._y

    @x.setter
    def x(self, x):
        if isinstance(x, float):
            self._x = x
        elif isinstance(x, int):
            self._x = float(x)
        else:
            self._x = np.random.random()

    @y.setter
    def y(self, y):
        if isinstance(y, float):
            self._y = y
        elif isinstance(y, int):
            self._y = float(y)
        else:
            self._y = np.random.random()

    @property
    def point(self):
        """Array: x, y coordinate."""
        return np.array([self._x, self._y])

    @point.setter
    def point(self, p):
        x, y = p[0], p[1]
        # x is a list or tuple or array,
        # e.g. x = (1, 2); x = [1, 2]; x = np.array([1,2])
        if isinstance(x, (list, tuple)):
            self.x, self.y = x[0], x[1]
        elif isinstance(x, np.ndarray):  # np.int64 is not instance of int
            x = x.tolist()
            self.x, self.y = x[0], x[1]
        elif isinstance(x, Point):
            # x is Point
            self.x, self.y = x.point
        else:
            # two floats
            self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        if isinstance(other, int):
            other = Point(0, 0)
        elif isinstance(other, (list, tuple, np.ndarray)):
            other = Point(other)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(other * self.x, other * self.y)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __radd__(self, other):
        if isinstance(other, int):
            other = Point(0, 0)
        elif isinstance(other, (list, tuple, np.ndarray)):
            other = Point(other)
        return Point(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return self.distance_to_point((0, 0))

    def distance_to_point(self, p):
        """Distance to point ``p``.
        """
        return Point.calc_distance_to_point(self.point, p)

    def distance_to_line(self, a, b):
        """Distance to line built by point ``a`` and ``b``.
        """
        return Point.calc_distance_to_line(self.point, a, b)

    def proj_point(self, a, b):
        """Projected point to line built by point ``a`` and ``b``.
        """
        return Point.calc_proj_point(self.point, a, b)

    def is_in_line(self, a, b):
        """Test if point is in line built by ``a`` and ``b``.
        """
        return Point.test_is_in_line(self.point, a, b)

    @staticmethod
    def calc_proj_point(p, a, b):
        """Return projected point of ``p`` to line built by point ``a``
        and ``b``.

        Parameters
        ----------
        p : tuple, list or Point
            Point to be projected, could be array of ``(x, y)``, or ``Point()``
            instance.
        a : tuple, list or Point
        b : tuple, list or Point
            Two point to build a line that ``p`` projected on to.

        Returns
        -------
        ret : Point
            Projected point onto a line.
        """
        if isinstance(p, Point):
            p = p.point
        elif isinstance(p, (tuple, list, np.ndarray)):
            p = np.array(p)
        if isinstance(a, Point):
            a = a.point
        elif isinstance(a, (tuple, list, np.ndarray)):
            a = np.array(a)
        if isinstance(b, Point):
            b = b.point
        elif isinstance(b, (tuple, list, np.ndarray)):
            b = np.array(b)
        return Point(a + np.dot(p - a, b - a) / np.dot(b - a, b - a) * (b - a))

    @staticmethod
    def calc_distance_to_point(a, b):
        """Calculate distance between two points ``a`` and ``b``.

        Parameters
        ----------
        a : tuple, list or Point
            ``(x,y)`` coordinate to represent a point.
        b : tuple, list or Point
            ``(x,y)`` coordinate to represent a point.

        Returns
        -------
        ret: float
            Distance between two points.
        """
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    @staticmethod
    def calc_distance_to_line(p, a, b):
        """Distance from point ``p`` to line built by point ``a`` and
        ``b``.

        Parameters
        ----------
        p : tuple, list or Point
            Point out of a line, could be array of ``(x, y)``, or ``Point()``
            instance.
        a : tuple, list or Point
        b : tuple, list or Point
            Two point to build a line.

        Returns
        -------
        ret : float
            Distance from ``p`` to line built by ``a`` and ``b``.
        """
        if isinstance(p, Point):
            p = p.point
        elif isinstance(p, (tuple, list, np.ndarray)):
            p = np.array(p)
        if isinstance(a, Point):
            a = a.point
        elif isinstance(a, (tuple, list, np.ndarray)):
            a = np.array(a)
        if isinstance(b, Point):
            b = b.point
        elif isinstance(b, (tuple, list, np.ndarray)):
            b = np.array(b)
        return abs(np.cross(p - a, b - a) / np.sqrt(np.dot(b - a, b - a)))

    @staticmethod
    def test_is_in_line(p, a, b):
        """Test if point ``p`` is within line built by ``a`` and ``b``.

        Parameters
        ----------
        p : tuple, list or Point
            Point, could be array of ``(x, y)``, or ``Point()``
            instance.
        a : tuple, list or Point
        b : tuple, list or Point
            Two point to build a line, ``a`` and ``b`` is limits of the line.

        """
        if isinstance(p, Point):
            p = p.point
        elif isinstance(p, (tuple, list, np.ndarray)):
            p = np.array(p)
        if isinstance(a, Point):
            a = a.point
        elif isinstance(a, (tuple, list, np.ndarray)):
            a = np.array(a)
        if isinstance(b, Point):
            b = b.point
        elif isinstance(b, (tuple, list, np.ndarray)):
            b = np.array(b)

        ap, ab = p - a, b - a
        if abs(np.cross(ap, ab) - EPS) < 0.0:  # out of line AB
            return False  # , 'out of Line AB'
        if np.dot(ap, ab) < 0.0:  # left of a
            return False  # , 'in Line AB, but left of a'
        if np.dot(ap, ab) > np.dot(ab, ab):  # right of b
            return False  # , 'in Line AB, but right of b'
        return True  # , 'within Line AB'

    def __getitem__(self, i):
        return self.point[i]

    def __repr__(self):
        return "Point ({0:.3f}, {1:.3f})".format(self._x, self._y)

    def move(self, vec=None, **kws):
        """Move point by given vector.

        Parameters
        ----------
        vec : array, list or tuple
            Along vector ``(x, y)`` to move point.

        Keyword Arguments
        -----------------
        direction : tuple
            Tuple of ``(theta, length)``, ``theta`` is anti-clockwised angle
            from ``x(+)`` to vector in degree, ``length`` is moving length.
            This argument will override *vec*.

        Returns
        -------
        ret : Point
            New *Point* object after moving.
        """
        if kws.get('direction', None) is not None:
            angle, length = kws.get('direction')
            theta = angle / 180.0 * np.pi
            m_vec = np.array((np.cos(theta), np.sin(theta))) * length
        else:
            m_vec = vec
        if m_vec is None:
            m_vec = (0, 0)
        return Point(self.point + m_vec)

    def rotate(self, angle, p0=None):
        """Rotate *angle* with *p0*.

        Parameters
        ----------
        angle : float
            Anti-clockwised rotating angle, degree.
        p0 : Point
            Rotating central point, ``(0,0)`` by default.

        Returns
        -------
        ret : Point
            New Point after rotation.
        """
        if p0 is None:
            p0 = Point(0, 0)
        p1 = self - p0
        theta = angle / 180.0 * np.pi
        m = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        p1_rot, = np.dot(m, np.vstack(p1[:])).T
        return Point(p1_rot) + p0


class Line(object):
    """Lines in 2D Cartesian coordinate system, if invalid input is detected,
    return ``Line(0,1) from Point(0,0) to Point(0,1)``.

    Note
    ----
    Always initilize with two points.

    Initialization approaches:

    Examples
    --------
    Any one of the following is to create a line from ``(0,0)`` to ``(0,1)``

    >>> Line()
    >>> Line((0,1))
    >>> Line((0,0),(0,1))
    >>> Line(p1=(0,0), p2=(0,1))
    >>> Line(Point(0,0), Point(0,1))

    """

    def __init__(self, p1=None, p2=None):
        self.vec = (p1, p2)

    @property
    def x(self):
        """float: x coordinate."""
        return self._x

    @property
    def y(self):
        """float: y coordinate."""
        return self._y

    @x.setter
    def x(self, x):
        if isinstance(x, float):
            self._x = x
        elif isinstance(x, int):
            self._x = float(x)
        else:
            self._x = 0.0

    @y.setter
    def y(self, y):
        if isinstance(y, float):
            self._y = y
        elif isinstance(y, int):
            self._y = float(y)
        else:
            self._y = 1.0

    @property
    def vec(self):
        return np.array([self._x, self._y])

    @vec.setter
    def vec(self, vec):
        p1, p2 = vec[0], vec[1]
        if p1 is None:
            if p2 is None:
                p1, p2 = Point(0, 0), Point(0, 1)
            elif isinstance(p2, (list, tuple, np.ndarray, Point)):
                p1, p2 = Point(0, 0), Point(p2)
            else:
                print("Point should be defined by list, tuple, array or Point.")
                p1, p2 = Point(0, 0), Point(0, 1)
        elif isinstance(p1, (list, tuple, np.ndarray, Point)):
            if p2 is None:
                p1, p2 = Point(0, 0), Point(p1)
            elif isinstance(p2, (list, tuple, np.ndarray, Point)):
                p1, p2 = Point(p1), Point(p2)
            else:
                print("Point should be defined by list, tuple, array or Point.")
                p1, p2 = Point(0, 0), Point(0, 1)
        else:
            print("Point should be defined by list, tuple, array or Point.")
            p1, p2 = Point(0, 0), Point(0, 1)

        self._x, self._y = (p2 - p1).point
        self._p_begin, self._p_end = p1, p2
        self._stackpoints = np.vstack([self._p_begin.point, self._p_end.point])

    @property
    def pbegin(self):
        """Point: Starting point of line."""
        return self._p_begin

    @property
    def pend(self):
        """Point: Ending point of line."""
        return self._p_end

    def __repr__(self):
        return "Line ({0:.3f}, {1:.3f}) from {2} to {3}".format(
            self._x, self._y, self._p_begin, self._p_end)

    def __eq__(self, other):
        return ((self.x == other.x)
                and (self.y == other.y)
                and (self.pbegin == other.pbegin)
                and (self.pend == other.pend))

    def __abs__(self):
        return np.sqrt(self.x * self.x + self.y * self.y)

    def angle(self, other=None, **kws):
        """Angle between lines.

        Parameters
        ----------
        other : Line
            Another line.

        Keyword Arguments
        -----------------
        direction : tuple
            Tuple of ``(theta, length)``, ``theta`` is anti-clockwised angle
            from ``x(+)`` to vector in degree, ``length`` is moving length.
            This argument will override *vec*.

        Returns
        -------
        ret : float
            Angle in degree.
        """
        if isinstance(other, Line):
            # Line
            tmp = np.dot(self.vec, other.vec) / abs(self) / abs(other)
        else:
            if kws.get('direction', None) is not None:
                angle, length = kws.get('direction')
                theta = angle / 180.0 * np.pi
                m_vec = np.array((np.cos(theta), np.sin(theta))) * length
                tmp = np.dot(self.vec, m_vec) / abs(self) / length
        if np.allclose(-1, tmp):
            tmp = -1.0
        elif np.allclose(1, tmp):
            tmp = 1.0
        return np.arccos(tmp) / np.pi * 180.0

    def cross(self, other):
        """Cross point of two lines.

        Returns
        -------
        ret : Point
            Point both on all lines.

        """
        # line1 = p1 + t1 * d1
        # line2 = p2 + t2 * d2
        p1, p2 = self.pbegin, other.pbegin
        d1, d2 = self.vec, other.vec
        t1 = np.cross((p2 - p1).point, d2) / np.cross(d1, d2)
        return p1 + t1 * d1

    def move(self, vec=None, **kws):
        """Parallel move line by given vector.

        Parameters
        ----------
        vec : array, list or tuple
            Along vector ``(x, y)`` to move line.

        Keyword Arguments
        -----------------
        direction : tuple
            Tuple of ``(theta, length)``, ``theta`` is anti-clockwised angle
            from ``x(+)`` to vector in degree, ``length`` is moving length.
            This argument will override *vec*.

        Returns
        -------
        ret : Line
            New *Line* object after moving.
        """
        if kws.get('direction', None) is not None:
            angle, length = kws.get('direction')
            theta = angle / 180.0 * np.pi
            m_vec = np.array((np.cos(theta), np.sin(theta))) * length
        else:
            m_vec = vec
        if m_vec is None:
            m_vec = (0, 0)
        new_p_begin = self._p_begin + m_vec
        new_p_end = self._p_end + m_vec
        return Line(new_p_begin, new_p_end)

    def rotate(self, angle, p0=None):
        """Rotate *angle* with *p0*.

        Parameters
        ----------
        angle : float
            Anti-clockwised rotating angle, degree.
        p0 : Point
            Rotating central point, middle point of line by default.

        Returns
        -------
        ret : Line
            New line after rotation
        """
        p1, p2 = self.pbegin, self.pend
        if p0 is None:
            p0 = (p1 + p2) * 0.5
        p1, p2 = self.pbegin - p0, self.pend - p0
        theta = angle / 180.0 * np.pi
        m = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        p1_rot, p2_rot = np.dot(m, np.vstack((p1[:], p2[:])).T).T
        new_p1, new_p2 = Point(p1_rot) + p0, Point(p2_rot) + p0
        return Line(new_p1, new_p2)

    def __getitem__(self, i):
        return self._stackpoints[i]


if __name__ == '__main__':
    # None, None
    p1 = Point()
    print(str(p1))

    # 1, None
    p2 = Point(1, )
    print(str(p2))

    # None, 1
    p3 = Point(y=1)
    print(str(p3))

    # None, INVALID
    p4 = Point(y='a')
    print(str(p4))

    # INVALID, INVALID
    p5 = Point('a', 'b')
    print(str(p5))

    # INVALID, None
    p6 = Point(x='a')
    print(str(p6))

    # tuple
    p7 = Point((1, 2))
    print(str(p7))

    # list
    p8 = Point([1, 2])
    print(str(p8))

    # array
    p9 = Point(np.array([1, 2]))
    print(str(p9))

    # Point instance
    p0 = Point(0, 1)
    p10 = Point(p0)
    print(str(p10))

    # compare
    print(Point(1, 2) == Point(x=1, y=2))

    # projection
    a = Point(1, 1)
    b = Point(5, 3)
    p = Point(2, 5)
    p_ab = p.proj_point(a, b)
    print(p_ab)

    # distance: point to point
    print(p.distance_to_point(p_ab))

    # distance: point to line
    print(p.distance_to_line(a, b))

    # inline test
    print(p_ab.is_in_line(a, b))

    ## move
    p = Point(0, 0)
    p_moveto1 = p.move(direction=(30, 1))
    p_moveto2 = p.move(direction=(45, 1))
    p_moveto3 = p.move(direction=(60, 1))

    import matplotlib.pyplot as plt

    fig = plt.figure(1)
    ax = fig.add_subplot(111, aspect='equal', xlim=[0, 1], ylim=[0, 1])
    line1 = np.vstack([p.point, p_moveto1.point])
    line2 = np.vstack([p.point, p_moveto2.point])
    line3 = np.vstack([p.point, p_moveto3.point])
    ax.scatter(*p.point, c='r')
    ax.scatter(*p_moveto1.point, c='b', label='30')
    ax.scatter(*p_moveto2.point, c='m', label='45')
    ax.scatter(*p_moveto3.point, c='g', label='60')
    ax.plot(line1[:, 0], line1[:, 1], '--')
    ax.plot(line2[:, 0], line2[:, 1], '--')
    ax.plot(line3[:, 0], line3[:, 1], '--')
    ax.legend()
    plt.show()

    # check move
    x = Point(1, 0)
    o = Point(0, 0)
    ox = Line(x - o)
    op1 = Line(p_moveto1 - o)
    op2 = Line(p_moveto2 - o)
    op3 = Line(p_moveto3 - o)

    print(ox.angle(op1))
    print(op1.angle(ox))
    print(ox.angle(op2))
    print(ox.angle(op3))

    # line
    line = Line(0, 0)
    print(line)

    line = Line((0, 1), (1, 0))
    print(line)

    line = Line(Point(1, 0))
    print(line)

    print(Line((0, 1)) == Line((0, 0), (0, 1)))

    # cross
    line1 = Line((1, 2), (2, 1))
    line2 = Line((3, 3), (4, 4))
    print(line1.cross(line2))

    # move
    line1 = Line((1, 2), (2, 1))
    line2 = line1.move((1, 1))
    print(line1)
    print(line2)

    print(line2[:, 1])
