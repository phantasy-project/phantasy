#!/usr/bin/python
# -*- coding: utf-8 -*-

"""PV data source could be:
1. Channel finder service
2. Local data file:
    - csv
    - sqlite
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging
import os
from fnmatch import fnmatch

from phantasy.library.channelfinder import get_data_from_db
from phantasy.library.channelfinder import get_data_from_cf


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)


class DataSource(object):
    """ class represents PV data sources,
    valid data sources: 
    
    - *cfs*: channel finder service
    - *csv*: csv sheet
    - *sql*: sqlite database

    Parameters
    ----------
    source : str
        PV data source, channel finder server url or name of *csv*/*sql* file,
        source type would be automatically detected as one of *cfs*, *csv* and
        *sql*.
    
    Keyword Arguments
    -----------------
    """
    def __init__(self, source=None, **kws):
        # source and source type is None by default or failed to set source
        self.source = source

        self._get_data = {
                'cfs': self._get_cfs_data,
                'csv': self._get_csv_data,
                'sql': self._get_sql_data,
                }

        self.pvdata = self.get_data()

    @property
    def source(self):
        """str: (File/URL) name of PV data source."""
        return self._source

    @property
    def source_type(self):
        """str: name of PV data source type."""
        return self._src_type

    @source.setter
    def source(self, s):
        if not isinstance(s, (unicode, str)):
            self._source, self._src_type = None, None
            return
        ext = os.path.splitext(s)[-1].lower()
        if fnmatch(s, 'http*://*'):
            _LOGGER.info("Set source to be channel finder server address: {s}.".format(
                s=s))
            self._src_type = 'cfs'
        elif fnmatch(ext, '.sql*'):
            _LOGGER.info("Set source to be sqlite database: {s}.".format(
                s=os.path.basename(s)))
            self._src_type = 'sql'
        elif fnmatch(ext, '.csv*'):
            _LOGGER.info("Set source to be CSV table: {s}.".format(
                s=os.path.basename(s)))
            self._src_type = 'csv'
        else:
            _LOGGER.error("Cannot set PV data source with {s}, try with one \
                    of the following categories: 1) cfs URL 2) sqlite file 3) \
                    csv file.".format(s=s))
            self._src_type = None
        self._source = s

    def get_data(self, **kws):
        """Get PV data from specific source.
        
        Keyword Arguments
        -----------------
        name_filter : str or list(str)
            Only get PVs with defined PV name(s), could be Unix shell pattern(s),
            logical OR applies for list of multiple name patterns.
        prop_filter : str or list(str) or list(tuple) or list(str, tuple)
            Only get PVs with defined property names (list(str)) or
            property configurations (list(tuple)),
            could be Unix shell patterns, e.g.:
            List of str pattern(s), to filter property names:
            - ``prop_filter='elem*'``
            - ``prop_filter=['elemHandle', 'send']``
            List of tuple(s), to filter property configurations,
            (ignore invalid property names):
            - ``prop_filter=[('elemHandle', 'setpoint')]``
            - ``prop_filter=[('elemHandle', 'setpoint'), ('INVALID', 'ABC')]``
            Or mixture of the above two:
            - ``prop_filter=['elem*', ('elemHandle', 'setpoint')]``
        tag_filter : str or list(str)
            Only get PVs with defined tags, could be Unix shell patterns,
            logical AND applies for multiple tags.

        Note
        ----
        When *tag_filter* (after pattern expanding) is a list, the data
        extraction policy should be logical AND, that is returned data should
        meet all filtering conditions, rules for *prop_filter* see below.

        Returns
        -------
        ret : list
            List of PV data, for each PV data, should be of list as:
            ``string of PV name, dict of PV properties, list of PV tags``,
            if failed, return None.

        Examples
        --------
        1. Get all PVs
        >>> pvdata = get_data()
        >>> print(len(pvdata))
        1737
        >>> print(pvdata[0])
        [u'V_1:LS1_CA01:CAV1_D1127:PHA_CSET',
         {'archive': 0,
          'elemField': u'PHA',
          'elemHandle': u'setpoint',
          'elemIndex': 3,
          'elemLength': 0.24,
          'elemName': u'LS1_CA01:CAV1_D1127',
          'elemPosition': 0.4470635,
          'elemType': u'CAV',
          'epsilon': 0.0,
          'size': 0,
          'virtual': 0},
         [u'phyutil.sub.CA01', u'phyutil.sys.LINAC', u'phyutil.sys.LS1']]
        2. Get PVs with single tag and property filters
        >>> pvdata = get_data(tag_filter='phyutil.sub.CB09', prop_filter='elem*')
        >>> print(len(pvdata))
        87
        >>> print(pvdata[0])
        [u'V_1:LS1_CB09:CAV1_D1739:PHA_CSET',
         {'elemField': u'PHA',
          'elemHandle': u'setpoint',
          'elemIndex': 475,
          'elemLength': 0.3,
          'elemName': u'LS1_CB09:CAV1_D1739',
          'elemPosition': 61.6459917,
          'elemType': u'CAV'},
         [u'phyutil.sub.CB09', u'phyutil.sys.LINAC', u'phyutil.sys.LS1']]
        3. Get PVs with multiple tags and property filters
        >>> get_data(tag_filter=['phyutil.sub.CB09','phyutil.sys.LINAC'],
                     prop_filter=['elem*','size'])
        4. Get PVs with certain property configuration
        >>> get_data(prop_filter=[('elemHandle', 'setpoint')])
        5. Get PVs with certain property configuration, also only get part
        properties
        >>> get_data(prop_filter=['elem*', ('elemHandle', 'setpoint')])
        
        Note
        ----
        Always keep precise property configuration filter followed by property
        name filter, e.g. ``prop_filter=['elem*', ('elemHandle', 'setpoint')]``
        will filter PVs of ``elemHandle`` is ``setpoint``, but
        ``prop_filter=[('elemHandle', 'setpoint'), 'elem*']`` will not work.
        """
        if self._src_type is not None:
            ret = self._get_data.get(self._src_type)(**kws)
        else:
            _LOGGER.warn("Failed to get PV data from invalid source.")
            ret = None
        return ret
    
    def _get_cfs_data(self, **kws):
        """Get PV data from ChannelFinderService (URL)
        """
        return get_data_from_cf(self.source, **kws)
        
    def _get_csv_data(self, **kws):
        """Get PV data from spreadsheet (CSV)
        """
        pass

    def _get_sql_data(self, **kws):
        """Get PV data from database (SQLite)
        """
        return get_data_from_db(self.source, **kws)

