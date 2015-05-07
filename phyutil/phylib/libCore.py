"""
Core APHLA Libraries
---------------------

Defines the fundamental routines.
"""

# :author: Lingyun Yang

import os
import logging
from datetime import datetime

from lattice import element
from .. import machine

_logger = logging.getLogger(__name__)

def getTimestamp(t = None, us = True):
    """
    generate the timestamp string

    t - user provided datetime object or new a datetime.now()
    us - with microsecond or not.
    """
    fmt = "%Y-%m-%d_%H:%M:%S"
    if us: fmt = fmt + ".%f"
    if t is None:
        t = datetime.now()

    return t.strftime(fmt)

def getOutputDir():
    """get the output data dir for the current lattice""" 
    return machine._lat.OUTPUT_DIR

def getElements(group, include_virtual=False, start=None, end=None):
    """searching for elements.
    If start is not `None`, get elements from start point.
    If end is not `None`, get elements before end point.
    If both are not `None`, get elements in between, otherwise, get all found elements. 


    this calls :func:`~aphla.lattice.Lattice.getElementList` of the current
    lattice.

    The default does not include virtual element.

    Parameters
    -----------
    group : str, list. a list of element name or a name pattern.
    include_virtual : include virtual element or not.
    start:  start from
    end:    end before

    Returns
    ---------
     elemlist : a list of matched element objects.
    
    Examples
    ----------
    >>> getElements('NO_SUCH_ELEMENT')
      []
    >>> getElements('PH1G2C30A')
      [PH1G2C30A:BPM @ sb=4.935000]
    >>> getElements('BPM')
      ...
    >>> getElements('F*G1C0*')
      ...
    >>> getElements(['FH2G1C30A', 'FH2G1C28A'])
      ...

    """
    # return the input if it is a list of element object
    if isinstance(group, element.AbstractElement):
        return [group]
    elif isinstance(group, (list, tuple)):
        if all([isinstance(e, element.AbstractElement) for e in group]):
            return group

    elems = machine._lat.getElementList(group)
    ret = []
    for e in elems:
        if e is None: 
            ret.append(e)
            continue

        if not include_virtual and e.virtual: 
            continue
        if start is None and end is None:
            # both start and end are None
            ret.append(e)
        elif start is None and e.se <= end:
            # get elements before end
            ret.append(e)
        elif end is None  and e.sb >= start:
            # get elements after start
            ret.append(e)
        elif e.se <= end and e.sb >= start:
            # get elements in between
            ret.append(e)
    return ret

def getExactElement(elemname):
    """find the element with exact name"""
    return machine._lat._find_exact_element(name=elemname)

def getPvList(elems, field, handle='readback', **kwargs):
    """return a pv list for given element or element list

    Parameters
    ------------
    elems : element pattern, name list or CaElement object list
    field : e.g. 'x', 'y', 'k1'
    handle : 'readback' or 'setpoint'

    Keyword arguments:

      - *first_only* (False) use only the first PV for each element. 
      - *compress_empty* (False) remove element with no PV.

    :Example:

      >>> getPvList('p*c30*', 'x')

    This can be simplified as::

      [e.pv(field) for e in getElements(elem) if field in e.fields()]

    extract the pv only if the element has that field (compress_empty=True).

      [e.pv(field) if field in e.fields() else None for e in getElements(elem)]

    put a None in the list if the field is not in that element

    *elem* accepts same input as :func:`getElements`
    """
    first_only = kwargs.get('first_only', False)
    compress_empty = kwargs.get('compress_empty', False)

    # did not check if it is a BPM 
    elemlst = getElements(elems)
    pvlst = []
    for elem in elemlst:
        if not isinstance(elem, element.CaElement):
            raise ValueError("element '%s' is not CaElement" % elem.name)
        
        pvs = elem.pv(field=field, handle=handle)
        if len(pvs) == 0 and not compress_empty:
            raise ValueError("element '%s' has no readback pv" % elem.name)
        elif len(pvs) > 1 and not first_only:
            raise ValueError("element '%s' has more %d (>1) pv" % 
                             (elem.name, len(pvs)))

        pvlst.append(pvs[0])

    return pvlst

def getLocations(group):
    """
    Get the location of a group, i.e. a family, an element or a list of
    elements

    Examples
    ---------

    >>> s = getLocations('BPM')
    >>> s = getLocations(['PM1G4C27B', 'PH2G2C28A'])

    It has a same input as :func:`getElements` and accepts group name,
    element name, element name pattern and a list of element names.
    """
    
    elem = getElements(group)
    if isinstance(elem, (list, set, tuple)):
        return [e.sb for e in elem]
    else: return elem.sb

def addGroup(group):
    """
    add a new group to current sub-machine.

    *group* should be plain string, characters in \[a-zA-Z0-9\_\]

    raise *ValueError* if *group* is an illegal name.

    it calls :func:`~aphla.lattice.Lattice.addGroup` of the current lattice.
    """
    return machine._lat.addGroup(group)

def removeGroup(group):
    """
    Remove a group if it is empty. It calls
    :func:`~aphla.lattice.Lattice.removeGroup` of the current lattice.
    """
    machine._lat.removeGroup(group)

def addGroupMembers(group, member):
    """
    add new members to an existing group

    ::

      >>> addGroupMembers('HCOR', 'CX1')
      >>> addGroupMembers('HCOR', ['CX1', 'CX2']) 

    it calls :meth:`~aphla.lattice.Lattice.addGroupMember` of the current
    lattice.
    """
    if isinstance(member, str):
        machine._lat.addGroupMember(group, member)
    elif isinstance(member, list):
        for m in member:
            machine._lat.addGroupMember(group, m)
    else:
        raise ValueError("member can only be string or list")

def removeGroupMembers(group, member):
    """
    Remove a member from group

    ::

      >>> removeGroupMembers('HCOR', 'CX1')
      >>> removeGroupMembers('HCOR', ['CX1', 'CX2'])

    it calls :meth:`~aphla.lattice.Lattice.removeGroupMember` of the current
    lattice.
    """
    if isinstance(member, str):
        machine._lat.removeGroupMember(group, member)
    elif isinstance(member, list):
        for m in member: machine._lat.removeGroupMember(group, m)
    else:
        raise ValueError("member can only be string or list")


def getGroups(element='*'):
    """
    Get all groups own these elements, '*' returns all possible groups,
    since it matches every element
    
    it calls :func:`~aphla.lattice.Lattice.getGroups` of the current lattice.
    """
    return machine._lat.getGroups(element)

def getGroupMembers(groups, op='intersection', **kwargs):
    """
    Get all elements in a group. If group is a list, consider which op:

    - op = "union", consider elements in the union of the groups
    - op = "intersection", consider elements in the intersect of the groups

    it calls :func:`~aphla.lattice.Lattice.getGroupMembers` of the current
    lattice.
    """
    return machine._lat.getGroupMembers(groups, op, **kwargs)

def getNeighbors(element, group, n=3, elemself=True):
    """
    Get a list of n objects in *group* before and after *element* 

    it calls :meth:`~aphla.lattice.Lattice.getNeighbors` of the current
    lattice to get neighbors.

    Parameters
    -----------
    element: str, object. the central element name
    group: str, the neighbors belong to
    n : int, default 3, number of neighbors each side. 
    elemself : default True, return the element itself.

    Returns
    --------
    elems : a list of element in given group. The list is
        sorted along s (the beam direction). There is 2*n+1 elements if
        elemself=True, else 2*n.


    Examples
    ----------
    >>> getNeighbors('X', 'BPM', 2) # their names are ['1','2','X', '3', '4']
    >>> getNeighbors('QC', 'QUAD', 1) # their names are ['Q1', 'QC', 'Q2']
    >>> el = hla.getNeighbors('PH2G6C25B', 'P*C10*', 2)
    >>> [e.name for e in el]
      ['PL2G6C10B', 'PL1G6C10B', 'PH2G6C25B', 'PH1G2C10A', 'PH2G2C10A']
    >>> [e.sb for e in el]
      [284.233, 286.797, 678.903, 268.921, 271.446]
    >>> hla.getNeighbors("X", ["BPM", "QUAD"], 2)
    """

    if isinstance(element, (str, unicode)):
        return machine._lat.getNeighbors(element, group, n, elemself)
    else:
        return machine._lat.getNeighbors(element.name, group, n, elemself)

def getClosest(element, group):
    """
    Get the closest neighbor in *group* for an element

    It calls :meth:`~aphla.lattice.Lattice.getClosest`

    Parameters
    -----------
    element: str, object. the element name or object
    group: str, the closest neighbor belongs to this group

    Examples
    ----------
    >>> getClosest('pm1g4c27b', 'BPM') # find the closest BPM to 'pm1g4c27b'
    >>> getClosest('pm1g4c27b', ["QUAD", "BPM"])
    """
    if isinstance(element, (str, unicode)):
        return machine._lat.getClosest(element, group)
    else:
        return machine._lat.getClosest(element.name, group)

def getBeamlineProfile(**kwargs):
    """
    return the beamline profile from sposition sb to se

    :param float s1: s-begin
    :param float s2: s-end, None means the end of beamline.

    it calls :meth:`~aphla.lattice.Lattice.getBeamlineProfile` of the
    current lattice.
    """
    return machine._lat.getBeamlineProfile(**kwargs)

def getDistance(elem1, elem2, absolute=True):
    """
    return distance between two element name

    Parameters
    -----------
    elem1: str, object. name or object of one element
    elem2: str, object. name or object of the other element
    absolute: bool. return s2 - s1 or the absolute value.

    Raises
    -------
    it raises RuntimeError if None or more than one elements are found
    """
    e1 = getElements(elem1)
    e2 = getElements(elem2)

    if len(e1) != 1 or len(e2) != 1:
        raise RuntimeError("elements are not uniq: %d and %d" % \
                           (len(e1), len(e2)))

    ds = e2[0].sb - e1[0].sb
    C = machine._lat.circumference
    if machine._lat.loop and C > 0:
        while ds < -C: ds = ds + C
        while ds > C: ds = ds - C
    if absolute: return abs(ds)
    else: return ds

def getBpms():
    """
    return a list of bpms object.

    this calls :func:`~aphla.lattice.Lattice.getGroupMembers` of current
    lattice and take a "union".
    """
    return machine._lat.getGroupMembers('BPM', op='union')

def getQuads():
    """
    return a list of bpms object.

    this calls :func:`~aphla.lattice.Lattice.getGroupMembers` of current
    lattice and take a "union".
    """
    return machine._lat.getGroupMembers('QUAD', op='union')

def outputFileName(group, subgroup, create_path = True):
    """generate the system default output data file name

    'Lattice/Year_Month/group/subgroup_Year_Month_Day_HourMinSec.hdf5'
    e.g. 'SR/2014_03/bpm/bpm_Fa_0_2014_03_04_145020.hdf5'

    if new directory is created, with permission "rwxrwxr-x"
    """
    # use the default file name
    import stat
    t0 = datetime.now()
    output_dir = ""
    for subdir in [machine.getOutputDir(), t0.strftime("%Y_%m"), group]:
        output_dir = os.path.join(output_dir, subdir)
        if not os.path.exists(output_dir):
            if create_path:
                _logger.info("creating new directory: {0}".format(output_dir))
                os.mkdir(output_dir)
                os.chmod(output_dir, stat.S_ISGID | stat.S_IRWXU | stat.S_IRWXG | \
                         stat.S_IROTH | stat.S_IXOTH)
            else:
                raise RuntimeError("{0} does not exist".format(output_dir))

    fopt = subgroup + t0.strftime("%Y_%m_%d_%H%M%S.hdf5")
    return os.path.join(output_dir, fopt)

def getBoundedElements(group, s0, s1):
    """
    get list of elements within [s0, s1] or outside.

    group - pattern, name, type, see `getElements`
    s0, s1 - the boundary
    outside - True: inside boundary [s0,s1], False: in [0, s0] or [s1, end]

    if s0 > s1, it will be treated as a ring.

    >>> inside, outside = getBoundedElements("BPM", 700, 100)

    The returned elements are sorted in s order. In the case of s0 > s1, it
    starts from [0, s0] and then [s1, end].
    """

    allelems = getElements(group)
    inside = [False] * len(allelems)
    for i,e in enumerate(allelems):
        # keep the elements fully inside [s0, s1]
        if s1 > s0 and e.sb > s0 and e.se < s1:
            inside[i] = True
        elif s1 < s0 and (e.sb > s0 or e.se < s1):
            inside[i] = True
        else:
            inside[i] = False

    return ([e for i,e in enumerate(allelems) if inside[i]],
            [e for i,e in enumerate(allelems) if not inside[i]])

def saveElement(elem, output, h5group = "/"):
    """
    save element info to HDF5 file *output* in *h5group*
    """
    import h5py
    h5f = h5py.File(output)
    grp = h5f.require_group(h5group)
    for fld in elem.fields():
        try:
            val = elem.get(fld, handle="setpoint", unitsys=None)
            grp[fld + ".sp"] = val
        except:
            pass
        try:
            val = elem.get(fld, handle="readback", unitsys=None)
            grp[fld + ".rb"] = val
        except:
            pass
    grp.attrs["name"]   = elem.name
    grp.attrs["family"] = elem.family
    grp.attrs["cell"]   = elem.cell
    grp.attrs["girder"] = elem.girder
    h5f.close()


def putElement(elem, output, h5group = "/", force = False):
    """
    put saved element data to hardware
    """
    import h5py
    h5f = h5py.File(output, 'r')
    grp = h5f[h5group]

    if elem.name != grp.attrs["name"]:
        _logger.warn("not same element name: %s != %s" % (
                elem.name, grp.attrs["name"]))
        if not force:
            h5f.close()
            return

    for fld in elem.fields():
        dsname = fld + '.sp'
        if dsname not in grp.keys():
            _logger.warn("%s not found in %s/%s" % (dsname, output, h5group))
            continue
        val = grp[dsname].value
        elem.put(fld, val, unitsys=None)
    h5f.close()


