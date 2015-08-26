# encoding: UTF-8

'''
Utilities for reading machine settings from various sources. 

:author: Dylan Maxwell <maxwelld@frib.msu.edu>
:date: 2015-06-02

:copyright: Copyright (c) 2015, Facility for Rare Isotope Beams
'''


import json

from copy import deepcopy
from collections import OrderedDict


class Settings(OrderedDict):
    """Settings is a simple extention of :class:`OrderedDict` with
       the addition of some utility functions for use within the
       phylib library.
    """
    def __init__(self, settingsPath=None):
        super(Settings, self).__init__()
        if settingsPath is not None:
            with open(settingsPath, "r") as fp:
                self.readfp(fp)


    def readfp(self, fp):
        """Read settings from file-like object in JSON format

           :param fp: file-like object to read settings
        """
        self.update(json.load(fp, object_pairs_hook=OrderedDict))

    def __deepcopy__(self, memo):
        """Due to the custom class initializer the default deepcopy
           implementation is broken. Override it to make it work again.
        """
        s = Settings()
        s.update(deepcopy(self.items(), memo))
        return s

