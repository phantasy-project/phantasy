#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data simulation, to test algorithms utilized in diagnostics.

Tong Zhang <zhangt@frib.msu.edu>
2017-03-27 11:22:25 AM EDT
"""

from phantasy.library.physics import Point

import numpy as np


class Distribution(object):
    """Particle distribution for transverse plane, i.e. ``x-o-y`` plane,
    default is Gaussian distribution.

    Parameters
    ----------
    x0 : float
        Mean value along ``x`` direction.
    y0 : float
        Mean value along ``y`` direction.
    sx : float
        Standard deviation along ``x`` direction.
    sy : float
        Standard deviation along ``y`` direction.
    N : int
        Total point number of particle distribution.

    Keyword Arguments
    -----------------
    mean : list
        Central point, ``[x0, y0]``, overrides *x0* and *y0*.
    cov : list
        Covariance matrix, overrides *sx* and *sy*.
    rho : float
        Correlation between ``x`` and ``y``, should be within ``[-1, 1]``.
    distfile : string
        Name of data file to load distribution, contains x and y data,
        if *distfile* is valid, the internal data generation would be
        ignored.
    distdata : array
        Array with shape of ``(2,n)`` to initialize distribution.
    """

    def __init__(self, x0=0, y0=0, sx=0.1, sy=0.1, N=1000, **kws):
        self.distype = None
        distfile = kws.get('distfile', None)
        distdata = kws.get('distdata', None)
        # try to load data from array
        if distdata is not None:
            self.particles = distdata
        else:
            # generate internally
            if not self.load_distfile(distfile):
                self._x, self._y = None, None

                if kws.get('mean', None) is not None:
                    mean = kws.get('mean')
                else:
                    mean = [x0, y0]

                if kws.get('cov', None) is not None:
                    cov = kws.get('cov')
                else:
                    rho = kws.get('rho', None)
                    if -1.0 <= rho <= 1.0:
                        cxy = rho * sx * sy
                    else:
                        cxy = 0
                    cov = [[sx ** 2, cxy], [cxy, sy ** 2]]

                self.distype = 'gaussian'
                self.particles = Distribution.generate_gaussian_distrubution(
                    mean, cov, N)
            else:
                # load from external file
                print("Load distribution from '{}'".format(distfile))

    def load_distfile(self, distfile):
        try:
            data = np.loadtxt(distfile)
            if data.shape[0] == 2:
                self._x, self._y = data
            else:
                self._x, self._y = data.T
            self.distype = 'external'
            return True
        except:
            return False

    @property
    def particles(self):
        """tuple: Array of x, y distribution."""
        return self._x, self._y

    @particles.setter
    def particles(self, p):
        self._x, self._y = p

    @staticmethod
    def generate_gaussian_distrubution(mean, cov, N):
        """Generate random two-dimensional distribution.
        """
        x, y = np.random.multivariate_normal(mean, cov, N).T
        return x, y

    def draw(self):
        """Draw particles.
        """
        if self._x is None:
            print("Particle distribution is not ready yet.")
            return 1
        else:
            import matplotlib.pyplot as plt
            x, y = self.particles
            plt.plot(x, y, '.')
            plt.show()

    @staticmethod
    def get_covariance(xarr, yarr, **kws):
        """Get covariance matrix of 'x' and 'y' array.

        Parameters
        ----------
        xarr : array
            X array.
        yarr : array
            Y array.

        Keyword Arguments
        -----------------
        norm :
            If set, return normalized covariance.

        Returns
        -------
        ret : array
            Covariance matrix.
        """
        if kws.get('norm', None) is not None:
            return np.corrcoef(xarr, yarr)
        else:
            return np.cov(xarr, yarr)

    def get_cov(self, **kws):
        """Return covariance of x and y of distribution,
        if *norm* keyword is set, return normalized one.
        """
        return Distribution.get_covariance(self._x, self._y, **kws)

    def resample(self):
        """Generate normal distribution by resampling.

        Returns
        -------
        ret : Distribution
            New Distribution instance.
        """
        mean = [np.mean(self._x), np.mean(self._y)]
        cov = np.cov(self._x, self._y)
        N = self._x.size
        return Distribution(mean=mean, cov=cov, N=N)

    def rotate(self, angle, p0=None):
        """Rotate particle distribution of *angle* w.r.t. *p0*.

        Parameters
        ----------
        angle : float
            Anti-clockwised rotating angle, degree.
        p0 : Point
            Rotating central point, ``(0,0)`` by default.

        Returns
        -------
        ret : Distribution
            New Distribution after rotation.
        """
        if p0 is None:
            p0 = Point(0, 0)

        data0 = np.array(self.particles)
        disp = np.tile(p0[:], [int(data0.size / 2), 1]).T

        theta = angle / 180.0 * np.pi
        m = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
        data1 = np.dot(m, data0 - disp) + disp
        return Distribution(distdata=data1)

    def __repr__(self):
        x, y = self._x, self._y
        cov = np.cov(x, y)
        x0, y0 = x.mean(), y.mean()
        sx, sy = x.std(ddof=1), y.std(ddof=1)
        rho_xy = cov[0, 1] / cov[0, 0] ** 0.5 / cov[1, 1] ** 0.5
        ret = '(x_0, y_0) = ({0:.3f},{1:.3f})\n'.format(x0, y0)
        ret += 'sigma_x = {0:.3f}\n'.format(sx)
        ret += 'sigma_y = {0:.3f}\n'.format(sy)
        ret += '(x,y) correlation = {0:.3f}'.format(rho_xy)
        return ret


if __name__ == '__main__':
    # default
    print("{0}{1}{0}".format('-' * 10, 'default'))
    ds = Distribution()
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # internal gaussian w/o correlation
    print("{0}{1}{0}".format('-' * 10, 'gaussian/rho=0'))
    ds = Distribution(1, 1, 2, 3, 50000)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # internal gaussian with correlation
    print("{0}{1}{0}".format('-' * 10, 'gaussian/rho=0.5'))
    ds = Distribution(1, 1, 2, 3, 50000, rho=0.5)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # load external
    print("{0}{1}{0}".format('-' * 10, 'external file'))
    ds = Distribution(distfile='../../../tests/temp/dist.dat')
    print(ds.distype)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # resample
    print("Resample external loaded dist")
    ds1 = ds.resample()
    ds1.draw()
