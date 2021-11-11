#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to read data from a CSV (comma separated values).
It is developed to assist the channel finder service, but could be used for
other purpose.

It supports 2 different CSV file formats.

* Format 1, which starts with pv name as first column, following by properties
  and tags.

  It supports 2 concept with property and tag.
  Each cell except the first one is a property name value pair if it has format
  like A=B with property name "A" and property value "B". Otherwise it is a tag.

  Example:
    PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2

* Format 2: Each column has a head label is a property except for the column
  "PV". Otherwise, it is a tag.

  Example:
    PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType
    xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2
"""

import csv
import getpass
import logging
import os

from phantasy.library.exception import CSVFormatError
from phantasy.library.misc import simplify_data

_LOGGER = logging.getLogger(__name__)


def __read_csv_1(csvdata):
    """Load data from CSV file with headers like:
    PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
    xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      xxx,xxx,xxx,xxx

    the last columns are for all tags.

    Parameters
    ----------
    csvdata : list
        List of line data read from csv file.
    
    Returns
    -------
    ret : list
    """
    keys = [k.strip() for k in csvdata[0]]
    pv_idx = [k.lower() for k in keys].index('pv')

    prpt_idx, tags_idx = [], []
    for idx, label in enumerate(keys):
        if idx == pv_idx:
            # no need to process PV column
            continue
        if len(label.strip()) == 0:
            # if the header is empty, it is a tag
            tags_idx.append(idx)
        else:
            # otherwise, it is a property
            prpt_idx.append(idx)

    results = []
    for data in csvdata[1:]:
        if len(data) == 0:
            # empty line, go to next
            continue
        properties = [v.strip() for v in data]
        pv = properties[pv_idx]
        if not pv or properties[0].strip().startswith('#'):
            # PV name is empty or a comment line
            # go to next
            continue

        # if given property value not empty, add to property dict
        prpts = dict([(keys[i], data[i]) for i in prpt_idx if data[i].strip()])

        # tags_idx could be empty for tags in the end columns
        tags = [data[i].strip() for i in tags_idx]
        for i in range(len(keys), len(data)):
            tags.append(data[i].strip())
        # print s[ipv], prpts, tags
        results.append([data[pv_idx], prpts, tags])

    return results


def __read_csv_2(csvdata):
    """Load data from CSV file without headers, that the first column is for PV, like:
    PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx, tag1,tag2,tag3

    the last one are all tags.

    Parameters
    ----------
    csvdata : list
        List of line data read from csv file.
    
    Returns
    -------
    ret : list
    """
    results = []
    for data in csvdata:
        if len(data) == 0:
            # empty line, do nothing
            continue
        s = [v.strip() for v in data]
        pv = s[0]
        if not pv or pv.strip().startswith('#'):
            # invalid pv name, or comment line. Do nothing
            continue

        prpts, tags = {}, []
        for cell in s:
            if '=' in cell:
                k, v = cell.split('=')
                prpts[k.strip()] = v.strip()
            else:
                tags.append(cell.strip())
        results.append([pv, prpts, tags])

    return results


def read_csv(csvfile):
    """Support 2 different CSV file formats.
    *Format 1 (table format)*:

    PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
    xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2

    *Format 2*:
    PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2

    In format 2, any column does not have a header label is treated as a tag.

    Parameters
    ----------
    csvfile : str
        CSV file name.

    Returns
    --------
    ret : List
        List of ``[pv, properties, tags]``.
    """
    if not os.path.isfile(csvfile):
        raise RuntimeError("Invalid CSV file {0}".format(csvfile))

    with open(csvfile, 'r') as f:
        csvraw = list(csv.reader(f))

    if len(csvraw) == 0:
        raise RuntimeError("Empty CSV file {0}".format(csvfile))

    for i, line in enumerate(csvraw):
        linestr = ''.join(line).strip()
        if linestr != '' and not linestr.startswith('#'):
            head_idx = i
            break

    if len(csvraw) == head_idx:
        raise RuntimeError("No data in CSV file {0}".format(csvfile))

    if csvraw[head_idx][0].strip().lower() == 'pv':
        csv_data = __read_csv_1(csvraw[head_idx:])
    else:
        csv_data = __read_csv_2(csvraw[head_idx:])

    return csv_data


def _save_csv_table(data, csvname):
    """save the CFS in CSV format (table).

    example
        PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
        xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2
    In this format, any column does not have a header label is treated as a tag.

    :param data:
    :param csvname:
    :return:
    """
    # find out all the property names
    prpts_set = set()
    for r in data:
        if r[1] is None:
            continue
        for k in r[1]:
            prpts_set.add(k)
    header = sorted(list(prpts_set))

    writer = csv.writer(open(csvname, 'w'))
    writer.writerow(["PV"] + header)
    for r in data:
        prpt = []
        for k in header:
            if r[1] is None:
                prpt.append('')
            elif k not in r[1]:
                prpt.append('')
            else:
                prpt.append(r[1][k])
        if r[2] is None:
            writer.writerow([r[0]] + prpt)
        else:
            writer.writerow([r[0]] + prpt + list(r[2]))
    del writer


def _save_csv_explicit(data, csvname):
    """export the CFS in CSV2 format (explicit).

    example:
        PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2
    """
    # find out all the property names
    with open(csvname, 'w') as f:
        for r in data:
            p = ",".join(["%s=%s" % (k, v) for k, v in r[1].items()])
            f.write(",".join([r[0], p, ",".join(r[2])]) + "\n")


def write_csv(data, csvname, frmt="table"):
    """Write data into CSV file.
    *Format 1 (table)*:
    PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
    xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2

    In format 1, any column does not have a header label is treated as a tag.

    *Format 2 (explicit)*:
    PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2

    Parameters
    ----------
    data :
        data.
    csvname : str
        Output file name.
    frmt : str
        Output file format as described above.
    """
    if frmt == "table":
        _save_csv_table(data, csvname)
    elif frmt == "explicit":
        _save_csv_explicit(data, csvname)
    else:
        raise CSVFormatError("CSV file format {0} not supported yet.".format(format))


def write_tb(data, tb_name, overwrite=False, **kwargs):
    """Write PV/channels data into spreadsheet, overwrite if *tb_name* is
    already exists while *overwrite* is True.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``.
    tb_name : str
        Filename of spreadsheet
    overwrite : bool
        Overwrite existing spreadsheet file or not, False by default.
    
    Keyword Arguments
    -----------------
    tb_type : str
        File type of spreadsheet, 'csv' by default.

    See Also
    --------
    get_data_from_tb : Get PV data from spreadsheet.
    get_data_from_db : Get PV data from database.
    get_data_from_cf : Get PV data from Channel Finder Service.
    """
    tb_type = kwargs.get('tb_type', 'csv')

    if os.path.isfile(tb_name):
        if not overwrite:
            _LOGGER.warning("{} already exists, overwrite it by passing overwrite=True".format(tb_name))
            return None
        else:
            _LOGGER.warning("{} will be overwritten.".format(tb_name))

    if tb_type == 'csv':
        pvdata = simplify_data(data)
        write_csv(pvdata, tb_name)


class CFCTable(object):
    """Channel finder client using spreadsheet as data source, uniform
    interface is provided as ``CFCDatabase`` and ``ChannelFinderClient``.

    Note
    ----
    This class is not intended to be used by the users, better solution is:
    1. Convert spreadsheet into SQLite database;
    2. Use ``CFCDatabase`` to initialize.
    3. If spreadsheet data source is required, generate from ``CFCDatabase``.
    """

    def __init__(self, tb_name=None, owner=None):
        self._tb_name = tb_name
        self.owner = owner
        self._csv_data = None
        if tb_name is not None:
            try:
                data = read_csv(tb_name)
                self._csv_data = data
            except:
                _LOGGER.warning("Cannot read data from {}.".format(tb_name))

    @property
    def owner(self):
        """Str: owner of the table source."""
        return self._owner

    @owner.setter
    def owner(self, owner):
        if owner is None:
            self._owner = getpass.getuser()
        else:
            self._owner = owner

    @property
    def tb_name(self):
        """Str: Filename of table source."""
        return self._tb_name

    @tb_name.setter
    def tb_name(self, n):
        try:
            data = read_csv(n)
            self._csv_data = data
            self._tb_name = n
        except:
            _LOGGER.warning("Cannot read data from {}.".format(n))
            _LOGGER.warning("Rollback to previous one.")

    def find(self, name='*'):
        """Return csv data as channel finder format.
        """
        if self._csv_data is None:
            return None

        _owner = self.owner
        retval = []
        for rec in self._csv_data:
            new_rec = {'name': rec[0],
                       'owner': _owner,
                       'properties': [{'name': k, 'value': v, 'owner': _owner}
                                      for k, v in rec[1].items()],
                       'tags': [{'name': t, 'owner': _owner} for t in rec[2]],
                       }
            retval.append(new_rec)

        return retval

    def getAllTags(self, **kws):
        """Get all tags.

        Keyword Arguments
        -----------------

        Keyword Arguments
        -----------------
        name_only : True or False
            If true, only return list of tag names.

        Returns
        -------
        ret : list of dict
            dict: {'name': tag_name, 'owner': owner}
        """
        if self._csv_data is None:
            return None

        _owner = self.owner
        tag_set = set()
        for _, _, t in self._csv_data:
            [tag_set.add(i) for i in t]

        if kws.get('name_only', False):
            return sorted(list(tag_set))
        else:
            return [{'name': tag, 'owner': _owner} for tag in tag_set]

    def getAllProperties(self, **kws):
        """Get all property definitions.

        Keyword Arguments
        -----------------
        name_only : True or False
            If true, only return list of property names.

        Returns
        -------
        ret : list of dict
            dict: {'name': property_name, 'value': None, 'owner': owner}
        """
        if self._csv_data is None:
            return None

        _owner = self.owner
        p_set = set()
        for _, p, _ in self._csv_data:
            [p_set.add(i) for i in p]

        if kws.get('name_only', False):
            return sorted(list(p_set))
        else:
            return [{'name': p, 'owner': _owner, 'value': None} for p in p_set]
