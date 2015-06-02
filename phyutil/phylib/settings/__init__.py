# encoding: UTF-8

'''
Utilities for reading machine settings from various sources. 

:author: Dylan Maxwell <maxwelld@frib.msu.edu>
:date: 2015-06-02

:copyright: Copyright (c) 2015, Facility for Rare Isotope Beams
'''


import json

from collections import OrderedDict


class Settings(OrderedDict):
    """Settings is a simple extention of :class:`OrderedDict` with
       the addition of some utility functions for use within the
       phylib library.
    """
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)


    def readfp(self, fp):
        """Read settings from file-like object in JSON format

           :param fp: file-like object to read settings
        """
        self.update(json.load(fp, object_pairs_hook=OrderedDict))

