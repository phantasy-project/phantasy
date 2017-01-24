#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Other support utils.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging
from bisect import bisect
from fnmatch import fnmatch
import getpass
from UserDict import DictMixin
from datetime import datetime

import dateutil.relativedelta as relativedelta

from flame import Machine


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016, Facility for Rare Isotope beams, Michigan State University"
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
                yield(n)
        else:
            yield(nn)


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


def get_intersection(**kws):
    """Get the intersection of all input keyword parameters, ignore
    empty list or tuple.

    Returns
    -------
    res : list
    
    Examples
    --------
    >>> a, b, c = [], [], []
    >>> print(get_intersection(a=a,b=b,c=c))
    []
    >>> a, b, c = [1], [2], []
    >>> print(get_intersection(a=a,b=b,c=c))
    []
    >>> a, b, c = [1,2], [2], []
    >>> print(get_intersection(a=a,b=b,c=c))
    [2]
    >>> a, b, c = [1,2], [2], [2,3]
    >>> print(get_intersection(a=a,b=b,c=c))
    [2]
    >>> a, b, c = [1,2], [3,4], [2,3]
    >>> print(get_intersection(a=a,b=b,c=c))
    []
    """
    s = set()
    for k in kws:
        v = kws.get(k, [])
        if s == set() or v == []:
            s = s.union(v)
        else:
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
                _LOGGER.error("{}: Failed to initialize flame machine".format(_handle_name))
                return None
            else:
                _LOGGER.warning("{}: Failed to initialize flame machine, use _machine instead".format(_handle_name))
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
    """Convert CFS formated data into simple tuple.
    
    Parameters
    ----------
    raw_data : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]

    Returns
    -------
    ret : list(list)
        List of list, each list element is of the format:
        PV name (str), PV properties (dict), PV tags (list(str))

    See Also
    --------
    get_data_from_tb, get_data_from_db, get_data_from_cf
    """
    retval = []
    for r in raw_data:
        new_rec = [
                    r['name'], 
                    {p['name']:p['value'] for p in r['properties']},
                    [t['name'] for t in r['tags']]
        ]
        retval.append(new_rec)
    return retval


def complicate_data(raw_data, **kws):
    """Convert simple tuple PV data into CFS formatted data.

    Parameters
    ----------
    raw_data : list(list)
        List of list, each list element is of the format:
        PV name (str), PV properties (dict), PV tags (list(str))
    owner : str
        Owner of the data.

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]

    See Also
    --------
    get_data_from_tb, get_data_from_db, get_data_from_cf
    """
    owner = kws.get('owner', getpass.getuser())
    retval = []
    for pv_name, pv_props, pv_tags in raw_data:
        new_rec = {'name': pv_name,
                   'owner': owner,
                   'properties': [{'name': k, 'value': v, 'owner': owner}
                                    for k,v in pv_props.items()],
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
        self.meta.update({k:v})
        self.obj.__dict__.update({k:v})

    def __getitem__(self, k):
        return self.meta.get(k, None)
    
    def keys(self):
        return self.meta.keys()

    def __repr__(self):
        return str(self.meta)


def parse_dt(dt, ref_date=None):
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
    if ref_date is None:
        timenow = datetime.now()
    elif isinstance(ref_date, datetime):
        timenow = ref_date
    else:
        raise TypeError("Invalid date time variable.")
    
    time_unit_table = {'years': 'years', 'months': 'months', 'weeks': 'weeks',
            'days': 'days', 'hours': 'hours', 'minutes': 'minutes',
            'seconds': 'seconds', 'microseconds': 'microseconds',
            'year': 'years', 'month': 'months', 'week': 'weeks', 'day': 'days',
            'hour': 'hours', 'minute': 'minutes', 'second': 'seconds',
            'microsecond': 'microseconds', 'min': 'minutes', 'sec': 'seconds',
            'msec': 'microseconds', 'mins': 'minutes', 'secs': 'seconds',
            'msecs': 'microseconds'}

    dt_dict = {}
    dt_tuple = dt.replace('and', ',').replace('ago', ',').strip(' ,').split(',')
    for part in dt_tuple:
        v, k = part.strip().split()
        dt_dict[time_unit_table[k]] = int(v)

    dt = relativedelta.relativedelta(**dt_dict)
    return timenow - dt
