#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Input and output functions regarding to generic directory service.
"""

import json
import logging
import os
from collections import OrderedDict
from fnmatch import fnmatch

from phantasy.library.misc import expand_list_to_dict
from phantasy.library.misc import flatten
from phantasy.library.misc import pattern_filter

from .database import CFCDatabase
from .table import CFCTable

_LOGGER = logging.getLogger(__name__)


def get_data_from_db(db_name, db_type='sqlite', **kws):
    """Get PV data from database, currently support database: ``SQLite``.

    Parameters
    ----------
    db_name : str
        Name of database.
    db_type : str
        Type of database, 'sqlite' by default.

    Keyword Arguments
    -----------------
    tag_delimiter : str
        Delimiter for tag string, ';' by default.
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
    owner : str
        Database owner, login username by default.
    prop_list : list
        Properties list.
    tag_list : list
        Tags list.

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    """
    tag_delimiter = kws.get('tag_delimiter', ';')
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)
    raw_data = kws.get('raw_data', None)
    owner = kws.get('owner', None)

    if db_type == 'sqlite':
        cfcd = CFCDatabase(db_name, owner=owner)
        if raw_data is None:
            raw_data = cfcd.find(name='*')
        prop_list = cfcd.getAllProperties(name_only=True)
        tag_list = cfcd.getAllTags(name_only=True)
        cfcd.close()
    else:
        _LOGGER.warning("{} will be implemented later.".format(db_type))
        raise NotImplementedError

    new_kws = {k: v for k, v in kws.items() if k not in ('raw_data', 'owner', 'tag_list', 'prop_list')}
    return _get_data(raw_data, prop_list, tag_list, **new_kws)


def get_data_from_tb(tb_name, tb_type='csv', **kws):
    """Get PV data from table file, currently support: ``csv``.

    Parameters
    ----------
    tb_name : str
        Name of table file.
    tb_type : str
        Type of table file, 'csv' by default

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
    owner : str
        Database owner, login username by default.
    prop_list : list
        Properties list.
    tag_list : list
        Tags list.

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    """
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)
    raw_data = kws.get('raw_data', None)
    owner = kws.get('owner', None)

    if tb_type == 'csv':
        cfct = CFCTable(tb_name, owner=owner)
        if raw_data is None:
            raw_data = cfct.find(name='*')
        prop_list = cfct.getAllProperties(name_only=True)
        tag_list = cfct.getAllTags(name_only=True)
    else:
        _LOGGER.warning("{} will be implemented later.".format(tb_type))
        raise NotImplementedError

    new_kws = {k: v for k, v in kws.items() if k not in ('raw_data', 'owner', 'tag_list', 'prop_list')}
    return _get_data(raw_data, prop_list, tag_list, **new_kws)


def _get_data(raw_data, prop_list, tag_list, **kws):
    """Filter data from *raw_data* by applying filters, which are
    defined by keyword arguments.
    """
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)

    if name_filter is not None:
        if isinstance(name_filter, str):
            name_filter = name_filter,
    else:
        name_filter = ('*',)

    prop_default = dict(zip(prop_list, ['*'] * len(prop_list)))
    if prop_filter is not None:
        if isinstance(prop_filter, str):
            prop_filter = prop_filter,
        prop_tmp = expand_list_to_dict(prop_filter, prop_list)  # dict
        if prop_tmp == {}:
            prop_selected = prop_default
        else:
            prop_selected = prop_tmp
    else:
        prop_selected = prop_default

    tag_selected = []
    if tag_filter is not None:
        if isinstance(tag_filter, str):
            tag_filter = tag_filter,
        tag_selected = flatten(
            [pattern_filter(tag_list, tn_i)
             for tn_i in tag_filter]
        )
        if tag_selected == []:
            _LOGGER.warning('Invalid tags defined, tag_filter will be inactived.')

    retval = []
    for rec in raw_data:
        pv_name_tmp = rec.get('name')
        if True in [fnmatch(pv_name_tmp, npi) for npi in name_filter]:
            pv_name = pv_name_tmp
        else:
            continue

        pv_tags = [t['name'] for t in rec.get('tags')]
        if not set(tag_selected).issubset(pv_tags):
            continue

        pv_props_selected = []
        for p in rec.get('properties'):
            k, v = p['name'], p['value']
            if k in prop_selected:
                if prop_selected[k] is not None and not fnmatch(str(v), prop_selected[k]):
                    pv_name = None
                    continue
                else:
                    pv_props_selected.append(p)

        # ignore empty properties
        if pv_props_selected == []:
            continue

        rec['properties'] = pv_props_selected

        # pv_props_selected = [p for p in rec.get('properties')
        #                     if p['name'] in prop_selected and
        #                     fnmatch(str(p['value']), str(prop_selected[p['name']]))]
        # new_rec = copy(rec)
        # new_rec['properties'] = pv_props_selected
        # retval.append(new_rec)
        if pv_name is not None:
            retval.append(rec)

    return retval


def write_json(data, json_name, overwrite=False, **kws):
    """Write PV/channels data into JSON file, overwrite if *json_name* is
    already exists while *overwrite* is True.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    json_name : str
        Filename of JSON file.
    overwrite : bool
        Overwrite existing database file or not, False by default.

    Keyword Arguments
    -----------------
    tag_delimiter : str
        Delimiter for tags string, ``';'`` by default.
    indent : int
        Indent level of JSON file, 4 by default.

    See Also
    --------
    get_data_from_tb : Get PV data from spreadsheet.
    get_data_from_db : Get PV data from database.
    get_data_from_cf : Get PV data from Channel Finder Service.
    """
    tag_delimiter = kws.get('tag_delimiter', ';')
    indent = kws.get('indent', 4)

    fname = json_name
    if os.path.isfile(fname):
        if not overwrite:
            _LOGGER.warning("{} already exists, overwrite it by passing overwrite=True".format(fname))
            return None
        else:
            _LOGGER.warning("{} will be overwritten.".format(fname))

    pvdict = OrderedDict()
    for r in data:
        name = r['name']
        prop_dict = {p['name']: p['value'] for p in r['properties']}
        tag_list = [t['name'] for t in r['tags']]
        rdata = OrderedDict(prop_dict)
        rdata['tags'] = tag_delimiter.join(tag_list)
        pvdict[name] = rdata

    with open(fname, 'w') as f:
        json.dump(pvdict, f, indent=indent)



def _get_cf_data(cfc, prop_list, tag_list, **kws):
    """Get data from CFS.
    """
    kargs = {}
    name_filter = kws.get('name_filter', None)
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    size = kws.get('size', None)
    ifrom = kws.get('ifrom', None)
    if name_filter is not None:
        if isinstance(name_filter, list):
            kargs['name'] = '|'.join(name_filter)
        else:
            kargs['name'] = name_filter

    tag_selected = []
    if tag_filter is not None:
        if isinstance(tag_filter, str):
            tag_filter = tag_filter,
        tag_selected = flatten([pattern_filter(tag_list, tn_i)
            for tn_i in tag_filter])
        if tag_selected == []:
            _LOGGER.warning('Invalid tags defined, tag_filter will be inactived.')
    if tag_selected != []:
        kargs['tagName'] = ','.join(tag_selected)

    if prop_filter is not None:
        if isinstance(prop_filter, str):
            prop_filter = prop_filter,
        prop_tmp = expand_list_to_dict(prop_filter, prop_list)  # dict
        if prop_tmp == {}:
            prop_selected = None
        else:
            prop_selected = prop_tmp
    else:
        prop_selected = None
    
    if prop_selected is not None:
        kargs['property'] = _none_to_star(prop_selected).items()

    if size is not None:
        kargs['size'] = int(size)
    if ifrom is not None:
        kargs['from'] = int(ifrom)

    if kargs == {}:
        kargs = {'name': '*'}  # add to ChannelFinderClient.find()?
    return cfc.find(**kargs)


def _none_to_star(raw_dict):
    new_dict = {}
    for k,v in raw_dict.items():
        if v is None:
            new_dict[k] = '*'
        else:
            new_dict[k] = v
    return new_dict
