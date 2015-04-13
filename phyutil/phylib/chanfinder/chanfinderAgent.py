"""
Channel Finder
---------------

A module providing local Channel Finder Service (CFS). It interfaces to CFS or
local comma separated file (csv) and provides configuration data for the aphla
package.

For each PV, Channel Finder Service (CFS) provide a set of properties and
tags. This can help us to identify the associated element name, type, location
for every PV. The PVs are also tagged for 'default' read/write for a element
it is linked.
"""

# :author: Lingyun Yang <lyyang@bnl.gov>
# :modified: Guobao Shen <shen@frib.msu.edu>

from __future__ import print_function, unicode_literals

import os

from fnmatch import fnmatch
from time import gmtime, strftime
import sqlite3

import logging
_logger = logging.getLogger(__name__)

class ChannelFinderAgent(object):
    """
    Channel Finder Agent

    This module builds a local cache of channel finder service. It can imports
    data from CSV format file.
    """
    
    def __init__(self, **kwargs):
        """
        initialzation.
        """
        self.__cdate = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
        self.source = kwargs.get("source", None)
        self.use_unicode = False
        # the data is in `rows`. It has (n,3) shape, n*(pv, prpts, tags) with
        # type (str, dict, list)
        self.results = []

        # property name for a channel running in an IOC
        # by default, iocName
        self.ioc_name = kwargs.get("hostName", "iocName")
        # property name for an IOC running on a computer server
        # by default, hostName
        self.host_name = kwargs.get("hostName", "hostName")

    def updateSource(self, source):
        """ Update data source, using the new data source.

        :param source: data source
        :return:
        """
        self.source = source

    def downloadCfs(self, **kwargs):
        """
        downloads data from channel finder service.
        
        :param cfsurl: the URL of channel finder service.
        :type cfsurl: str
        :param keep: if present, it only downloads specified properties.
        :type keep: list
        :param converter: convert properties from string to other format.
        :type converter: dict

        :Example:

            >>> prpt_list = ['elemName', 'sEnd']
            >>> conv_dict = {'sEnd', float}
            >>> downloadCfs(source=URL, keep = prpt_list, converter = conv_dict)
            >>> downloadCfs(source=URL, property=[('hostName', 'virtac2')])
            >>> downloadCfs(source=URL, property=[('hostName', 'virtac')], tagName='aphla.*')

        The channel finder client API provides *property* and *tagName* as
        keywords parameters. 
        """
        source = kwargs.get("source", None)
        if source is not None:
            self.source = source
        if os.path.isfile(self.source) or self.source == ":memoty:":
            # get data from SQLite database file or in memory
            res = self._downloadCfsSQLite(self.source, **kwargs)
        else:
            res = self._downloadCfs(self.source, **kwargs)

        return res

    def _downloadCfsSQLite(self, dbname, **kwargs):
        """Get data from local SQLite database, either in file, or in memory

        :param dbname:
        :param kwargs:
        :return:
        """
        # keep_prpts = kwargs.pop('keep', None)
        # converter  = kwargs.pop('converter', {})
        delimeter = kwargs.get('tag_delimiter', ';')

        from cflocaldb import ChannelFinderLocal

        cfl = ChannelFinderLocal(dbname)
        cfl.conn()
        properties, results = cfl.find(name="*")
        cfl.close()

        # if keep_prpts is None:
        #     # use all possible property names
        #     keep_prpts = [p.Name for p in properties]

        #print "# include properties", properties
        self.results[:]=[]
        for res in results:
            pvname = None
            props = {}
            tags = []
            for idx, prpts in enumerate(properties):
                if prpts in ['pv_id', 'elem_id']:
                    continue
                elif prpts == "pv":
                    pvname = res[idx]
                elif prpts == "tags":
                    if res[idx] is not None:
                        tags = res[idx].split(delimeter)
                elif res[idx] is not None:
                    props[prpts] = res[idx]
            if pvname is not None:
                self.results.append([pvname, props, tags])

    def _downloadCfs(self, cfsurl, **kwargs):
        """Get daya from channel finder web service

        :param cfsurl:
        :param kwargs:
        :return:
        """
        keep_prpts = kwargs.pop('keep', None)
        converter  = kwargs.pop('converter', {})
        from channelfinder import ChannelFinderClient
        cf = ChannelFinderClient(BaseURL = cfsurl)
        if len(kwargs) == 0:
            chs = cf.find(name='*')
        else:
            #print kwargs
            chs = cf.find(**kwargs)
        if not chs:
            return

        if keep_prpts is None:
            # use all possible property names
            keep_prpts = [p.Name for p in cf.getAllProperties()]
            
        #print "# include properties", properties
        for ch in chs:
            # keep only known properties
            prptdict = ch.getProperties()
            # prpts is known part from prptdict, otherwise empty dict
            if prptdict is not None:
                prpts = dict([v for v in prptdict.iteritems()])
                # convert the data type
            else:
                prpts = None
            # the empty tags could be None
            if self.use_unicode:
                self.results.append([unicode(ch.Name),
                                  dict([(unicode(k), unicode(v))
                                        for k,v in prpts.iteritems()]),
                                  [unicode(v) for v in ch.getTags()]])
            else:
                self.results.append([ch.Name.encode('ascii'),
                                  dict([(k.encode('ascii'), v.encode('ascii'))
                                        for k,v in prpts.iteritems()]),
                                  [v.encode('ascii') for v in ch.getTags()]])
            if self.results[-1][1]:
                for k in converter:
                    self.results[-1][1][k] = converter[k](prpts[k])
            # warn if hostName or iocName does not present
            if self.host_name not in self.results[-1][1]:
                _logger.warn("no 'hostName' for {0}".format(self.results[-1]))
            if self.ioc_name not in self.results[-1][1]:
                _logger.warn("no 'iocName' for {0}".format(self.results[-1]))

            del prptdict

    def sort(self, fld, dtype = None):
        """
        sort the data by 'pv' or other property name.

        :Example:

            >>> sort('pv')
            >>> sort('elemName')

        :param fld:
        :param dtype:
        :return:
        """
        from operator import itemgetter
        if fld == 'pv':
            self.results.sort(key = itemgetter(0))
        elif dtype is None:
            self.results.sort(key=lambda k: k[1][fld])
        elif dtype == 'str':
            self.results.sort(key=lambda k: str(k[1].get(fld, "")))
        elif dtype == 'float':
            self.results.sort(key=lambda k: float(k[1].get(fld, 0.0)))
        elif dtype == 'int':
            self.results.sort(key=lambda k: int(k[1].get(fld, 0)))

    def renameProperty(self, oldkey, newkey):
        """rename the property name for data copy in memory.
        No change to either local database or remote service.

        :param oldkey: old name of a property
        :param newkey: new name of a property
        :return:
        """
        n = 0
        for r in self.results:
            if oldkey not in r[1]:
                continue
            r[1][newkey] = r[1].pop(oldkey)
            n += 1

    def _loadJson(self, fname):
        """Read data from a CSV (Comma Separated Values) file.
        Update the data source to the CSV file name.

        The CSV file format has to be as a Python dict:
         { '__cdata': date string,
           'results': data
         }

        :param fname: CSV file name
        :return:
        """
        self.source = fname
        import json
        with file(fname, 'r') as f:
            d = json.load(f)
            self.__cdate = d['__cdate']
            self.results = d['results']

    def _saveJson(self, fname):
        """ Save data into a CSV (Comma Separated Values) file.

        The CSV file format has a format as below:
         { '__cdata': date string,
           'results': data
         }

        :param fname: CSV file name
        :return:
        """
        import json
        with file (fname, 'w') as f:
            json.dump({'__cdate': self.__cdate, 'results': self.source}, f)

    def update(self, pv, prpts, tags):
        """
        update the properties and tags for pv for data copy in memory.
        No change to either local database or remote service.

        :param pv: pv
        :param prpts: property dictionary
        :param tags: list of tags
        :return:
        """
        idx = -1
        for i, rec in enumerate(self.results):
            if rec[0] != pv:
                continue
            idx = i
            rec[1].update(prpts)
            for tag in tags:
                if tag in rec[2]:
                    continue
                rec[3].append(tag)
        if idx < 0:
            self.results.append([pv, prpts, tags])
            idx = len(self.results) - 1
        return idx

    def tags(self, pat):
        """
        return a list of tags matching the unix filename pattern *pat* for data copy in memory.
        No change to either local database or remote service.

        :param pat: unix file name pattern
        :return: list of matched tags
        """
        alltags = set()
        for r in self.results:
            alltags.update(r[2])
        return [t for t in alltags if fnmatch(t, pat)]

    def splitPropertyValue(self, prpt, delimiter=";"):
        """Split value of given property for data copy in memory.
        No change to either local database or remote service.

        :param prpts: property name
        :param delimiter: delimiter to divide property value, ";" by default
        :return:
        """

        for r in self.results:
            if prpt not in r[1]:
                continue
            r[1][prpt] = r[1][prpt].split(delimiter)

    def splitChainedElement(self, prpt, delimiter=";"):
        """ Split property of a chained channel name, which is separated by ";" by default.

        :param prpt: property name
        :param delimiter: delimiter, ";" by default
        :return: new results
        """
        old_results = self.results[:]
        self.results[:] = []
        for r in old_results:
            prptlst = r[1][prpt].split(delimiter)
            if len(prptlst) == 1:
                self.results.append(r)
                continue
            ext = []
            for v in prptlst:
                ext.append([r[0], {prpt: v}, r[2]])
            for k,v in r[1].items():
                if k == prpt:
                    continue
                prptlst = v.split(delimiter)
                if len(prptlst) == 1:
                    for ei in ext: ei[1][k] = v
                else:
                    for j,ei in enumerate(ext):
                        ei[1][k] = prptlst[j]
            self.results.extend(ext)

    def groups(self, key='elemName'):
        """group the data according to their property *key*.

        e.g. groups(key='elemName') will return a dictionary with keys the
        element names, values a list of indices which share the same element
        name.

        Example::

            groups()
            {'BPM1': [0, 3], 'Q1': [1], 'COR1' : [2]}

        :param key: property name
        :return: dict using given property name as key.
        """
        ret = {}
        for i, r in enumerate(self.results):
            # skip if no properties
            if r[1] is None:
                continue
            # skip if no interesting properties
            if key not in r[1]:
                continue

            # record the property-value and its index. Append if
            # property-value exists.
            v = ret.setdefault(r[1][key], [])
            v.append(i)
        return ret

    def __sub__(self, rhs):
        """the result has no info left if it was same as rhs, ignore empty properties in self

        :param rhs:
        :return:
        """
        samp = dict([(rec[0],i) for i,rec in enumerate(rhs.rows)])
        ret = {}
        for pv, prpt, tags in self.rows:
            if not samp.has_key(pv):
                ret[pv] = (prpt, tags)
                continue
            rec2 = rhs.rows[samp[pv]]
            p2, t2 = rec2[1], rec2[2]
            ret[pv] = [{}, []]
            for k,v in prpt.iteritems():
                if not p2.has_key(k):
                    ret[pv][0][k] = v
                    continue
                elif p2[k] != v:
                    ret[pv][0][k] = v
            for t in tags:
                if t in t2:
                    continue
                ret[pv][1].append(t)
        return ret

if __name__ == "__main__":
    cfa = ChannelFinderAgent()
    cfa.downloadCfs("example.sqlite")
    print (cfa.results)