#!/usr/bin/python
# -*- coding: utf-8 -*-

""" util for handling channels/PVs

:author: Tong Zhang <zhangt@frib.msu.edu>
:time: 2016-11-21 11:54:39 AM EST
"""

class DataSource(object):
    """ class represents PV data sources,
    valid data sources: 
    
    * *cfs*: channel finder service
    * *csv*: csv sheet
    * *sql*: sqlite database

    :param source: PV data source, one of listed valid data sources
    :param kws: other keyword parameters
    """
    def __init__(self, source, **kws):
        pass
