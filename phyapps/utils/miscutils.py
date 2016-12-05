#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" other support utils

.. moduleauthor:: Tong Zhang <zhangt@frib.msu.edu>

:date: 2016-11-22 11:21:15 AM EST
"""

import logging
from flame import Machine


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
    >>> 
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
    >>> 
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
