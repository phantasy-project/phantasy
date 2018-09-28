# -*- coding: utf-8 -*-

import numpy as np


class ScanDataModel(object):
    """Standardize the scan output data.

    Parameters
    ----------
    data : array
        Numpy array with the shape of `(t, h, w)`, e.g.
        `t` is iteration number, `h` is shot number, `w` is scan dimension.
    """
    def __init__(self, data=None):
       self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, z):
        """Every time data is updated, the shape, std array and mean array
        will be updated.
        """
        self._data = z
        self.t, self.h, self.w = self.shape
        self._std = self._data.std(axis=1)
        self._avg = self._data.mean(axis=1)

    @property
    def shape(self):
        return self._data.shape

    def get_xerr(self, **kws):
        if kws == {}:
            return self._std[:, 0]
        else:
            return self._data.std(axis=1, **kws)[:, 0]

    def get_yerr(self, **kws):
        if kws == {}:
            return self._std[:, 1]
        else:
            return self._data.std(axis=1, **kws)[:, 1]

    def get_xavg(self):
        return self._avg[:, 0]

    def get_yavg(self):
        return self._avg[:, 1]
