#/usr/env/python

"""
Create Lattice object from PV data

:author: Lingyun Yang
:date: 2012-07-09 16:50

:modified: Guobao Shen
:date: 2015-03-27 13:26

A lattice is equivalent to a machine: a storage ring, a LINAC or a transport
line. 

the lattice object manages a set of elements
(e.g. :class:`~aphla.element.CaElement`) and their group information, a twiss
data, an orbit response matrix data and more.

seealso :mod:`~aphla.element`, :mod:`~aphla.twiss`, :mod:`~aphla.machines`
"""

from __future__ import print_function, unicode_literals

import os
import sys
import re
from math import log10
import numpy as np
import shelve
from fnmatch import fnmatch
import logging

from .element import AbstractElement
from .impact import LatticeFactory as ImpactLatticeFactory
from .impact import run_lattice as run_impact_lattice


logger = logging.getLogger(__name__)

class Lattice(object):
    """Lattice class. It assumes all elements inside this lattice has a 
    unique name.

    - *name*
    - *mode*
    - *source* where it was created. URL, Sqlite3 DB filename, ...
    - *sb*, *se* s-position of begin and end.
    - *tune* [nux, nuy], mainly for circular machine
    - *chromaticity* [cx, cy] mainly for circular machine
    - *ormdata* orbit response matrix data
    - *mtype* as a ring (=1) or line (=0)
    - *simulation* the type of simulation (ie IMPACT, etc)
    - *kwargs* other arguments based on the simulation
    """
    # ignore those "element" when construct the lattice object
    def __init__(self, name, source='undefined', mode='', mtype=0, simulation='IMPACT', **kwargs):
        self.machine = ''
        self.machdir = ''
        self.name = name
        self._twiss = None
        # group name and its element
        self._group = {}
        # guaranteed in the order of s.
        self._elements = []
        # data set
        self.mode = mode
        self.tune = [None, None]
        self.chromaticity = [None, None]
        self.sb = 0.0
        self.se = sys.float_info.max
        self.ormdata = None
        self.isring = bool(mtype)
        self.Ek = None
        self.arpvs = None
        self.OUTPUT_DIR = ''
        self.source = source
        self.latticemodelmap = None
        self.simulation = simulation.upper()

        if self.simulation == "IMPACT":
            self._latticeFactory = ImpactLatticeFactory(kwargs.get("layout", None), **kwargs)
        else:
            raise RuntimeError("Lattice: Simulation code '{}' not supported".format(self.simulation))


    def set(self, name, fieldvalue, value=None):
        """Set the value of a lattice element field (ie settings).
        
        If no field name is given, then the element must only contain a 
        single field.

        Parameters
        ----------
        name : 
            Element name or element object.
        fieldvalue :
            If the value parameter is given then this is the name of an
            element field, otherwise, this is the value of the field.
        value :
            Value of the field if set, or None.
        """
        if self.simulation == "IMPACT":
            if not isinstance(name, AbstractElement):
                elms = self.getElementList(name)
                if len(elms) != 1:
                    raise RuntimeError("Lattice: Multiple elements found with the specified name.")
                name = elms[0]

            if value is not None:
                fds = [ fieldvalue ]
            else:
                fds = name.fields()

            if len(fds) != 1:
                raise RuntimeError("Lattice: Multiple fields found, must specify a field name.")

            if value is not None:
                self._latticeFactory.settings[name.name][fds[0]] = value
            else:
                self._latticeFactory.settings[name.name][fds[0]] = fieldvalue

        else:
            raise RuntimeError("Lattice: Simulation code '{}' not supported".format(self.simulation))

    def get(self, name, field=None):
        """Get the value of a lattice element field (ie setting).

        If no field name is given, then the element must only contain a single
        field.

        Parameters
        ----------
        name :
            Element name or element object
        field : 
            Optional field name

        Returns
        -------
        ret :
            Field value
        """
        if self.simulation == "IMPACT":
            if not isinstance(name, AbstractElement):
                elms = self.getElementList(name)
                if len(elms) != 1:
                    raise RuntimeError("Lattice: Multiple elements found with the specified name.")
                name = elms[0]

            if field is not None:
                fds = [ field ]
            else:
                fds = name.fields()

            if len(fds) != 1:
                raise RuntimeError("Lattice: Multiple fields found, must specify a field name.")

            return self._latticeFactory.settings[name.name][fds[0]]

        else:
            raise RuntimeError("Lattice: Simulation code '{}' not supported".format(self.simulation))

    def run(self):
        """Execute the simulation to update the model data.
        
        Returns
        -------
        p : 
            Path of the model data directory.
        """
        if self.simulation == "IMPACT":
            lat = self._latticeFactory.build()
            config = self._latticeFactory.config
            work_dir = run_impact_lattice(lat, config=config, work_dir=self.OUTPUT_DIR)
            if self.latticemodelmap is None:
                self.createLatticeModelMap(os.path.join(work_dir, "model.map"))
            return work_dir
        else:
            raise RuntimeError("Lattice: Simulation code '{}' not supported".format(self.simulation))


    def __getitem__(self, key):
        if isinstance(key, int):
            return self._elements[key]
        elif isinstance(key, str) or isinstance(key, unicode):
            return self._find_exact_element(name=key)
        else:
            return None

    def _find_exact_element(self, name):
        """Exact matching of element name, None if not.
        """
        if isinstance(name, AbstractElement):
            return name
        for e in self._elements:
            if e.name == name:
                return e
        return None

    def _find_element_s(self, s, eps=1e-9, loc='left'):
        """Given s location, find an element at this location, mostly return
        the element index mostly near s, by left/right approaching.

        If this is drift space, find the element at 'left' or 'right' of the
        given point.
        """
        if not loc in ['left', 'right']:
            raise ValueError('loc must be in ["left", "right"]')

        # normalize s into [0, C]
        sn = s
        if s > self.circumference: sn = s - self.circumference
        if s < 0: sn = s + self.circumference

        if sn < 0 or sn > self.circumference:
            raise ValueError("s= %f out of boundary ([%f, %f])"
                             % (s, -self.circumference, self.circumference))
        ileft, eleft = -1, self.circumference
        iright, eright = -1, self.circumference
        for i,e in enumerate(self._elements):
            if e.virtual > 0: continue
            # assuming elements is in order
            if abs(e.sb-s) <= eleft:
                ileft, eleft = i, abs(e.sb-s)
            if abs(e.se-s) <= eright:
                iright, eright = i, abs(e.se-s)
        if loc == 'left':
            return ileft
        elif loc == 'right':
            return iright

    def createLatticeModelMap(self, mapfile):
        """Create a mapping between lattice layout and model output from a file
        
        :param mapfile: file name which has mapping information.
        
        """
        mapping = np.loadtxt(mapfile, dtype=str)
        if self.latticemodelmap is not None:
            self.latticemodelmap.clear()
        else:
            self.latticemodelmap={}
        for idx, mp in enumerate(mapping):
            if mp[0] == "NONE":
                continue
            if mp[0] not in self.latticemodelmap:
                self.latticemodelmap[mp[0]] = {}
            if mp[1] not in self.latticemodelmap[mp[0]]:
                self.latticemodelmap[mp[0]][mp[1]] = []
            self.latticemodelmap[mp[0]][mp[1]].append(idx)

    def hasElement(self, name):
        """has the named element"""
        if self._find_exact_element(name):
            return True
        else:
            return False

    def insertElement(self, elem, i = None, groups = None):
        """insert an element at index *i* or append it.

        seealso :func:`appendElement`

        Parameters
        ------------
        elem : element object. :class:`~aphla.element.CaElement`, :class:`~aphla.element.AbstractElement`
        i : int. the index to insert. append if *None*
        groups : group names the element belongs to.

        """
        if i is not None:
            self._elements.insert(i, elem)
        else:
            if len(self._elements) == 0:
                self._elements.append(elem)
            else:
                k = 0
                for e in self._elements:
                    if e.sb < elem.sb: 
                        k += 1
                        continue
                if k == len(self._elements):
                    self._elements.append(elem)
                else:
                    self._elements.insert(k, elem)
        if groups is not None:
            for g in groups:
                if self._group.has_key(g):
                    self._group[g].append(elem)
                else:
                    self._group[g] = [elem]

    def getOverlapped(self):
        ret = []
        i = 0
        while i < len(self._elements):
            # for each element, searching the elements behind it
            j = i + 1
            ov = []
            while j < len(self._elements):
                if self._elements[j].sb < self._elements[i].se:
                    ov.append(self._elements[j].name)
                elif self._elements[j].sb >= self._elements[i].se:
                    break
                j = j + 1
            if ov:
                ret.append([self._elements[i].name] + ov)
            i = i + 1
        if ret:
            return ret
        else: return None

    def appendElement(self, elem):
        """append a new element to lattice. 

        callers are responsible for avoiding duplicate elements (call
        hasElement before).

        seealso :func:`insertElement`
        """
        self._elements.append(elem)

    def size(self):
        """total number of elements."""
        return len(self._elements)

    def remove(self, elemname):
        """remove the element, return None if not find the element."""
        for i,e in enumerate(self._elements):
            if e.name != elemname:
                continue
            return self._elements.pop(i)
        return None

    def save(self, fname, dbmode='c'):
        """save the lattice into binary data, using writing *dbmode*.

        see also Python Standard Lib `shelve`
        """
        f = shelve.open(fname, dbmode)
        pref = "lat.%s." % self.mode
        f[pref+'group']   = self._group
        f[pref+'elements'] = self._elements
        f[pref+'mode']    = self.mode
        f[pref+"source"]  = self.source
        f[pref+'tune']    = self.tune
        f[pref+'chromaticity'] = self.chromaticity
        f.close()

    def load(self, fname):
        """load the lattice from binary data

        In the db file, all lattice has a key with prefix 'lat.mode.'. If the
        given mode is empty string, then use 'lat.'
        
        seealso Python Standard Lib `shelve`
        """
        f = shelve.open(fname, 'r')
        pref = "lat."
        self._group  = f[pref+'group']
        self._elements  = f[pref+'elements']
        self.mode     = f[pref+'mode']
        self.source   = f[pref+"source"]
        self.tune     = f[pref+'tune']
        self.chromaticity = f[pref+'chromaticity']
        if self._elements:
            self.circumference = self._elements[-1].se
        f.close()

    def mergeGroups(self, parent, children):
        """merge child group(s) into a parent group

        the new parent group is replaced by this new merge of children
        groups. no duplicate element will appears in merged *parent* group
        
        Examples
        ---------
        >>> mergeGroups('BPM', ['BPMX', 'BPMY'])
        >>> mergeGroups('TRIM', ['TRIMX', 'TRIMY'])
        >>> mergeGroups('BPM', ['BPM', 'UBPM'])

        """
        if isinstance(children, str):
            chlist = [children]
        elif hasattr(children, '__iter__'):
            chlist = children[:]
        else:
            raise ValueError("children can be string or list of string")

        #if not self._group.has_key(parent):
        pl = []

        for child in chlist:
            if not self._group.has_key(child):
                logger.warn("WARNING: no %s group found" % child)
                continue
            for elem in self._group[child]:
                if elem in pl: continue
                pl.append(elem)
        self._group[parent] = pl
            
    def sortElements(self, namelist = None):
        """
        sort the element list to the order of *s*

        use sorted() for a list of element object.

        The group needs to be rebuild, since *getElementList* relies on a 
        sorted group dict.
        """
        if not namelist:
            self._elements = sorted(self._elements)
            self.buildGroups()
            return
        
        ret = []
        for e in self._elements:
            if e.name in ret:
                continue
            if e.name in namelist:
                ret.append(e.name)

        #
        if len(ret) < len(namelist):
            raise ValueError("Some elements are missing in the results")
        elif len(ret) > len(namelist):
            raise ValueError("something wrong on sorting element list")
 
        return ret[:]

    def getLocations(self, elemsname):
        """
        if elems is a string(element name), do exact match and return
        single number.  if elems is a list do exact match on each of them,
        return a list. None if the element in this list is not found.

        .. warning::
        
          If there are duplicate elements in *elems*, only first
          appearance has location returned.

        :Example:

          >>> getLocations(['BPM1', 'BPM1', 'BPM1']) #doctest: +SKIP
          [0.1, None, None]

        """

        if isinstance(elemsname, str):
            e = self._find_exact_element(elemsname)
            return e.sb
        elif isinstance(elemsname, list):
            ret = [None] * len(elemsname)
            for elem in self._elements:
                if elem.name in elemsname:
                    idx = elemsname.index(elem.name)
                    ret[idx] = elem.s
            return ret
        else:
            raise ValueError("not recognized type of *elems*")

    def getLocationRange(self):
        s0, s1 = 0.0, 1.0
        for elem in self._elements:
            if elem.virtual:
                continue
            if isinstance(elem.sb, (int, float)): 
                s0 = elem.sb
                break
        for i in range(1, 1+len(self._elements)):
            elem = self._elements[-i]
            if elem.virtual:
                continue
            if isinstance(elem.se, (int, float)) and elem.se > s0:
                s1 = elem.se
                break
        return s0, s1

    def getLine(self, srange, eps = 1e-9):
        """
        get a list of element within range=(s0, s1).

        if s0 > s1, the range is equiv to (s0, s1+C), where C is the
        circumference.

        *eps* is the resolution.

        relying on the fact that element.s is the beginning of element.
        """
        s0, s1 = srange[0], srange[1]

        i0 = self._find_element_s(s0, loc='right')
        i1 = self._find_element_s(s1, loc='left')

        if i0 == None or i1 == None:
            return None
        elif i0 == i1:
            return self._elements[i0]
        elif i0 < i1:
            ret = self._elements[i0:i1+1]
        else:
            ret = self._elements[i0:]
            ret.extend(self._elements[:i1+1])
        return ret

    def getElementList(self, group, **kwargs):
        """
        get a list of element objects.

        Parameters
        -----------
        group : str, list. element name, pattern or name list.
            when it is str, searching for an element with name *group*, if not
            found, searching for a group with name *group*. At last treat it
            as a pattern to match the element names.  When the input *group*
            is a list, each string in this list will be treated as exact
            string instead of pattern.

        virtual : bool. optional(True). Including virtual element or not.

        Returns
        --------
        elemlst : a list of element objects.

        Examples
        ----------
        >>> getElementList('BPM')
        >>> getElementList('PL*')
        >>> getElementList('C02')
        >>> getElementList(['BPM1', 'BPM2'])

        """

        virtual = kwargs.get('virtual', True)
        # do exact element name match first
        elem = self._find_exact_element(group)
        if elem is not None: 
            return [elem]

        # do exact group name match
        if group in self._group.keys():
            return self._group[group][:]

        if isinstance(group, str) or isinstance(group, unicode):
            # do pattern match on element name
            ret, names = [], []
            for e in self._elements:
                if e.name in names:
                    continue
                if not virtual and e.virtual:
                    continue
                if fnmatch(e.name, group):
                    ret.append(e)
                    names.append(e.name)
            return ret
        elif isinstance(group, list):
            # exact one-by-one match, None if not found
            return [self._find_exact_element(e) for e in group]
            
    def _matchElementCgs(self, elem, **kwargs):
        """check properties of an element
        
        - *cell*
        - *girder*
        - *symmetry*
        """

        cell = kwargs.get("cell", None)
        
        if isinstance(cell, str) and elem.cell != cell:
            return False
        elif hasattr(cell, "__iter__") and not elem.cell in cell:
            return False

        girder = kwargs.get("girder", None)
        
        if isinstance(girder, str) and elem.girder != girder:
            return False
        elif hasattr(girder, "__iter__") and not elem.girder in girder:
            return False

        symmetry = kwargs.get("symmetry", None)
        
        if isinstance(symmetry, str) and elem.symmetry != symmetry:
            return False
        elif hasattr(symmetry, "__iter__") and not elem.symmetry in symmetry:
            return False

        return True

    def _getElementsCgs(self, group = '*', **kwargs):
        """
        call signature::
        
          getElementsCgs(group)

        Get a list of elements from cell, girder and sequence

        - *cell*
        - *girder*
        - *symmetry*

        :Example:

            >>> getElementsCgs('BPMX', cell=['C20'], girder=['G2'])

        When given a general group name, check the following:

        - element name
        - element family
        - existing *group*: 'BPM', 'BPMX', 'BPMY', 'A', 'C02', 'G4'

            - cell
            - girder
            - symmetry
        """

        # return empty set if not specified the group
        if not group: return None
        
        elem = []
        for e in self._elements:
            # skip for duplicate
            if e.name in elem: continue

            if not self._matchElementCgs(e, **kwargs):
                continue
            
            if e.name in self._group.get(group, []):
                elem.append(e.name)
            elif fnmatch(e.name, group):
                elem.append(e.name)
            else:
                pass
                
            #if cell and not e.cell in cell: continue
            #if girder and not e.girder in girder: continue
            #if symmetry and not e.symmetry in symmetry: continue
        
        return elem

    def _illegalGroupName(self, group):
        # found character not in [a-zA-Z0-9_]
        if not group: return True
        elif re.search(r'[^\w:]+', group):
            #raise ValueError("Group name must be in [a-zA-Z0-9_]+")
            return True
        else: return False

    def buildGroups(self):
        """
        clear the old groups, fill with new data by collecting group name
        that each element belongs to.

        - the elements must be in s order
        """
        # cleanr everything
        self._group = {}
        for e in self._elements:
            for g in e.group:
                if self._illegalGroupName(g):
                    continue
                #self.addGroupMember(g, e.name, newgroup=True)
                lst = self._group.setdefault(g, [])
                lst.append(e)

    def addGroup(self, group):
        """
        create a new group

        :Example:
        
            >>> addGroup(group)
          
        Input *group* is a combination of alphabetic and numeric
        characters and underscores. i.e. "[a-zA-Z0-9\_]"

        raise ValueError if the name is illegal or the group already exists.
        """
        if self._illegalGroupName(group):
            raise ValueError('illegal group name %s' % group)

        if not self._group.has_key(group):
            self._group[group] = []
        else:
            raise ValueError('group %s exists' % group)

    def removeGroup(self, group):
        """
        remove a group only when it is empty
        """
        if self._illegalGroupName(group):
            return
        if not self._group.has_key(group):
            raise ValueError("Group %s does not exist" % group)
        if len(self._group[group]) > 0:
            raise ValueError("Group %s is not empty" % group)
        # remove it!
        self._group.pop(group)

    def addGroupMember(self, group, member, newgroup=False):
        """
        add a member to group

        if newgroup == False, the group must exist before.
        """

        elem = self._find_exact_element(member)
        if not elem:
            raise ValueError("element %s is not defined" % member)

        if self.hasGroup(group):
            if elem in self._group[group]:
                return
            elem.group.add(group)
            for i,e in enumerate(self._group[group]):
                if e.sb < elem.sb:
                    continue
                self._group[group].insert(i, elem)
                break
            else:
                self._group[group].append(elem)
        elif newgroup:
            self._group[group] = [elem]
            elem.group.add(group)
        else:
            raise ValueError("Group %s does not exist."
                             "use newgroup=True to add it" % group)

    def hasGroup(self, group):
        """
        check if group exists or not.
        """
        return self._group.has_key(group)

    def removeGroupMember(self, group, member):
        """
        remove a member from group
        """
        if not self.hasGroup(group):
            raise ValueError("Group %s does not exist" % group)
        if member in self._group[group]:
            self._group[group].remove(member)
        else:
            raise ValueError("%s not in group %s" % (member, group))

    def getGroups(self, element=None):
        """
        return a list of groups this element belongs to

        :Example:

            >>> getGroups() # list all groups, including the empty groups
            >>> getGroups('*') # all groups, not including empty ones
            >>> getGroups('Q?')
          
        The input string is wildcard matched against each element.
        """
        if element is None:
            return self._group.keys()

        ret = []
        for k, elems in self._group.items():
            for e in elems:
                if fnmatch(e.name, element):
                    ret.append(k)
                    break
        return ret

    def getGroupMembers(self, groups, op, **kwargs):
        """
        return members in a list of groups. 

        can take a union or intersections of members in each group

        - *groups* can be a list of exact group name, pattern or both.
        - op = ['union' | 'intersection']

        :Example:
        
            >>> getGroupMembers(['C0[2-3]', 'BPM'], op = 'intersection')

        Note: an element pattern, e.g. "p*g1c23a" is not a pattern of `groups`
        """
        if not groups:
            return None
        ret = {}

        if groups in self._group.keys():
            return self._group[groups]

        for g in groups:
            ret[g] = []
            imatched = 0
            for k, elems in self._group.items():
                if fnmatch(k, g): 
                    imatched += 1
                    ret[g].extend([e.name for e in elems])


        r = set(ret[groups[0]])
        if op.lower() == 'union':
            for g, v in ret.items():
                r = r.union(set(v))
        elif op.lower() == 'intersection':
            for g, v in ret.items():
                r = r.intersection(set(v))
        else:
            raise ValueError("%s not defined" % op)
        
        return self.getElementList(self.sortElements(r))

    def getNeighbors(self, elemname, groups, n, elemself=True):
        """
        Assuming self._elements is in s order

        the element matched with input 'element' string should be unique
        and exact.

        If the input *element* name is also in one of the *groups*, no
        duplicate the result.
        
        For a linear machine, it will fill `None` is there is no enough elements in upstream or in downstream. 

        :Example:

            >>> getNeighbors('P4', 'BPM', 2)
            ['P2', 'P3', 'P4', 'P5', 'P6']
            >>> getNeighbors('Q3', 'BPM', 2)
            ['P2', 'P3', 'Q3', 'P4', 'P5']
            >>> getNeighbors('Q3', ["BPM", "SEXT"], 2)
        """

        e0 = self._find_exact_element(elemname)
        if not e0:
            raise ValueError("element %s does not exist" % elemname)

        el = []
        if isinstance(groups, (str, unicode)):
            el = self.getElementList(groups, virtual=0)
        elif isinstance(groups, (list, tuple)):
            el = self.getGroupMembers(groups, op="union")

        if not el:
            raise ValueError("elements/group %s does not exist" % groups)
        if e0 in el:
            el.remove(e0)

        i0 = len(el)
        for i, e in enumerate(el):
            if e.sb < e0.sb: 
                continue
            i0 = i
            break
        ret = [e0] if elemself else []
        for i in range(n):
            _, r = divmod(i0 - i - 1, len(el))
            if self.isring or el[r].sb < e0.sb:
                # insert into the front no matter what for a ring  
                # or when the position is smaller than that of current element for a linear machine
                ret.insert(0, el[r])
            else:
                ret.insert(0, None)
            _, r = divmod(i0 + i, len(el))
            if self.isring or el[r].sb > e0.sb:
                # append into the list no matter what for a ring  
                # or when the position is larger than that of current element for a linear machine
                ret.append(el[r])
            else:
                ret.append(None)
        return ret
        
    def getClosest(self, elemname, groups):
        """
        Assuming self._elements is in s order

        the element matched with input 'element' string should be unique
        and exact.

        :Example:

            >>> getClosest('P4', 'BPM')
            >>> getClosest('Q3', 'BPM')
            >>> getClosest('Q3', ["QUAD", "SEXT"])

        The result can not be virtual element.
        """

        e0 = self._find_exact_element(elemname)
        if not e0:
            raise ValueError("element %s does not exist" % elemname)

        el = []
        if isinstance(groups, (str, unicode)):
            el = self.getElementList(groups, virtual=0)
        elif isinstance(groups, (list, tuple)):
            el = self.getGroupMembers(groups, op="union")

        if not el: raise ValueError("elements/group %s does not exist" % groups)

        idx, ds = 0, el[-1].sb
        for i,e in enumerate(el):
            if e == e0: continue
            if isinstance(e.sb, (list, tuple)):
                ds0 = abs(e.sb[0] - e0.sb)
            else:
                ds0 = abs(e.sb - e0.sb)
            if ds0 > ds: continue
            idx = i
            ds = ds0

        return el[idx]
        
    def __repr__(self):
        s0 = '#name of submachine: {}'.format(self.name)
        s1 = '#{0:<6s}{1:^20s} {2:<10s} {3:<10s} {4:<10s}'.format(
                'index', 'name', 'family', 'position', 'length'
                )
        ret = [s0, s1]

        ml_name, ml_family = 0, 0
        for e in self._elements:
            if len(e.name) > ml_name: ml_name = len(e.name)
            if e.family and len(e.family) > ml_family:
                ml_family = len(e.family)

        idx = 1
        if len(self._elements) >= 10:
            idx = int(1.0+log10(len(self._elements)))
        fmt = "{idx:<6d} {name:<20s} {family:<10s} {pos:<10.4f} {len:<10.4f}" 
        for i, e in enumerate(self._elements):
            if e.virtual: continue
            ret.append(fmt.format(idx=i, name=e.name, family=e.family, 
                                  pos=e.sb, len=e.length))            
        return '\n'.join(ret)
