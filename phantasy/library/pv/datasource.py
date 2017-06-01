#!/usr/bin/python
# -*- coding: utf-8 -*-

"""PV data source could be:

1. Channel finder service
2. Local data file:

    - csv
    - sqlite
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
from fnmatch import fnmatch

from phantasy.library.channelfinder import get_data_from_cf
from phantasy.library.channelfinder import get_data_from_db
from phantasy.library.channelfinder import get_data_from_tb
from phantasy.library.channelfinder import write_cfs
from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import write_json
from phantasy.library.channelfinder import write_tb

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, " \
                "Michigan State University"
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
    username : str
        Username of channel finder service
    password : str
        Password of username.
    """

    def __init__(self, source=None, **kws):
        # source and source type is None by default or failed to set source
        self.source = source

        self._get_data = {
            'cfs': self._get_cfs_data,
            'csv': self._get_csv_data,
            'sql': self._get_sql_data,
        }

        self._pvdata = None
        if source is not None:
            self._pvdata = self.get_data()

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

    @property
    def pvdata(self):
        """List(dict): PV data got from source."""
        return self._pvdata

    @pvdata.setter
    def pvdata(self, data):
        self._pvdata = data

    def get_data(self, **kws):
        """Get PV data from specific source.

        Keyword Arguments
        -----------------
        name_filter : str or list(str)
            Only get PVs with defined PV name(s), could be Unix shell pattern,
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
        ret : list(dict) or None
            List of dict, each dict element is of the format:
            ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.

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

        >>> pvdata = get_data(tag_filter='phyutil.sub.CB09',
        >>>                   prop_filter='elem*')
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
        if ret is not None:
            self.pvdata = ret
        return ret

    def _get_cfs_data(self, **kws):
        """Get PV data from ChannelFinderService (URL)
        """
        return get_data_from_cf(self.source, **kws)

    def _get_csv_data(self, **kws):
        """Get PV data from spreadsheet (CSV)
        """
        return get_data_from_tb(self.source, **kws)

    def _get_sql_data(self, **kws):
        """Get PV data from database (SQLite)
        """
        return get_data_from_db(self.source, **kws)

    def dump_data(self, fname, ftype, **kws):
        """Dump PV data to file or CFS, defined by *ftype*, support types:

        - *sql*: SQLite database
        - *csv*: CSV spreadsheet
        - *json*: JSON string file
        - *cfs*: Channel Finder Service

        Parameters
        ----------
        fname : str
            File name or CFS url.
        ftype : str
            Dumped file type, supported types: sql*, *csv*, *json*, *cfs*.

        See Also
        --------
        dump_data
        """
        if self._pvdata is None:
            _LOGGER.warn("PV data is not available, get_data() first.")
            return None

        dump_data(self._pvdata, fname, ftype, **kws)

    def map_property_name(self, name_map, **kws):
        """Adjust property name(s) according to *name_map*.

        Parameters
        ----------
        name_map : dict
            Keys are original name(s), and values are new name(s).
        """
        if self._pvdata is None:
            _LOGGER.warn("PV data is not available, get_data() first.")
            return None

        for r in self._pvdata:
            p_list = []
            for p in r['properties']:
                for k, v in name_map.items():
                    if k == p['name']:
                        p['name'] = v
                p_list.append(p)
            r['properties'] = p_list


def dump_data(data, fname, ftype, **kws):
    """Dump PV data to file or CFS, defined by *ftype*, support types:

    - *sql*: SQLite database
    - *csv*: CSV spreadsheet
    - *json*: JSON string file
    - *cfs*: Channel Finder Service

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    fname : str
        File name or CFS url.
    ftype : str
        Dumped file type, supported types: sql*, *csv*, *json*, *cfs*.
    """
    dump_meth = {'csv': write_tb,
                 'sql': write_db,
                 'json': write_json,
                 'cfs': write_cfs}
    dump_meth.get(ftype)(data, fname, **kws)
