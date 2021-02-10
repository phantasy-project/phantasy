#!/usr/bin/python
# -*- coding: utf-8 -*-

"""functions for readback handler.
"""

import logging

from cothread.catools import caget

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2016-2017, Facility for Rare Isotope beams," \
                "Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)


def get_readback(pv):
    """Get readback data from define PVs.

    Parameters
    ----------
    pv : str or List(str) or dict
        pv names.
    
    Returns
    -------
    ret : str or list or dict
        Array of readback values, if input pv is a dict,
        return dict, with keys of field names.

    Examples
    --------
    >>> elem = mp.get_elements(type='*PM')
    >>> pv1 = mp.get_pv_names(elem[0], 'X')
    >>> # pv is single string
    >>> get_readback(pv1['X'][0])
    5.128351743150942e-06
    >>> # pv is a list
    >>> get_readback(pv1['X'])
    [5.128351743150942e-06]
    >>> # pv is a dict
    >>> get_readback(pv1)
    {'X': [5.128351743150942e-06]}
    >>> # pv is from list of elements, with multiple fields
    >>> pv2 = mp.get_pv_names(elem, ['X', 'Y'])
    >>> data = get_readback(pv2)
    >>> data.keys()
    ['Y', 'X']

    See Also
    --------
    :class:`~phyapps.flowutils.MachinePortal.get_pv_names`
    """
    rtype = 'dict'
    if isinstance(pv, str):
        pv = {'pv': pv, }
        rtype = 'list'
    elif isinstance(pv, (list, tuple)):
        pv = {'pv': pv}
        rtype = 'list'

    rbk_dict = {k: caget(v) for k, v in pv.items()}

    if rtype == 'list':
        return rbk_dict['pv']
    else:
        return rbk_dict
