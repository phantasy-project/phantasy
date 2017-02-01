#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Input and output functions about CFS.

.. Authors: 
..    Lingyun Yang <lyyang@bnl.gov>
..    Guobao Shen <shen@frib.msu.edu>
..    Tong Zhang <zhangt@frib.msu.edu>
"""

from __future__ import print_function
from __future__ import unicode_literals

import getpass
import json
import logging
import os
import time
from collections import OrderedDict
from fnmatch import fnmatch

from channelfinder import ChannelFinderClient

from phantasy.library.misc import expand_list_to_dict
from phantasy.library.misc import flatten
from phantasy.library.misc import pattern_filter
from .database import CFCDatabase
from .table import CFCTable

_LOGGER = logging.getLogger(__name__)

#class ChannelFinderAgent(object):
#    """
#    [docstring to be updated]
#    Channel Finder Agent
#
#    This module builds a local cache of channel finder service. It can imports
#    data from CSV format file.
#
#    For every PV record, fetched data is of the following format:
#    [PV name (str), PV properties (dict), PV tags (list of str)]
#    """
#    
#    def __init__(self, **kwargs):
#        # timestamp
#        self.__cdate = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())
#
#        self.source = kwargs.get("source", None)
#        self.use_unicode = False
#
#        # PV data results
#        self.results = []
#
#        # property name for a channel running in an IOC
#        # by default, iocName
#        self.ioc_name = kwargs.get("hostName", "iocName")
#
#        # property name for an IOC running on a computer server
#        # by default, hostName
#        self.host_name = kwargs.get("hostName", "hostName")
#    
#    @property
#    def source(self):
#        return self._source
#
#    @source.setter
#    def source(self, s):
#        self._source = s
#
#    def downloadCfs(self, **kwargs):
#        """
#        downloads data from channel finder service.
#        
#        :param cfsurl: the URL of channel finder service.
#        :type cfsurl: str
#        :param keep: if present, it only downloads specified properties.
#        :type keep: list
#        :param converter: convert properties from string to other format.
#        :type converter: dict
#
#        :Example:
#
#            >>> prpt_list = ['elemName', 'sEnd']
#            >>> conv_dict = {'sEnd', float}
#            >>> downloadCfs(source=URL, keep = prpt_list, converter = conv_dict)
#            >>> downloadCfs(source=URL, property=[('hostName', 'virtac2')])
#            >>> downloadCfs(source=URL, property=[('hostName', 'virtac')], tagName='aphla.*')
#
#        The channel finder client API provides *property* and *tagName* as
#        keywords parameters. 
#        """
#        source = kwargs.get("source", None)
#        if source is not None:
#            self.source = source
#        if os.path.isfile(self.source) or self.source == ":memoty:":
#            # get data from SQLite database file or in memory
#            res = self._downloadCfsSQLite(self.source, **kwargs)
#        else:
#            res = self._downloadCfs(self.source, **kwargs)
#
#        return res
#
#    def _downloadCfs(self, cfsurl, **kwargs):
#        """Get daya from channel finder web service
#
#        :param cfsurl:
#        :param kwargs:
#        :return:
#        """
#        keep_prpts = kwargs.pop('keep', None)
#        converter  = kwargs.pop('converter', {})
#        from channelfinder import ChannelFinderClient
#        cf = ChannelFinderClient(BaseURL = cfsurl)
#        if len(kwargs) == 0:
#            chs = cf.find(name='*')
#        else:
#            #print kwargs
#            chs = cf.find(**kwargs)
#        if not chs:
#            return
#
#        if keep_prpts is None:
#            # use all possible property names
#            keep_prpts = [p.Name for p in cf.getAllProperties()]
#            
#        #print "# include properties", properties
#        for ch in chs:
#            # keep only known properties
#            prptdict = ch.getProperties()
#            # prpts is known part from prptdict, otherwise empty dict
#            if prptdict is not None:
#                prpts = dict([v for v in prptdict.iteritems()])
#                # convert the data type
#            else:
#                prpts = None
#            # the empty tags could be None
#            if self.use_unicode:
#                self.results.append([unicode(ch.Name),
#                                  dict([(unicode(k), unicode(v))
#                                        for k,v in prpts.iteritems()]),
#                                  [unicode(v) for v in ch.getTags()]])
#            else:
#                self.results.append([ch.Name.encode('ascii'),
#                                  dict([(k.encode('ascii'), v.encode('ascii'))
#                                        for k,v in prpts.iteritems()]),
#                                  [v.encode('ascii') for v in ch.getTags()]])
#            if self.results[-1][1]:
#                for k in converter:
#                    self.results[-1][1][k] = converter[k](prpts[k])
#            # warn if hostName or iocName does not present
#            if self.host_name not in self.results[-1][1]:
#                _logger.warn("no 'hostName' for {0}".format(self.results[-1]))
#            if self.ioc_name not in self.results[-1][1]:
#                _logger.warn("no 'iocName' for {0}".format(self.results[-1]))
#
#            del prptdict
#
#    def sort(self, fld, dtype = None):
#        """
#        sort the data by 'pv' or other property name.
#
#        :Example:
#
#            >>> sort('pv')
#            >>> sort('elemName')
#
#        :param fld:
#        :param dtype:
#        :return:
#        """
#        from operator import itemgetter
#        if fld == 'pv':
#            self.results.sort(key = itemgetter(0))
#        elif dtype is None:
#            self.results.sort(key=lambda k: k[1][fld])
#        elif dtype == 'str':
#            self.results.sort(key=lambda k: str(k[1].get(fld, "")))
#        elif dtype == 'float':
#            self.results.sort(key=lambda k: float(k[1].get(fld, 0.0)))
#        elif dtype == 'int':
#            self.results.sort(key=lambda k: int(k[1].get(fld, 0)))
#
#    def renameProperty(self, oldkey, newkey):
#        """rename the property name for data copy in memory.
#        No change to either local database or remote service.
#
#        :param oldkey: old name of a property
#        :param newkey: new name of a property
#        :return:
#        """
#        n = 0
#        for r in self.results:
#            if oldkey not in r[1]:
#                continue
#            r[1][newkey] = r[1].pop(oldkey)
#            n += 1
#
#    def _loadJson(self, fname):
#        """Read data from a CSV (Comma Separated Values) file.
#        Update the data source to the CSV file name.
#
#        The CSV file format has to be as a Python dict:
#         { '__cdata': date string,
#           'results': data
#         }
#
#        :param fname: CSV file name
#        :return:
#        """
#        self.source = fname
#        import json
#        with file(fname, 'r') as f:
#            d = json.load(f)
#            self.__cdate = d['__cdate']
#            self.results = d['results']
#
#    def _saveJson(self, fname):
#        """ Save data into a CSV (Comma Separated Values) file.
#
#        The CSV file format has a format as below:
#         { '__cdata': date string,
#           'results': data
#         }
#
#        :param fname: CSV file name
#        :return:
#        """
#        import json
#        with file (fname, 'w') as f:
#            json.dump({'__cdate': self.__cdate, 'results': self.source}, f)
#
#    def update(self, pv, prpts, tags):
#        """
#        update the properties and tags for pv for data copy in memory.
#        No change to either local database or remote service.
#
#        :param pv: pv
#        :param prpts: property dictionary
#        :param tags: list of tags
#        :return:
#        """
#        idx = -1
#        for i, rec in enumerate(self.results):
#            if rec[0] != pv:
#                continue
#            idx = i
#            rec[1].update(prpts)
#            for tag in tags:
#                if tag in rec[2]:
#                    continue
#                rec[3].append(tag)
#        if idx < 0:
#            self.results.append([pv, prpts, tags])
#            idx = len(self.results) - 1
#        return idx
#
#    def tags(self, pat):
#        """
#        return a list of tags matching the unix filename pattern *pat* for data copy in memory.
#        No change to either local database or remote service.
#
#        :param pat: unix file name pattern
#        :return: list of matched tags
#        """
#        alltags = set()
#        for r in self.results:
#            alltags.update(r[2])
#        return [t for t in alltags if fnmatch(t, pat)]
#
#    def splitPropertyValue(self, prpt, delimiter=";"):
#        """Split value of given property for data copy in memory.
#        No change to either local database or remote service.
#
#        :param prpts: property name
#        :param delimiter: delimiter to divide property value, ";" by default
#        :return:
#        """
#
#        for r in self.results:
#            if prpt not in r[1]:
#                continue
#            r[1][prpt] = r[1][prpt].split(delimiter)
#
#    def splitChainedElement(self, prpt, delimiter=";"):
#        """ Split property of a chained channel name, which is separated by ";" by default.
#
#        :param prpt: property name
#        :param delimiter: delimiter, ";" by default
#        :return: new results
#        """
#        old_results = self.results[:]
#        self.results[:] = []
#        for r in old_results:
#            prptlst = r[1][prpt].split(delimiter)
#            if len(prptlst) == 1:
#                self.results.append(r)
#                continue
#            ext = []
#            for v in prptlst:
#                ext.append([r[0], {prpt: v}, r[2]])
#            for k,v in r[1].items():
#                if k == prpt:
#                    continue
#                prptlst = v.split(delimiter)
#                if len(prptlst) == 1:
#                    for ei in ext: ei[1][k] = v
#                else:
#                    for j,ei in enumerate(ext):
#                        ei[1][k] = prptlst[j]
#            self.results.extend(ext)
#
#    def groups(self, key='elemName'):
#        """group the data according to their property *key*.
#
#        e.g. groups(key='elemName') will return a dictionary with keys the
#        element names, values a list of indices which share the same element
#        name.
#
#        Example::
#
#            groups()
#            {'BPM1': [0, 3], 'Q1': [1], 'COR1' : [2]}
#
#        :param key: property name
#        :return: dict using given property name as key.
#        """
#        ret = {}
#        for i, r in enumerate(self.results):
#            # skip if no properties
#            if r[1] is None:
#                continue
#            # skip if no interesting properties
#            if key not in r[1]:
#                continue
#
#            # record the property-value and its index. Append if
#            # property-value exists.
#            v = ret.setdefault(r[1][key], [])
#            v.append(i)
#        return ret
#
#    def __sub__(self, rhs):
#        """the result has no info left if it was same as rhs, ignore empty properties in self
#
#        :param rhs:
#        :return:
#        """
#        samp = dict([(rec[0],i) for i,rec in enumerate(rhs.rows)])
#        ret = {}
#        for pv, prpt, tags in self.rows:
#            if not samp.has_key(pv):
#                ret[pv] = (prpt, tags)
#                continue
#            rec2 = rhs.rows[samp[pv]]
#            p2, t2 = rec2[1], rec2[2]
#            ret[pv] = [{}, []]
#            for k,v in prpt.iteritems():
#                if not p2.has_key(k):
#                    ret[pv][0][k] = v
#                    continue
#                elif p2[k] != v:
#                    ret[pv][0][k] = v
#            for t in tags:
#                if t in t2:
#                    continue
#                ret[pv][1].append(t)
#        return ret
#

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

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]
    """
    raw_data = kws.get('raw_data', None)
    username = kws.get('username', None)
    password = kws.get('password', None)
    cfc = ChannelFinderClient(BaseURL=url, username=username, password=password)
    all_prop_list = sorted([p['name'] for p in cfc.getAllProperties()])
    all_tag_list = sorted([t['name'] for t in cfc.getAllTags()])
    if raw_data is None:
        raw_data = cfc.find(name='*')

    new_kws = {k:v for k,v in kws.iteritems() if k != 'raw_data'} 
    return _get_data(raw_data, all_prop_list, all_tag_list, **new_kws)


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

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]
    """
    tag_delimiter = kws.get('tag_delimiter', ';')
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)
    raw_data = kws.get('raw_data', None)

    if db_type == 'sqlite': 
        cfcd = CFCDatabase(db_name)
        if raw_data is None:
            raw_data = cfcd.find(name='*')
        all_prop_list = cfcd.getAllProperties(name_only=True)
        all_tag_list = cfcd.getAllTags(name_only=True)
        cfcd.close()
    else:
        _LOGGER.warn("{} will be implemented later.".format(db_type))
        raise NotImplementedError

    new_kws = {k:v for k,v in kws.iteritems() if k != 'raw_data'} 
    return _get_data(raw_data, all_prop_list, all_tag_list, **new_kws)


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

    Returns
    -------
    ret : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]
    """
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)
    raw_data = kws.get('raw_data', None)

    if tb_type == 'csv':
        cfct = CFCTable(tb_name)
        if raw_data is None:
            raw_data = cfct.find(name='*')
        all_prop_list = cfct.getAllProperties(name_only=True)
        all_tag_list = cfct.getAllTags(name_only=True)
    else:
        _LOGGER.warn("{} will be implemented later.".format(db_type))
        raise NotImplementedError

    new_kws = {k:v for k,v in kws.iteritems() if k != 'raw_data'} 
    return _get_data(raw_data, all_prop_list, all_tag_list, **new_kws)


def _get_data(raw_data, all_prop_list, all_tag_list, **kws):
    """Filter data from *raw_data* by applying filters, which are
    defined by keyword arguments.
    """
    prop_filter = kws.get('prop_filter', None)
    tag_filter = kws.get('tag_filter', None)
    name_filter = kws.get('name_filter', None)

    if name_filter is not None:
        if isinstance(name_filter, (str, unicode)):
            name_filter = name_filter,
    else:
        name_filter = ('*',)

    prop_default = dict(zip(all_prop_list, ['*']*len(all_prop_list)))
    if prop_filter is not None:
        if isinstance(prop_filter, (str, unicode)):
            prop_filter = prop_filter,
        prop_tmp = expand_list_to_dict(prop_filter, all_prop_list) # dict
        if prop_tmp == {}:
            prop_selected = prop_default
        else:
            prop_selected = prop_tmp
    else:
        prop_selected = prop_default
    
    tag_selected = []
    if tag_filter is not None:
        if isinstance(tag_filter, (str, unicode)):
            tag_filter = tag_filter,
        tag_selected = flatten(
                    [pattern_filter(all_tag_list, tn_i)
                        for tn_i in tag_filter]
                    )
        if tag_selected == []:
            _LOGGER.warn('Invalid tags defined, tag_filter will be inactived.')

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

        #pv_props_selected = [p for p in rec.get('properties')
        #                     if p['name'] in prop_selected and 
        #                     fnmatch(str(p['value']), str(prop_selected[p['name']]))]
        #new_rec = copy(rec)
        #new_rec['properties'] = pv_props_selected
        #retval.append(new_rec)
        if pv_name is not None:
            retval.append(rec)

    return retval


def write_cfs(data, cfs_url, **kws):
    """Write PV/channels data into Channel Finder Service, only the owner of 
    tags/properties/channels can manipulate CFS.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]
    cfs_url : str
        URL of channel Finder Service.
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
            username = raw_input("Enter username: ")

        if password is None:
            password = getpass.getpass("Enter password: ")

        cfc = ChannelFinderClient(BaseURL=cfs_url, username=username, password=password)
        
        ch_list = []
        for ch in data:
            ch_tags, ch_props = ch['tags'], ch['properties']
            skip_ch = False

            for t in ch_tags:
                if not cfc.findTag(t['name']):
                    _LOGGER.debug('Add new tag: {0}:{1}'.format(t['name'], t['owner']))
                    if username == t['owner']:
                        cfc.set(tag=t)
                    else:
                        _LOGGER.debug('Cannot add new tag, permission denied.')
                        skip_ch = True

            for p in ch_props:
                p_dict = {'name': p['name'], 'owner': p['owner'], 'value': None}
                if not cfc.findProperty(p['name']):
                    _LOGGER.debug('Add new property: {0}:{1}'.format(t['name'], t['owner']))
                    if username == t['owner']:
                        cfc.set(property=p)
                    else:
                        _LOGGER.debug('Cannot add new property, permission denied.')
                        skip_ch = True

            if username == ch['owner'] and not skip_ch:
                ch_list.append(ch)
        
        cfc.set(channels=ch_list)
    else:
        if cfs_url is None:
            cfc = ChannelFinderClient()
        else:
            cfc = ChannelFinderClient(BaseURL=cfs_url)
        tags, props = get_all_tags(data), get_all_properties(data)
        cfc.set(tags=tags)
        cfc.set(properties=props)
        cfc.set(channels=data)
        

def write_json(data, json_name, overwrite=False, **kws):
    """Write PV/channels data into JSON file, overwrite if *json_name* is
    already exists while *overwrite* is True.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]
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
            _LOGGER.warn("{} already exists, overwrite it by passing overwrite=True".format(fname))
            return None
        else:
            _LOGGER.warn("{} will be overwritten.".format(fname))

    pvdict = OrderedDict()
    for r in data:
        name = r['name']
        prop_dict = {p['name']:p['value'] for p in r['properties']}
        tag_list = [t['name'] for t in r['tags']]
        rdata = OrderedDict(prop_dict)
        rdata['tags'] = tag_delimiter.join(tag_list)
        pvdict[name] = rdata

    with open(fname, 'w') as f:
        json.dump(pvdict, f, indent=indent)


def get_all_tags(data, **kws):
    """Get all tags from PV data.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]

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
        {'name': PV name (str), 'owner': str,
         'properties': PV properties (list(dict)),
         'tags': PV tags (list(dict))]

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

