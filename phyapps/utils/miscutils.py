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

