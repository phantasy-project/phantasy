"""
Element
~~~~~~~

.. moduleauthor:: Lingyun Yang
.. moduledate:: 2011-05-13 10:28
"""

import re
import copy
import logging
# from unitconv import *

# public symbols
_logger = logging.getLogger(__name__)

# flags bit pattern
_DISABLED = 0x01
_READONLY = 0x02

UNSPECIFIED = 0
ASCENDING   = 1
DESCENDING  = 2
RANDOM      = 3

class AbstractElement(object):
    """The :class:`AbstractElement` contains most of the lattice properties,
    such as element name, length, location and family. It also keeps a list of
    groups which belongs to. The default group list contains cell, girder,
    family and symmetry information if they are valid.

    AbstractElement has no Channel Access abilities. The AbstractElement can
    be created with the following optional parameters
    
    ==========  ===================================================
    Variable    Meaning
    ==========  ===================================================
    *name*      element name
    *index*     index
    *devname*   device name
    *phylen*    physical(yoke) length
    *family*    family
    *sb*        s position of the entrance
    *se*        s position of the exit
    *length*    effective(magnetic) length 
    *cell*      cell name
    *girder*    girder name
    *symmetry*  symmetry type
    *sequence*  sequence tuple
    *group*     list of groups the element belongs to
    ==========  ===================================================

    *index* is used for sorting elements in a list if it is not
    None. Otherwise sorted according to *sb*.
    """

    # format string for __str__
    _STR_FORMAT = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}"
    #__slots__ = []
    def __init__(self, **kwargs):
        """
        create an element from Channel Finder Service data or explicit
        parameters.

        :param str name: element name
        """
        #print kwargs
        self.name     = kwargs.get('name', None)
        self.devname  = kwargs.get('devname', None)
        self.phylen   = float(kwargs.get('phylen', '0.0'))
        self.index    = int(kwargs.get('index', '-1'))
        self.family   = kwargs.get('family', None)
        self.se       = float(kwargs.get('se', 'inf'))
        self.sb       = float(kwargs.get('sb', 'inf'))
        self.length   = float(kwargs.get('length', '0.0'))
        self.cell     = kwargs.get('cell', None)
        self.girder   = kwargs.get('girder', None)
        self.symmetry = kwargs.get('symmetry', None)
        self.sequence = kwargs.get('sequence', (0, 0))
        self.flag   = 0

        self.group = set([self.family, self.cell, self.girder, self.symmetry])
        for g in kwargs.get('group', []): 
            self.group.add(g)

    def profile(self, vscale=1.0):
        """the profile for drawing the lattice.

        The return is a tuple of (x, y, color) where (*x*, *y) are coordinates
        and *color* is one of the ['k', 'r', 'b'] depending its family.
        
        It recognize the following *family*:

        - 'QUAD', quadrupole, box height *vscale*, no negative
        - 'BEND', dipole. box height vscale both positive and negative.
        - 'SEXT', sextupole. box height 1.4*vscale
        - 'SOL', solenoid, box height 0.8*vscale
        - 'CAV', RF cavity,  box height 1.8*vscale
        - ['HCOR' | 'VCOR' | 'TRIMX' | 'TRIMY' | 'DCH' | 'DCV'], corrector, thin line
        - ['BPM' | 'BPMX' | 'BPMY' | 'PM'], beam position monitor, profile monitor, thin line
        - The rest unrecognized element, it returns a box with height 
          0.2*vscale and color 'k'.

        """
        b, e = self.sb, max(self.sb + self.length, self.se)
        h = vscale
        if self.family == 'CAV':
            return [b, b, e, e], [0, 1.8*h, 1.8*h, 0], 'k'
        elif self.family == 'SOL':
            return [b, b, e, e], [0, 0.8*h, 0.8*h, 0], 'k'
        elif self.family == 'QUAD':
            return [b, b, e, e], [0, h, h, 0], 'k'
        elif self.family == 'BEND':
            return [b, b, e, e, b, b, e, e], [0, h, h, -h, -h, h, h, 0], 'k'
        elif self.family == 'SEXT':
            return [b, b, e, e], [0, 1.4*h, 1.4*h, 0], 'k'
        elif self.family in ['HCOR', 'VCOR', 'TRIMX', 'TRIMY', 'DCH', 'DCV']:
            return [b, (b+e)/2.0, (b+e)/2.0, (b+e)/2.0, e], \
                [0, 0, h, 0, 0], 'r'
        elif self.family in ['BPM', 'BPMX', 'BPMY', 'PM']:
            return [b, (b+e)/2.0, (b+e)/2.0, (b+e)/2.0, e], \
                [0, 0, h, 0, 0], 'b'
        else:
            return [b, b, e, e], [0, 0.2*h, 0.2*h, 0], 'k'

    def __str__(self):
        return AbstractElement._STR_FORMAT.format(
            self.index, self.name, self.family, self.sb, self.length,
            self.devname, self.cell, self.girder, self.symmetry, self.sequence)

    def __repr__(self):
        return "%s:%s @ sb=%f" % (self.name, self.family, self.sb)

    def __lt__(self, other):
        """use *index* if not None, otherwise use *sb*"""
        if self.index is None and other.index is None:
            return True
        elif self.index is None:
            return False
        elif other.index is None:
            return True
        elif self.index > 0 and other.index > 0:
            return self.sb < other.sb
        elif self.index > 0:
            return True
        elif other.index > 0:
            return False
        else:
            # both less than 0
            return self.index > other.index

    def __eq__(self, other):
        """compares location, length and name"""
        return self.sb == other.sb and \
               self.length == other.length and \
               self.index == other.index and \
               self.name == other.name

    def updateProperties(self, prpt):
        """
        Update the properties of this element.

        :param dict prpt: a dictionary with the following keys:

        - *devname* Device name
        - *cell* Cell
        - *girder* Girder
        - *symmetry* Symmetry
        - *phylen* Physical length
        - *length* Effective/magnetic length
        - *sb* s-loc of the entrance (effective length)
        - *se* s-loc of the exit (effective length)
        - *index* index in lattice

        This update will not synchronize element properties, e.g. calculate
        length from sb and se, or se from sb and length.
        """

        if prpt.has_key('family'):
            # rename the family name, append to group. The family name is kept
            # unique, but "pushed" old family name to group name
            newfam = prpt['family']
            if not newfam in self.group:
                # TODO more proper way to handle family 
                self.group.add(newfam)
            self.family = newfam
            
        if prpt.has_key('devname'):
            self.devname = prpt['devname']
        if prpt.has_key('cell'):
            self.cell = prpt['cell']
        if prpt.has_key('girder'):
            self.girder = prpt['girder']
        if prpt.has_key('symmetry'):
            self.symmetry = prpt['symmetry']
            
        if prpt.has_key('phylen'):
            self.phylen = float(prpt['phylen'])
        if prpt.has_key('length'):
            self.length = float(prpt['length'])
        if prpt.has_key('se'):
            self.se = float(prpt['se'])
        if prpt.has_key('sb'):
            self.sb = float(prpt['sb'])
        if prpt.has_key('index'):
            self.index = int(prpt['index'])

    def isEnabled(self):
        return not (self.flag & _DISABLED)

    def setEnabled(self, b):
        if b:
            self.flag = self.flag & ~_DISABLED
        else:
            self.flag = self.flag | _DISABLED

class CaAction(object):
    """Manages channel access for an element field.

    it manages a list of readback and setpoint PVs. Each PV has its own
    stepsize and value range.

    If *trace* is True, every readback/setpoint will be recorded for later
    reset/revert whenever the get/put functions are called. Extra history
    point can be recorded by calling *mark*.

    None in unit conversion means the lower level unit, like the PV in EPICS.
    """
    ALLDATA  = 0
    READBACK = 1
    SETPOINT = 2
    GOLDEN   = 3
    def __init__(self, **kwargs):
        self.pvrb = [] # readback pv
        self.pvsp = [] # setpoint pv
        # self.unitconv = {}
        self.ucrb = {}  # unit conversion for readback
        self.ucsp = {}  # unit conversion for setpoint
        self.golden = [] # some setpoint can saved as golden value
        self.pvh  = [] # step size
        self.pvlim = [] # lower/upper limit
        # buffer the initial value and last setting/reading
        self.pvrbunit = '' # unit for readback PVs
        self.pvspunit = '' # overwrite unit in unit conversions
        self.rb = []  # bufferred readback value
        self.sp = []  # bufferred setpoint value
        self._sp1 = [] # the last bufferred sp value when sp dimension changes.
        self.field = ''
        self.desc = kwargs.get('desc', None)
        self.order = ASCENDING
        self.opflags = 0
        self.trace = kwargs.get('trace', False)
        self.trace_limit = 200
        self.timeout = 2
        self.sprb_epsilon = 0

    def __eq__(self, other):
        return self.pvrb == other.pvrb and \
            self.pvsp == other.pvsp and \
            self.field == other.field and \
            self.desc == other.desc

    def _insert_in_order(self, lst, v):
        """
        insert `v` to an ordered list `lst`
        """
        if len(lst) == 0 or self.order == UNSPECIFIED:
            if isinstance(v, (tuple, list)): lst.extend(v)
            else: lst.append(v)
            return 0

        if self.order == ASCENDING:
            for i,x in enumerate(lst):
                if x < v: continue
                lst.insert(i, v)
                return i
        elif self.order == DESCENDING:
            for i,x in enumerate(lst):
                if x > v: continue
                lst.insert(i, v)
                return i

        lst.append(v)
        return len(lst) - 1

    def _unit_conv(self, x, src, dst, unitconv):
        if (src, dst) == (None, None): return x

        # try (src, dst) first
        uc = unitconv.get((src, dst), None)
        if uc is not None:
            return uc.eval(x)

        # then inverse (dst, src)
        uc = unitconv.get((dst, src), None)
        if uc is not None and uc.invertible:
            return uc.eval(x, True)
        else:
            raise RuntimeError("no method for unit conversion from "
                               "'%s' to '%s'" % (src, dst))

    def _all_within_range(self, v, lowhigh):
        """if lowhigh is not valid, returns true"""
        # did not check for string type
        if isinstance(v, (str, unicode)): return True
        if lowhigh is None: return True

        low, high = lowhigh
        if isinstance(v, (float, int)):
            if low is None: return v <= high
            elif high is None: return v >= low
            elif high <= low: return True
            elif v > high or v < low: return False
            else: return True
        elif isinstance(v, (list, tuple)):
            for vi in v:
                if not self._all_within_range(vi, lowhigh): return False
            return True
        else:
            raise RuntimeError("unknow data type '{0}:{1}'".format(v, type(v)))

    def setReadbackPv(self, pv, idx = None):
        """
        set/replace the PV for readback.
 
        :param str pv: PV name
        :param int idx: index in the PV list
 
        `idx` is needed if such readback has a list
        of PVs.  if idx is None, replace the original one. if idx is an index
        integer and pv is not a list, then replace the one with this index.
        """
        if idx is None:
            if isinstance(pv, (str, unicode)):
                self.pvrb = [pv]
            elif isinstance(pv, (tuple, list)):
                self.pvrb = [p for p in pv]
            while len(self.golden) < len(self.pvrb): self.golden.append(None)
        elif not isinstance(pv, (tuple, list)):
            while idx >= len(self.pvrb): self.pvrb.append(None)
            while idx >= len(self.golden): self.golden.append(None)
            self.pvrb[idx] = pv
        else:
            raise RuntimeError("invalid readback pv '%s' for position '%s'" %
                               (str(pv), str(idx)))
 
 
    def setSetpointPv(self, pv, idx = None, **kwargs):
        """
        set the PV for setpoint at position idx.
 
        :param str pv: PV name
        :param int idx: index in the PV list.
 
        if idx is None, replace the original one. if idx is an index integer
        and pv is not a list, then replace the one with this index.
 
        seealso :func:`setStepSize`, :func:`setBoundary`
        """
        #lim = kwargs.get("boundary", None)
        #h = kwargs.get("step_size", None)
        if idx is None:
            if isinstance(pv, (str, unicode)):
                self.pvsp = [pv]
            elif isinstance(pv, (tuple, list)):
                self.pvsp = [p for p in pv]
            #lim_h = [self._get_sp_lim_h(pvi) for pvi in self.pvsp]
            # None means not checked yet. (None, None) checked but no limit
            self.pvlim = [None] * len(self.pvsp)
            self.pvh = [None] * len(self.pvsp)
            self.golden = [None] * len(self.pvsp)
        elif not isinstance(pv, (tuple, list)):
            while idx >= len(self.pvsp):
                self.pvsp.append(None)
                self.pvh.append(None)
                self.pvlim.append(None)
                self.golden.append(None)
            self.pvsp[idx] = pv
            self.pvlim[idx] = None
            self.pvh[idx] = None
            self.golden[idx] = None
        else:
            raise RuntimeError("invalid setpoint pv '%s' for position '%s'" %
                               (str(pv), str(idx)))
 
        # roll the buffer.
        self._sp1 = self.sp
        self.sp = []

class CaElement(AbstractElement):
    """Element with Channel Access ability.

    'field' -> Object Attr.
    """
    __slots__ = []
    def __init__(self, **kwargs):
        """
        An element is homogeneous means, it use same get/put function on a
        list of variables to speed up.        
        """
        #AbstractElement.__init__(self, **kwargs)
        self.__dict__['_field'] = {}
        self.__dict__['_golden'] = {}  # the golden values for fields.
        self.__dict__['_pvtags'] = {}
        self.__dict__['_pvarchive'] = []
        self.__dict__['virtual'] = kwargs.get('virtual', 0)
        self.__dict__['trace'] = kwargs.get('trace', False)
        # the linked element, alias
        self.__dict__['alias'] = []

        # update all element properties
        super(CaElement, self).__init__(**kwargs)
        
    def __setstate__(self, data):
        for (name, value) in data.iteritems():
            if name in ['_field', '_pvtags']:
                self.__dict__[name] = value
            else:
                super(CaElement, self).__setattr__(name, value)
            
    def _pv_1(self, **kwargs):
        """Find the pv when len(kwargs)==1.
        
        - tag: 
        - tags: all tags are met
        - field: return pvrb + pvsp
        """
        if kwargs.get('tag', None):
            return self._pv_tags([kwargs['tag']])
        elif kwargs.get('tags', None):
            return self._pv_tags(kwargs['tags'])
        elif kwargs.get('field', None):
            att = kwargs['field']
            if self._field.has_key(att):
                decr = self._field[att]
                return decr.pvrb + decr.pvsp
            else:
                return []
        elif kwargs.get('handle', None):
            pvl = []
            if kwargs["handle"] == "setpoint":
                for _, act in self._field.items():
                    pvl.extend(act.pvsp)
            elif kwargs["handle"] == "readback":
                for _, act in self._field.items():
                    pvl.extend(act.pvrb)
            return pvl
        return []

    def _pv_tags(self, tags):
        """
        return pv list which has all the *tags*.
        """
        tagset = set(tags)
        return [pv for pv,ts in self._pvtags.iteritems()
                   if tagset.issubset(ts) and ts]

    def _pv_fields(self, fields):
        """
        return pv list which has all fields in the input
        """
        fieldset = set(fields)
        ret = []
        for k,v in self._field.iteritems():
            #print k, v
            if k in fieldset:
                ret.extend(v['eget'])
                ret.extend(v['eput'])
        return ret
            
    def pv(self, **kwargs):
        """Search for pv with specified *tag*, *tags*, *field*, *handle* or a
        combinatinon of *field* and *handle*.

        Examples
        --------
        >>> pv() # returns all pvs.
        >>> pv(tag='aphla.X')
        >>> pv(tags=['aphla.EGET', 'aphla.Y'])
        >>> pv(field = "x")
        >>> pv(field="x", handle='readback')

        See Also
        --------
        :class:`CaAction`
        """
        if len(kwargs) == 0:
            return self._pvtags.keys()
        elif len(kwargs) == 1:
            return self._pv_1(**kwargs)
        elif len(kwargs) == 2:
            handle = kwargs.get('handle', None)
            fd = kwargs.get('field', None)
            if fd not in self._field: return []
            if handle == 'readback':
                return self._field[kwargs['field']].pvrb
            elif handle == 'setpoint':
                return self._field[kwargs['field']].pvsp
            else:
                return []
        else: return []

    def hasPv(self, pv, inalias=False):
        """Check if this element has pv.

        inalias=True will also check its alias elements. 

        If the alias (child) has its aliases (grand children), they are not
        checked. (no infinite loop)
        """
        if self._pvtags.has_key(pv): return True
        if inalias == True:
            for e in self.alias: 
                #if e.hasPv(pv): return True
                if e._pvtags.has_key(pv): return True
        return False
        
    def addAliasField(self, newfld, fld):
        self._field[newfld] = copy.deepcopy(self._field[fld])

    def status(self):
        """String representation of value, golden setpoint, range for each
        field.
        """
        ret = self.name
        if not self._field.keys(): return ret

        maxlen = max([len(att) for att in self._field.keys()])
        head = '\n%%%ds: ' % (maxlen+2)
        for att in self._field.keys():
            decr = self._field[att]
            if not decr: continue
            val = decr.getReadback()
            val1 = decr.getGolden()
            val2 = decr.boundary()
            ret = ret + head % att + str(val) + " (%s) " % str(val1) + " [%s]" % str(val2)
        return ret

    def __getattr__(self, att):
        # called after checking __dict__
        if not self._field.has_key(att):
            raise AttributeError("element '%s' has no field '%s'" % 
                                 (self.name, att))
        else:
            decr = self._field.get(att, None)
            if decr is None:
                raise AttributeError("field %s of %s is not defined" \
                                         % (att, self.name))
            x = decr.getReadback()
            if x is not None: return x
            x = decr.getSetpoint()
            if x is not None: return x
            raise AttributeError("error when reading field %s" % att)

    def __setattr__(self, att, val):
        # this could be called by AbstractElement.__init__ or Element.__init__
        # Note: the quick way has wait=False
        if hasattr(super(CaElement, self), att):
            super(CaElement, self).__setattr__(att, val)
        elif self.__dict__['_field'].has_key(att):
            decr = self.__dict__['_field'][att]
            if not decr:
                raise AttributeError("field '%s' is not defined for '%s'" % (
                        att, self.name))
            if not decr.pvsp:
                raise ValueError("field '%s' in '%s' is not writable" % (
                        att, self.name))
            decr.putSetpoint(val, wait=False)
            # if _field_trig exists, trig it, do not wait
            decr_trig = self.__dict__['_field'].get(att + "_trig", None)
            if decr_trig:
                decr_trig.putSetpoint(1, wait=False)
        elif att in self.__dict__.keys():
            self.__dict__[att] = val
        else:
            # new attribute for superclass
            super(CaElement, self).__setattr__(att, val)
            #raise AttributeError("Error")
        for e in self.alias: e.__setattr__(att, val)

    def _get_unitconv(self, field, handle):
        if not self._field.has_key(field): return {}
        if handle == "readback":
            return self._field[field].ucrb
        elif handle == "setpoint":
            return self._field[field].ucsp
        else:
            return {}

    def convertible(self, field, src, dst, handle="readback"):
        """Check the unit conversion is possible or not.

        Parameters
        ----------
        field :
        src :
        dst :
        handle : ["readback"|"setpoint"|None]
            Check readback, setpoint or all handle values.

        Returns
        -------
        ret : True or False
            If no specified handle, returns False.
        """
        if not self._field.has_key(field): 
            return False

        if src is None and dst is None: 
            return True

        unitconv = self._get_unitconv(field, handle)

        if (src, dst) in unitconv: 
            return True
        
        uc = unitconv.get((dst, src), None)
        if uc is not None and uc.invertible: 
            return True
        return False

    def addUnitConversion(self, field, uc, src, dst, handle=None):
        """Add unit conversion for field.

        Parameters
        ----------
        field :
        src :
        dst :
        handle : ["readback"|"setpoint"|None].
            None means for every named handles.
        """
        # src, dst is unit system name, e.g. None for raw, phy
        if handle is None or handle == "readback":
            self._field[field].ucrb[(src, dst)] = uc
            if src is None: 
                self._field[field].pvrbunit = uc.srcunit
            elif dst is None: 
                self._field[field].pvrbunit = uc.dstunit
        if handle is None or handle == "setpoint":
            self._field[field].ucsp[(src, dst)] = uc
            if src is None: 
                self._field[field].pvspunit = uc.srcunit
            elif dst is None: 
                self._field[field].pvspunit = uc.dstunit

    def convertUnit(self, field, x, src, dst, handle="readback"):
        """Convert value x between units without setting hardware"""
        uc = self._get_unitconv(field, handle)
        return self._field[field]._unit_conv(x, src, dst, uc)

    def get_unit_systems(self, field, handle="readback"):
        """Get a list of all unit systems for field. 

        None is the lower level unit, e.g. in EPICS channel. Use convertible
        to see if the conversion is possible between any two unit systems.
        """
        unitconv = self._get_unitconv(field, handle)
        if not unitconv: 
            return [None]

        src, dst = zip(*(unitconv.keys()))

        ret = set(src).union(set(dst))
        return list(ret)

    def getUnitSystems(self, field=None, handle="readback"):
        """Return a list of available unit systems for field. 

        If no field specified, return a dictionary for all fields and their
        unit systems.

        None means the unit used in the lower level control system, e.g. EPICS.
        """
        if field is None:
            return dict([(f, self.get_unit_systems(f, handle)) for f \
                             in self._field.keys()])
        else:
            return self.get_unit_systems(field, handle)

    def getUnit(self, field, unitsys='phy', handle="readback"):
        """Get the unit symbol of a unit system, e.g. unitsys='phy'

        The unit name, e.g. "T/m" for integrated quadrupole strength, is
        helpful for plotting routines.

        return '' if no such unit system. A tuple of all handles when *handle*
        is None
        """
        if field in self._field.keys() and unitsys == None: 
            if handle == "readback":
                return self._field[field].pvrbunit
            elif handle == "setpoint":
                return self._field[field].pvspunit
            else:
                return ""

        unitconv = self._get_unitconv(field, handle)
        for k,v in unitconv.iteritems():
            if k[0] == unitsys: 
                return v.srcunit
            elif k[1] == unitsys: 
                return v.dstunit

        return ""

    def setUnit(self, field, u, unitsys='phy', handle="readback"):
        """Set the unit symbol for a unit system.
        """
        if field not in self._field.keys(): 
            raise RuntimeError("element '%s' has no '%s' field" % \
                                   self.name, field)

        if unitsys is None: 
            self._field[field].pvunit = u
        
        for k,v in self._get_unitconv(field, handle).iteritems():
            if k[0] == unitsys: 
                v.srcunit = u
            elif k[1] == unitsys: 
                v.dstunit = u

    def getEpsilon(self, field):
        return self._field[field].sprb_epsilon

    def setEpsilon(self, field, eps):
        self._field[field].sprb_epsilon = eps

    def updatePvRecord(self, pvname, properties, tags = []):
        """Update the pv with property dictionary and tag list."""
        if not isinstance(pvname, (str, unicode)):
            raise TypeError("%s is not a valid type" % (type(pvname)))

        # update the properties
        if properties is not None: 
            self.updateProperties(properties)

        # the default handle is 'readback'
        if properties is not None:
            elemhandle = properties.get('handle', 'readback')
            fieldfname = properties.get('field', None)
            pvunit = properties.get('unit', '')
            if fieldfname is not None:
                g = re.match(r'([\w\d]+)(\[\d+\])?', fieldfname)
                if g is None:
                    raise ValueError("invalid field '%s'" % fieldfname)
                fieldname, idx = g.group(1), g.group(2)
                if idx is not None: 
                    idx = int(idx[1:-1])
                if elemhandle == 'readback': 
                    self.setGetAction(pvname, fieldname, idx)
                elif elemhandle == 'setpoint':
                    self.setPutAction(pvname, fieldname, idx)
                elif elemhandle == 'readset':
                    # TODO Add support for read set pvs
                    # slient ignore that handle for now
                    pass
                else:
                    raise ValueError("invalid handle value '%s' for pv '%s'" % 
                                     (elemhandle, pvname))
                if pvunit: 
                    self._field[fieldname].pvunit = pvunit
                _logger.debug("'%s' field '%s'[%s] = '%s'" % (
                        elemhandle, fieldname, idx, pvname))
                if properties.has_key("epsilon"):
                    self.setEpsilon(fieldname, properties["epsilon"])

        # check element field
        #for t in tags:
        #    g = re.match(r'aphla.elemfield.([\w\d]+)(\[\d+\])?', t)
        #    if g is None: continue
        #
        #    fieldname, idx = g.group(1), g.group(2)
        #    if idx is not None: 
        #        idx = int(idx[1:-1])
        #        _logger.info("%s %s[%d]" % (pvname, fieldname, idx))
                        
        # update the (pv, tags) dictionary
        if pvname in self._pvtags.keys(): 
            self._pvtags[pvname].update(tags)
        else: 
            self._pvtags[pvname] = set(tags)

    def setGetAction(self, v, field, idx = None, desc = ''):
        """Set the action when reading *field*.
    
        The previous action will be replaced if it was defined.
        *v* is single PV or a list/tuple
        """
        if not self._field.has_key(field):
            # TODO later how to set channel access
            # should not handle in this library
            self._field[field] = CaAction(trace=self.trace)
     
        self._field[field].setReadbackPv(v, idx)
    
    def setPutAction(self, v, field, idx=None, desc = ''):
        """Set the action for writing *field*.
    
        The previous action will be replaced if it was define.
        *v* is a single PV or a list/tuple
        """
        if not self._field.has_key(field):
            # TODO later how to set channel access
            self._field[field] = CaAction(trace=self.trace)
     
        self._field[field].setSetpointPv(v, idx)
        
    def fields(self):
        """Return element's fields, not sorted."""
        return self._field.keys()

    def stepSize(self, field):
        """Return the stepsize of field (hardware unit)"""
        return self._field[field].stepSize()

    def updateBoundary(self, field=None, lowhi=None, r=None):
        """Update the boundary for field.
        
        Parameters
        ----------
        field :
        lowhi : tuple
            Low(low) and high(hi) boundary. e.g. (0, 1) 
        r : int
            Divide the range (hi-low) by r to get the stepsize.

        Examples
        --------
        >>> updateBoundary('b1', (0, 2), 10) 

        The above example sets 'b1' range to (0, 2) and stepsize 0.2

        If this field has been set once, its boundary has been updated at the
        first time putting a value to it. Since putting a value needs to know
        the boundary and check if the value is inside.
        """
        if field is None: 
            fields = self._field.keys()
        else: 
            fields = [field]

        kw = {}
        if lowhi is not None: 
            kw['low'] = lowhi[0]
            kw['high'] = lowhi[1]

        if r is not None: kw['r'] = r
        for fld in fields:
            self._field[fld].setBoundary(**kw)

    def boundary(self, field=None):
        """Return the (low, high) range of *field* or all fields (raw unit)"""
        if field is not None:
            return self._field[field].boundary()
        else:
            return dict([(fld, act.boundary()) 
                         for fld,act in self._field.iteritems()])

    def __dir__(self):
        return dir(CaElement) + list(self.__dict__) + self._field.keys()

    def __repr__(self):
        if self.virtual:
            return "%s [%s] (virtual)" % (self.name, self.family)
        else:
            return AbstractElement.__repr__(self)

    def enableTrace(self, fieldname):
        if not self._field[fieldname].trace:
            self._field[fieldname].trace = True
            self._field[fieldname].sp = []
            self._field[fieldname].mark('setpoint')

    def disableTrace(self, fieldname):
        if self._field[fieldname].trace:        
            self._field[fieldname].trace = False
            self._field[fieldname].sp = []

    def disableField(self, fieldname):
        self._field[fieldname].opflags |= _DISABLED

    def enableField(self, fieldname):
        self._field[fieldname].opflags &= ~_DISABLED

    def setFieldReadonly(self, fieldname):
        self._field[fieldname].opflags |= _READONLY

    def resetFieldReadonly(self, fieldname):
        self._field[fieldname].opflags &= ~_READONLY
 
    def revert(self, fieldname):
        """undo the field value to its previous one"""
        self._field[fieldname].revert()
        for e in self.alias: e._field[fieldname].revert()

    def mark(self, fieldname, handle = 'setpoint'):
        self._field[fieldname].mark(handle)
        for e in self.alias: e._field[fieldname].mark(handle)

    def reset(self, fieldname, data='golden'):
        """data='golden' or 'origin'. see CaAction::reset()"""
        self._field[fieldname].reset(data)
        for e in self.alias: e._field[fieldname].reset(data)

    def get(self, fields, handle='readback', unitsys='phy'):
        """Get the values for given fields. None if not exists.

        Parameters
        ----------
        fields : str, list
            field.
        handle : str
            'readback', 'setpoint' or 'golden'.
        unitsys : the unit system
            None for lower level unit.

        Examples
        --------
        >>> get('x')
        >>> get(['x', 'y'])
        >>> get(['x', 'unknown'])
        [ 0, None]
        """
        kw = {'handle': handle, 'unitsys': unitsys}
        if isinstance(fields, (str, unicode)):
            return self._get_field(fields, **kw)
        else:
            # a list of fields
            return [ self._get_field(v, **kw) for v in fields]

    def _put_field(self, field, val, unitsys, **kwargs):
        """Set *val* to *field*. handle='golden' will set value as golden.

        See Also
        --------
        :func:`pv(field=field)`
        """
        att = field
        if not self.__dict__['_field'].has_key(att):
            raise RuntimeError("field '%s' is not defined for '%s'" % (
                    att, self.name))

        decr = self.__dict__['_field'][att]
        if not decr:
            raise AttributeError("field '%s' is not defined for '%s'" % (
                    att, self.name))
        if not decr.pvsp:
            raise ValueError("field '%s' in '%s' is not writable" % (
                        att, self.name))

        bc = kwargs.get('bc', 'exception')
        wait = kwargs.get("wait", True)
        timeout = kwargs.get("timeout", 5)
        decr.putSetpoint(val, unitsys, bc=bc, wait=wait, timeout=timeout)

    def put(self, field, val, **kwargs):
        """Set *val* to *field*.

        Parameters
        ----------
        field : str
            Element field
        val : float, int
            The new value.

        Keyword Arguments
        -----------------
        unitsys : str
            Unit system.
        bc : str
            Bounds checking: "exception" will raise a ValueError. 
            "ignore" will abort the whole setting. "boundary" will use the 
            boundary value it is crossing.
        wait : 
            The same as in caput
        timeout : 
        
        See Also
        --------
        :func:`pv(field=field)`
        """
        unitsys = kwargs.get("unitsys", 'phy')
        bc = kwargs.get("bc", 'exception')
        wait = kwargs.get("wait", True)
        trig = kwargs.get("trig", None)
        timeout = kwargs.get("timeout", 5)

        self._put_field(field, val, timeout=timeout, unitsys=unitsys, bc=bc, wait=wait)
        for e in self.alias:
            e._put_field(field, val, timeout=timeout, unitsys=unitsys, bc=bc, wait=wait)

        trig_fld = field + "_trig"
        if trig_fld in self.fields() and trig is not None:
            self._put_field(field + "_trig", trig,
                            unitsys=None, timeout=timeout, wait=True)
 
    def settable(self, field):
        """check if the field can be changed. not disabled, nor readonly."""
        if field not in self._field.keys(): return False
        if self._field[field].opflags & _DISABLED: return False
        if self._field[field].opflags & _READONLY: return False

        return self._field[field].settable()

    def readable(self, field):
        """check if the field readable (not disabled)."""
        if field not in self._field.keys(): return False
        if self._field[field].opflags & _DISABLED: return False
        return True


def merge(elems, field=None, **kwargs):
    """Merge the fields for all elements in a list return it as a single
    element. 

    Parameters
    ----------
    elems : list
        a list of element object
    kwargs: dict
        other properties of the new element.

    Examples
    --------
    >>> bpm = getElements('BPM') 
    >>> vpar = { 'virtual': 1, 'name': 'VBPM' }
    >>> vbpm = merge(bpm, **vpar)

    Note
    ----
    It does not merge the unit conversion. All raw unit.

    See Also
    --------
    :class:`CaElement`
    """

    # count 'field' owners and its rb,wb PVs.
    count, pvdict = {}, {}
    for e in elems:
        fds = e.fields()
        for f in fds: 
            if f in count: count[f] += 1
            else: count[f] = 1
            pvrb = e.pv(field=f, handle='readback')
            pvsp = e.pv(field=f, handle='setpoint')
            if f not in pvdict: pvdict[f] = [[], []]
            #print f, pvrb, pvsp
            pvdict[f][0].extend(pvrb)
            pvdict[f][1].extend(pvsp)

    elem = CaElement(**kwargs)
    #print "merged:", elem
    # consider only the common fields
    if field is None: 
        for k,v in count.iteritems(): 
            if v < len(elems): 
                _logger.warn("field '%s' has %d < %d" % (k, v, len(elems)))
                pvdict.pop(k)
        #print pvdict.keys()
        for fld,pvs in pvdict.iteritems():
            if len(pvs[0]) > 0: 
                elem.setGetAction(pvs[0], fld, None, '')
            if len(pvs[1]) > 0: 
                elem.setPutAction(pvs[1], fld, None, '')
        elem.sb = [e.sb for e in elems]
        elem.se = [e.se for e in elems]
        elem._name = [e.name for e in elems]
    elif field in pvdict:
        pvrb, pvsp = pvdict[field][0], pvdict[field][1]
        if len(pvrb) > 0: 
            elem.setGetAction(pvrb, field, None, '')
        if len(pvsp) > 0: 
            elem.setPutAction(pvsp, field, None, '')
        # count the element who has the field
        elemgrp = [e for e in elems if field in e.fields()]
        elem.sb = [e.sb for e in elemgrp] 
        elem.se = [e.se for e in elemgrp]
        elem._name = [e.name for e in elemgrp]
        #print pvsp
    else:
        _logger.warn("no pv merged for {0}".format([
                    e.name for e in elems]))
    # if all raw units are the same, so are the merged element
    for fld in elem.fields():
        units = sorted([e.getUnit(fld, unitsys=None) for e in elems if fld in e.fields()])
        if units[0] == units[-1]:
            elem.setUnit(fld, units[0], unitsys=None)

    return elem
