#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Other support utils.
"""
import logging
from bisect import bisect
from fnmatch import fnmatch
import getpass
from datetime import datetime
import os
import tempfile
import sys

if sys.version_info[:2] >= (3, 8):
    from collections.abc import MutableMapping as DictMixin
else:
    from collections import MutableMapping as DictMixin

import dateutil.relativedelta as relativedelta

from flame import Machine

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams, " \
                "Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)


def _flatten(nnn):
    """ flatten recursively defined list or tuple

    :param nnn: recursively defined list or tuple
    :return: a generator object

    :Example:

    >>> l0 = [1,2,3,[4,5],[6,[7,8,[9,10,['x',['y']]]]]]
    >>> l1 = list(_flatten(l0))
    >>> print(l1)
    [1,2,3,4,5,6,7,8,9,10,'x','y']
    """
    for nn in nnn:
        if isinstance(nn, (list, tuple)):
            for n in flatten(nn):
                yield (n)
        else:
            yield (nn)


def flatten(nnn):
    """ flatten recursively defined list or tuple

    :param nnn: recursively defined list or tuple
    :return: flattened list

    :Example:

    >>> l0 = [1,2,3,[4,5],[6,[7,8,[9,10,['x',['y']]]]]]
    >>> l1 = flatten(l0)
    >>> print(l1)
    [1,2,3,4,5,6,7,8,9,10,'x','y']
    """
    return list(_flatten(nnn))


def get_intersection(*args):
    """Get the intersection of all input parameters, separated by comma, ignore
    empty list or tuple.

    Returns
    -------
    res : list

    Note
    ----
    The order of the returned list may be not consistent with the input.

    Examples
    --------
    >>> a, b, c = [], [], []
    >>> print(get_intersection(a, b, c))
    []
    >>> a, b, c = [1], [2], []
    >>> print(get_intersection(a, b, c))
    []
    >>> a, b, c = [1, 2], [2], []
    >>> print(get_intersection(a, b, c))
    [2]
    >>> a, b, c = [1, 2], [2], [2, 3]
    >>> print(get_intersection(a, b, c))
    [2]
    >>> a, b, c = [1, 2], [3, 4], [2, 3]
    >>> print(get_intersection(a, b, c))
    []
    """
    vs = (v for v in args if v != list() and v != tuple())
    s = set(next(vs, ()))
    if s == set():
        return list()
    for v in vs:
        s = s.intersection(v)
    return list(s)


def machine_setter(_latfile=None, _machine=None, _handle_name=None):
    """ set flame machine, prefer *_latfile*

    :return: FLAME machine object
    """
    if _latfile is not None:
        try:
            m = Machine(open(_latfile, 'r'))
        except:
            if _machine is None:
                _LOGGER.error("{}: Failed to initialize flame machine".format(
                    _handle_name))
                return None
            else:
                _LOGGER.warning("{}: Failed to initialize flame machine, "
                                "use _machine instead".format(_handle_name))
                m = _machine
    else:
        if _machine is None:
            return None
        else:
            m = _machine
    return m


def bisect_index(x, val):
    """Get the *val* index in sorted *x*.

    Parameters
    ----------
    x : List, sequence
        Sorted sequence.
    val :
        Value to be located.

    Returns
    -------
    i : int
        Index of *val* that should be inserted into *x*.

    Examples
    --------
    >>> x = [0.2070635,0.51132684,0.6433303399999999,
             0.74333034,0.74333034,0.9867243400000001,
             1.7663703400000001]
    >>> bisect_index(x, 1.5)
    6
    >>> bisect_index(x, 0.5)
    1
    >>> x[1:6]
    [0.51132684, 0.6433303399999999, 0.74333034, 0.74333034,
     0.9867243400000001]
    """
    return bisect(x, val)


def pattern_filter(x, pattern):
    """Get sub sequence from sequence by applying filter.

    Parameters
    ----------
    x : sequence
        List or tuple to be filtered.
    pattern : str
        Unix shell style pattern to be as filter.

    Returns
    -------
    ret : List
        List filtered out.

    Examples
    --------
    >>> a = ['BPM', 'BEND', 'VCOR', 'PM', 'HCOR']
    >>> pattern_filter(a, 'BP*')
    ['BPM']
    >>> pattern_filter(a, '*PM*')
    ['BPM', 'PM']
    >>> pattern_filter(a, '*COR')
    ['VCOR', 'HCOR']
    """
    return [i for i in x if fnmatch(i, pattern)]


def expand_list_to_dict(x, keys):
    """Expand list to dict according to following rule:

    1. If list element is string, treat it as Unix shell pattern,
       to match *keys*, and expand it as tuple like ``(k, None)``;
    2. If list element is tuple, test if the first element of tuple
       is in the *keys* list, if not just ignore;
    3. Convert final list of tuple to be a dict.

    Parameters
    ----------
    x : list
        List of (tuple and str).
    keys : list
        List of keys.

    Returns
    -------
    ret : dict

    Examples
    --------
    >>> x = ['k?', ('k2', 3), ('a1', 's')]
    >>> keys = ['k1', 'k2', 'k3', 'k4']
    >>> print(expand_list_to_dict(x, keys))
    {'k1': None, 'k2': 3, 'k3': None, 'k4': None}
    """
    ret = []
    for i in x:
        if not isinstance(i, tuple):
            ret.extend([(k, None) for k in keys if fnmatch(k, i)])
        else:
            if i[0] in keys:
                ret.append(i)
    return dict(ret)


def simplify_data(raw_data):
    """Convert CFS formatted data into simple tuple.

    Parameters
    ----------
    raw_data : dict or list(dict)
        Each dict element is of the following format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.

    Returns
    -------
    ret : list or list(list)
        Each list element is of the following format:
        PV name (str), PV properties (dict), PV tags (list(str))

    Note
    ----
    If the input *raw_data* is a single dict, the returned on is a single list.

    See Also
    --------
    get_data_from_tb, get_data_from_db, get_data_from_cf
    """
    if isinstance(raw_data, dict):
        retval = [
            raw_data['name'],
            {p['name']: p['value'] for p in raw_data['properties']},
            [t['name'] for t in raw_data['tags']]
        ]
    else:
        retval = []
        for r in raw_data:
            new_rec = [
                r['name'],
                {p['name']: p['value'] for p in r['properties']},
                [t['name'] for t in r['tags']]
            ]
            retval.append(new_rec)
    return retval


def complicate_data(raw_data, **kws):
    """Convert simple tuple PV data into CFS formatted data.

    Parameters
    ----------
    raw_data : list or list(list)
        Each list element is of the format:
        ``PV name (str), PV properties (dict), PV tags (list(str))``

    Keyword Arguments
    -----------------
    owner : str
        Owner of the data.

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.

    See Also
    --------
    :func:`~phantasy.library.channelfinder.io.get_data_from_tb`
    :func:`~phantasy.library.channelfinder.io.get_data_from_db`
    :func:`~phantasy.library.channelfinder.io.get_data_from_cf`
    """
    owner = kws.get('owner', getpass.getuser())
    if isinstance(raw_data, list):
        pv_name, pv_props, pv_tags = raw_data
        retval = {'name': pv_name,
                  'owner': owner,
                  'properties': [{'name': k, 'value': v, 'owner': owner}
                                 for k, v in pv_props.items()],
                  'tags': [{'name': t, 'owner': owner} for t in pv_tags]
                  }
    else:
        retval = []
        for pv_name, pv_props, pv_tags in raw_data:
            new_rec = {'name': pv_name,
                       'owner': owner,
                       'properties': [{'name': k, 'value': v, 'owner': owner}
                                      for k, v in pv_props.items()],
                       'tags': [{'name': t, 'owner': owner} for t in pv_tags],
                       }
            retval.append(new_rec)
    return retval


class SpecialDict(DictMixin):
    """New dict class to support dynamic features.

    1: Initialize class with keyword arguments (meta) defined properties;
    2: New attributes could be dynamically added by assigning new k,v to (meta);
    """

    def __init__(self, meta, obj, *args, **kwargs):
        self.meta = meta
        self.obj = obj
        self.obj.__dict__.update(meta)

    def __setitem__(self, k, v):
        self.meta.update({k: v})
        self.obj.__dict__.update({k: v})

    def __getitem__(self, k):
        return self.meta.get(k, None)

    def keys(self):
        return self.meta.keys()

    def __repr__(self):
        return str(self.meta)

    def __iter__(self):
        return iter(self.meta)

    def __len__(self):
        return len(self.meta)

    def __delitem__(self, k):
        del self.meta[k]


def parse_dt(dt, ref_date=None, epoch=None):
    """Parse delta time defined by *dt*, which is approching plain English,
    e.g. '1 hour and 30 mins ago', return date time object.

    Parameters
    ----------
    dt : str
        Relative timestamp w.r.t. current time available units: *years*,
        *months*, *weeks*, *days*, *hours*, *minutes*, *seconds*,
        *microseconds*, and some unit alias: *year*, *month*, *week*, *day*,
        *hour*, *minute*, *second*, *microsecond*, *mins*, *secs*, *msecs*,
        *min*, *sec*, *msec*, could be linked by string 'and' or ',',
        ended with 'ago', e.g. '5 mins ago', '1 hour and 30 mins ago'.
    ref_date :
        Datetime object, default one is now.
    epoch : True or False
        If return date time as seconds since Epoch.

    Warning
    -------
    Only support integer number when defining time unit.

    Returns
    -------
    ret : date
        Datetime object.

    Examples
    --------
    >>> dt = '1 month, 2 weeks, 4 hours, 7 mins and 10 secs ago'
    >>> print(parse_dt(dt))
    datetime.datetime(2016, 12, 10, 12, 30, 41, 833955)
    """
    enable_epoch = False if epoch is None else epoch
    if ref_date is None:
        timenow = datetime.now()
    elif isinstance(ref_date, datetime):
        timenow = ref_date
    else:
        raise TypeError("Invalid date time variable.")

    time_unit_table = {'years': 'years', 'months': 'months', 'weeks': 'weeks',
                       'days': 'days', 'hours': 'hours', 'minutes': 'minutes',
                       'seconds': 'seconds', 'microseconds': 'microseconds',
                       'year': 'years', 'month': 'months', 'week': 'weeks',
                       'day': 'days', 'hour': 'hours', 'minute': 'minutes',
                       'second': 'seconds', 'microsecond': 'microseconds',
                       'min': 'minutes', 'sec': 'seconds',
                       'msec': 'microseconds', 'mins': 'minutes',
                       'secs': 'seconds', 'msecs': 'microseconds'}

    dt_dict = {}
    dt_tuple = dt.replace('and', ',').replace('ago', ',').strip(' ,').split(',')
    for part in dt_tuple:
        v, k = part.strip().split()
        dt_dict[time_unit_table[k]] = int(v)

    dt = relativedelta.relativedelta(**dt_dict)

    retro_datetime = timenow - dt
    if enable_epoch:
        retval = (retro_datetime - datetime(1970, 1, 1)).total_seconds()
    else:
        retval = retro_datetime

    return retval


def epoch2human(ts, **kws):
    """Convert epoch time to human friendly format.

    Parameters
    ----------
    ts : float
        Time in epoch format.

    keyword Arguments
    -----------------
    fmt : str
        Format to convert, default is `%Y-%m-%d %H:%M:%S.%f`.

    Returns
    -------
    t : str
        Converted time string.
    """
    fmt = "%Y-%m-%d %H:%M:%S.%f" if kws.get('fmt', None) is None else kws.get('fmt')
    return datetime.fromtimestamp(ts).strftime(fmt)


def convert_epoch(epoch_ts, ts_format='raw'):
    if ts_format == 'epoch':
        return epoch_ts
    elif ts_format == 'human':
        return epoch2human(epoch_ts)
    elif ts_format == 'raw':
        return datetime.fromtimestamp(epoch_ts)
    else:
        _LOGGER.warning("Unknown timestamp format, return orignal one.")
        return epoch_ts


class QCallback(object):
    def __init__(self, data_queue, status_queue):
        self.data_queue = data_queue
        self.status_queue = status_queue

    def __call__(self, **kws):
        val = kws.get('value')
        ts = kws.get('timestamp')
        self.data_queue.put((val, ts))
        if self.data_queue.full():
            idx, obj = kws.get('cb_info')
            obj.remove_callback(idx)
            self.status_queue.put(1)


def truncate_number(x, n):
    v = '{0:.{1}f}'.format(x, n)
    return float(v)


def create_tempdir(mode='ts', ts_fmt="%H%M%S", dir="/tmp", prefix="_"):
    """Create temp directory, mode: 'ts', 'str'.

    See Also
    --------
    create_tempfile
    """
    if mode == 'ts':
        dirname = datetime.strftime(datetime.now(), ts_fmt)
        tmpdir = os.path.join(dir, "{}{}".format(prefix, dirname))
        i = 1
        while os.path.exists(tmpdir):
            tmpdir = '{}_{}'.format(tmpdir, i)
            i += 1
        os.makedirs(tmpdir, mode=0o700)
    else:
        tmpdir = tempfile.mkdtemp(prefix=prefix, dir=dir)
    return tmpdir


def create_tempfile(mode='ts', ts_fmt="%H%M%S", dir="/tmp", prefix="_",
                    suffix=""):
    """Create temp file, mode: 'ts', 'str'.

    See Also
    --------
    create_tempdir
    """
    if mode == 'ts':
        fn = datetime.strftime(datetime.now(), ts_fmt)
        tmpfile = os.path.join(dir, "{}{}{}".format(prefix, fn, suffix))
        i = 1
        while os.path.exists(tmpfile):
            tmpfile = '{}_{}'.format(tmpfile, i)
            i += 1
        os.mknod(tmpfile, mode=0o600)
    else:
        _, tmpfile = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=dir)
    return tmpfile


def find_conf(conf_file):
    """Find configuration file, searching the following locations:
    * ~/.phantasy/<conf_file>
    * /etc/phantasy/<conf_file>
    * package location: phantasy/config/<conf_file>

    Parameters
    ----------
    conf_file : str
        Name of config file, e.g. .ini.

    Returns
    -------
    r : str
        Config path or None.
    """
    home_conf = os.path.expanduser("~/.phantasy/{}".format(conf_file))
    sys_conf = "/etc/phantasy/{}".format(conf_file)
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, '../../config/{}'.format(conf_file))
        try:
            assert os.path.isfile(path)
        except AssertionError:
            return None
        else:
            return os.path.abspath(path)
