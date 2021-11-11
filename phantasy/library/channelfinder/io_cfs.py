#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Input and output functions regarding to generic directory service (CFS).
"""

import logging
import requests
import getpass

from channelfinder import ChannelFinderClient
from phantasy.library.misc import cofetch

from .io import _get_data
from .io import _get_cf_data

_LOGGER = logging.getLogger(__name__)


def get_data_from_cf(url, **kws):
    """Get PV data from Channel Finder Service (URL).

    Parameters
    ----------
    url : str
        URL address of channel finder server, e.g.
        ``https://127.0.0.1:8181/ChannelFinder``.

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
    raw_data : list
        List of PV data.
    username :
        Username of channel finder service.
    password :
        Password of channel finder service username.
    prop_list : list
        Properties list.
    tag_list : list
        Tags list.
    size : int
        Length of returned list.
    ifrom : int
        Starting index of returned list (see find()).

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    """
    raw_data = kws.get('raw_data', None)
    username = kws.get('username', None)
    password = kws.get('password', None)
    prop_list = kws.get('prop_list', None)
    tag_list = kws.get('tag_list', None)
    new_kws = {k: v for k, v in kws.items() if k not in ['raw_data', 'prop_list', 'tag_list']}
    #
    if raw_data is None:
        cfc = ChannelFinderClient(BaseURL=url, username=username, password=password)
        return _get_cf_data(cfc, prop_list, tag_list, **new_kws)
    else:
        return _get_data(raw_data, prop_list, tag_list, **new_kws)


def write_cfs(data, cfs_url, **kws):
    """Write PV/channels data into Channel Finder Service, only the owner of
    tags/properties/channels can manipulate CFS.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    cfs_url : str
        URL of channel Finder Service.

    Keyword Arguments
    -----------------
    force : True or False
        Skip authorization if True, False by default.

    Keyword Arguments
    -----------------
    username : str
        Username of Channel Finder Service.
    password : str
        Password of defined username of Channel Finder Service.
    """
    force = kws.get('force', False)
    if not force:
        username = kws.get('username', None)
        password = kws.get('password', None)

        if username is None:
            username = input("Enter username: ")

        if password is None:
            password = getpass.getpass("Enter password: ")

        cfc = ChannelFinderClient(BaseURL=cfs_url, username=username, password=password)
        tags, props = get_all_tags(data), get_all_properties(data)
        cfc.set(tags=tags)
        cfc.set(properties=props)
        cfc.set(channels=data)

    #        ch_list = []
    #        for ch in data:
    #            ch_tags, ch_props = ch['tags'], ch['properties']
    #            skip_ch = False
    #
    #            for t in ch_tags:
    #                if not cfc.findTag(t['name']):
    #                    _LOGGER.debug('Add new tag: {0}:{1}'.format(t['name'], t['owner']))
    #                    if username == t['owner']:
    #                        cfc.set(tag=t)
    #                    else:
    #                        _LOGGER.debug('Cannot add new tag, permission denied.')
    #                        skip_ch = True
    #
    #            for p in ch_props:
    #                p_dict = {'name': p['name'], 'owner': p['owner'], 'value': None}
    #                if not cfc.findProperty(p['name']):
    #                    _LOGGER.debug('Add new property: {0}:{1}'.format(t['name'], t['owner']))
    #                    if username == t['owner']:
    #                        cfc.set(property=p)
    #                    else:
    #                        _LOGGER.debug('Cannot add new property, permission denied.')
    #                        skip_ch = True
    #
    #            if username == ch['owner'] and not skip_ch:
    #                ch_list.append(ch)
    #
    #        cfc.set(channels=ch_list)
    else:
        if cfs_url is None:
            cfc = ChannelFinderClient()
        else:
            cfc = ChannelFinderClient(BaseURL=cfs_url)
        tags, props = get_all_tags(data), get_all_properties(data)
        cfc.set(tags=tags)
        cfc.set(properties=props)
        cfc.set(channels=data)


def get_all_tags(data, **kws):
    """Get all tags from PV data.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.

    Keyword Arguments
    -----------------
    name_only : True or False
        If true, only return list of property names.

    Returns
    -------
    ret : list of dict
        dict: {'name': property_name, 'value': None, 'owner': owner}
    """
    t_list = []
    for r in data:
        new_t = [
            {'name': p['name'], 'owner': p['owner']}
            for p in r['tags']
        ]
        [t_list.append(i) for i in new_t if i not in t_list]

    if kws.get('name_only', False):
        return sorted([t['name'] for t in t_list])
    else:
        return t_list


def get_all_properties(data, **kws):
    """Get all property definitions from PV data.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.

    Keyword Arguments
    -----------------
    name_only : True or False
        If true, only return list of property names.

    Returns
    -------
    ret : list of dict
        dict: {'name': property_name, 'value': None, 'owner': owner}
    """
    p_list = []
    for r in data:
        new_p = [
            {'name': p['name'], 'owner': p['owner'], 'value': None}
            for p in r['properties']
        ]
        [p_list.append(i) for i in new_p if i not in p_list]

    if kws.get('name_only', False):
        return sorted([p['name'] for p in p_list])
    else:
        return p_list


@cofetch
def _cofetch_data(url):
    return requests.get(url, verify=False).json()
