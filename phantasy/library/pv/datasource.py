#!/usr/bin/python
# -*- coding: utf-8 -*-

"""PV data source could be:

1. Channel finder service
2. Local data file:

    - csv
    - sqlite
"""

import logging
import os
import requests
from fnmatch import fnmatch

from phantasy.library.channelfinder import get_data_from_db
from phantasy.library.channelfinder import get_data_from_tb
from phantasy.library.channelfinder import write_db
from phantasy.library.channelfinder import write_json
from phantasy.library.channelfinder import write_tb
from phantasy.library.misc import cofetch

_LOGGER = logging.getLogger(__name__)


from phantasy.library.channelfinder import HAS_CFC
if HAS_CFC:
    from channelfinder import ChannelFinderClient
    from phantasy.library.channelfinder import get_data_from_cf
    from phantasy.library.channelfinder import write_cfs

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, " \
                "Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"


class DataSource(object):
    """PV data sources,
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

        self._pvdata = None
        self._tag_list = None
        self._prop_list = None

        self._get_data = {
            'csv': self._get_csv_data,
            'sql': self._get_sql_data,
        }

        self._init_data = {
            'csv': self._init_csv_data,
            'sql': self._init_sql_data,
        }
        if HAS_CFC:
            self._get_data['cfs'] = self._get_cfs_data
            self._init_data['cfs'] = self._init_cfs_data

        self.source = source

    def init_data(self, **kws):
        """Initialize data source.
        """
        self._init_data.get(self._src_type)(**kws)

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
        if not isinstance(s, str):
            self._source, self._src_type = None, None
            return
        ext = os.path.splitext(s)[-1].lower()
        if fnmatch(s, 'http*://*'):
            _LOGGER.info(f"Set source to be channel finder server address: {s}.")
            self._src_type = 'cfs'
        elif fnmatch(ext, '.sql*'):
            _LOGGER.info(f"Set source to be sqlite database: {os.path.basename(s)}.")
            self._src_type = 'sql'
        elif fnmatch(ext, '.csv*'):
            _LOGGER.info(f"Set source to be CSV table: {os.path.basename(s)}.")
            self._src_type = 'csv'
        else:
            _LOGGER.error(f"Cannot set PV data source with {s}, try with one \
                    of the following categories: 1) cfs URL 2) sqlite file 3) \
                    csv file.")
            self._src_type = None
        self._source = s
        # init data
        self.init_data()

    @property
    def pvdata(self):
        """List(dict): PV data got from source."""
        return self._pvdata

    @pvdata.setter
    def pvdata(self, data):
        self._pvdata = data

    @property
    def prop_list(self):
        """List(str): Properties list."""
        return self._prop_list

    @prop_list.setter
    def prop_list(self, l):
        self._prop_list = l

    @property
    def tag_list(self):
        """List(str): Tags list."""
        return self._tag_list

    @tag_list.setter
    def tag_list(self, l):
        self._tag_list = l

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
        prop_list : list
            Properties list.
        tag_list : list
            Tags list.
        raw_data : list
            Lsit of PV data.
        size : int
            Length of returned list.
        ifrom : int
            Starting index of list.

        Note
        ----
        1. When *tag_filter* (after pattern expanding) is a list, the data
           extraction policy should be logical AND, that is returned data
           should meet all filtering conditions, rules for *prop_filter* see
           below.
        2. If *prop_list* and *tag_list* are not given, the ones created at
           ``init_data`` will be used.
        3. *size* and *ifrom* are only valid when source type if ``cfs``, and
           *raw_data* is not defined.
        4. If *raw_data* is defined, apply filters on *raw_data*.

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
        prop_list = kws.get('prop_list', self.prop_list)
        tag_list = kws.get('tag_list', self.tag_list)

        if self._src_type is not None:
            ret = self._get_data.get(self._src_type)(prop_list=prop_list,
                    tag_list=tag_list, **kws)
        else:
            _LOGGER.warning("Failed to get PV data from invalid source.")
            ret = None
        if ret is not None:
            self.pvdata = ret
        return ret

    if HAS_CFC:
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
            _LOGGER.warning("PV data is not available, get_data() first.")
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
            _LOGGER.warning("PV data is not available, get_data() first.")
            return None

        for r in self._pvdata:
            p_list = []
            for p in r['properties']:
                for k, v in name_map.items():
                    if k == p['name']:
                        p['name'] = v
                p_list.append(p)
            r['properties'] = p_list

    if HAS_CFC:
        def _init_cfs_data(self, **kws):
            username = kws.get('username', None)
            password = kws.get('password', None)
            cfc = ChannelFinderClient(BaseURL=self.source,
                                      username=username,
                                      password=password)
            c_url = cfc.get_resource('channel')
            t_url = cfc.get_resource('tag')
            p_url = cfc.get_resource('property')

            resource_data = _cofetch_data([c_url, t_url, p_url])

            prop_list = sorted([p['name'] for p in resource_data[p_url]])
            tag_list = sorted([t['name'] for t in resource_data[t_url]])
            raw_data = resource_data[c_url]

            self._prop_list = prop_list
            self._tag_list = tag_list
            self._pvdata = raw_data

    def _init_csv_data(self, **kws):
        pass

    def _init_sql_data(self, **kws):
        pass

    def __repr__(self):
        if self.source is None:
            return "DataSource [] to be initialized..."
        elif self.pvdata is None:
            return f"DataSource: [{self.source_type.upper()}] at '{self.source}', load data by `get_data`."
        else:
            return f"DataSource: [{self.source_type.upper()}] at '{self.source}', loaded data: {len(self.pvdata)} records."


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
                 'json': write_json}
    if HAS_CFC:
        dump_meth['cfs'] = write_cfs
    dump_meth.get(ftype)(data, fname, **kws)


@cofetch
def _cofetch_data(url):
    return requests.get(url, verify=False).json()
