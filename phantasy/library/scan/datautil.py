#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""utils for data crunching, saving.
"""

import numpy as np


class ScanDataFactory(object):
    """Post processor of data from scan server.

    Parameters
    ----------
    data : dict
        Raw data retrieving from scan server regarding scan ID, after
        completing certain scan task.
    n_sample : int
        Sample number for every scan device setup.
    """

    def __init__(self, data, n_sample):
        self._raw_data = data
        self._n = n_sample
        self._rebuild_data()

    @property
    def raw_data(self):
        """dict: Dict of array, raw scan data."""
        return self._raw_data

    @property
    def data(self):
        """dict: Dict of array, raw scan data after postprocessing."""
        return self._data

    def _rebuild_data(self):
        """Rebuild raw_data
        """
        self._data = {k: np.array(v.get('value')).reshape(-1, self._n)
                      for k, v in self._raw_data.iteritems()}

    def get_average(self, name):
        """Get average.

        Parameters
        ----------
        name : str
            Key name of raw_data.
        """
        return self._data.get(name).mean(axis=1)

    def get_errorbar(self, name):
        """Get errorbar

        Parameters
        ----------
        name : str
            Key name of raw_data.
        """
        return self._data.get(name).std(axis=1)

    def get_all_names(self):
        """Get all key names of raw_data.

        Returns
        -------
        ret : list
            List of keys.
        """
        return self._data.keys()

    def save(self, ext='dat'):
        """
        """
        pass
