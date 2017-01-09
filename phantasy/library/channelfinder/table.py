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

:author: Guobao Shen <shen@frib.msu.edu>
"""

import os
import csv

from phantasy.library.exception import CSVFormatError

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
        #print s[ipv], prpts, tags
        results.append([data[pv_idx], prpts, tags])

    return results


def __read_csv_2 (csvdata):
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
    Format 1 (table format):
        PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
        xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2
    Format 2:
        PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2

    In format 2, any column does not have a header label is treated as a tag.

    :param csvfile:
    :return: list of [pv, properties, tags]

    :raise: RuntimeError
    """
    if not os.path.isfile(csvfile):
        raise RuntimeError("Invalid CSV file {0}".format(csvfile))

    csvraw = list(csv.reader(open(csvfile, 'r')))

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

    writer = csv.writer(open(csvname, 'wb'))
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
            p = ",".join(["%s=%s" % (k,v) for k,v in r[1].items()])
            f.write(",".join([r[0], p, ",".join(r[2])]) + "\n")


def write_csv(data, csvname, frmt="table"):
    """Write data into CSV file.
    Format 1 (table):
        PV, machine, elemIndex, elemPosition, elemName, elemHandle, elemField, elemType, tags
        xxx, xxx,    xxx,       xxx,          xxx,      xxx,        xxx,       xxx,      tag1,tag2
    In format 1, any column does not have a header label is treated as a tag.

    Format 2 (explicit):
        PV,machine=xxx,elemIndex=xxx,elemPosition=xxx,elemName=xxx,elemHandle=xxx,elemField=xxx,elemType=xxx,tag1,tag2

    :param data:
    :param csvname: output file name
    :param frmt:    output file format as described above.
    :return:
    """
    if frmt == "table":
        _save_csv_table(data, csvname)
    elif frmt == "explicit":
        _save_csv_explicit(data, csvname)
    else:
        raise CSVFormatError("CSV file format {0} not supported yet.".format(format))
    
