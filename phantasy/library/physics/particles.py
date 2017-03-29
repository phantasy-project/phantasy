#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data simulation, to test algorithms utilized in diagnostics.

Tong Zhang <zhangt@frib.msu.edu>
2017-03-27 11:22:25 AM EDT
"""

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
        Name of data file to load distribution, if *distfile* is valid,
        the internal data generation would be ignored.
    """
    def __init__(self, x0=0, y0=0, sx=0.1, sy=0.1, N=1000, **kws):
        self.distype = None
        distfile = kws.get('distfile', None)
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
                    cxy = rho*sx*sy
                else:
                    cxy = 0
                cov = [[sx**2, cxy], [cxy, sy**2]]

            self.distype = 'gaussian'
            self.particles = Distribution.generate_gaussian_distrubution(
                    mean, cov, N)
        else:
            print("Load distribution from '{}'".format(distfile))

    def load_distfile(self, distfile):
        try:
            self._x, self._y = np.loadtxt(distfile)
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
        """
        if kws.get('norm', None) is not None:
            return np.corrcoef(xarr, yarr)
        else:
            return np.cov(xarr, yarr)

    def get_cov(self, **kws):
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


if __name__ == '__main__':
    # default
    print("{0}{1}{0}".format('-'*10, 'default'))
    ds = Distribution()
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # internal gaussian w/o correlation
    print("{0}{1}{0}".format('-'*10, 'gaussian/rho=0'))
    ds = Distribution(1,1,2,3,50000)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # internal gaussian with correlation
    print("{0}{1}{0}".format('-'*10, 'gaussian/rho=0.5'))
    ds = Distribution(1,1,2,3,50000, rho=0.5)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # load external
    print("{0}{1}{0}".format('-'*10, 'external file'))
    ds = Distribution(distfile='../../../tests/temp/dist.dat')
    print(ds.distype)
    print(ds.get_cov())
    print(ds.get_cov(norm='True'))
    ds.draw()

    # resample
    print("Resample external loaded dist")
    ds1 = ds.resample()
    ds1.draw()
