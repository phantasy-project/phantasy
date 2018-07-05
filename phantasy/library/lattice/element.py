#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build elements with Channel Access support.
"""

import logging

try:
    basestring
except NameError:
    basestring = str

from epics import PV
from phantasy.library.misc import flatten
from phantasy.library.pv import PV_POLICIES
from phantasy.library.pv import unicorn_read
from phantasy.library.pv import unicorn_write


_LOGGER = logging.getLogger(__name__)

UNSPECIFIED = 0
ASCENDING = 1
DESCENDING = 2
RANDOM = 3

VALID_STATIC_KEYS = ('name', 'family', 'index', 'se', 'length', 'sb',
                     'phy_name', 'phy_type', 'machine')
VALID_CA_KEYS = ('field_eng', 'field_phy', 'handle', 'pv_policy')


class AbstractElement(object):
    """``AbstractElement`` contains most of the lattice properties,
    such as element name, length, location and family. It also keeps a list of
    groups which belongs to.

    ``AbstractElement`` does not support Channel Access.

    Keyword Arguments
    -----------------
    name : str
        Element name.
    family : str
        Element type.
    index : int
        Element index, default sort key, otherwise, ``sb`` is used as sort key.
    length : float
        Effective element length.
    sb : float
        Longitudinal position at the beginning point, unit: *m*.
    se : float
        Longitudinal position at the end point, unit: *m*.
    enable : True or False
        Element is enabled or not, ``True`` is controllable, default is True.
    """

    def __init__(self, **kws):
        self.name = kws.get('name', None)
        self.index = kws.get('index', None)
        self.family = kws.get('family', None)
        self.se = kws.get('se', None)
        self.sb = kws.get('sb', None)
        self.length = kws.get('length', None)
        self._active = kws.get('enable', True)
        self.group = kws.get('group', None)
        if self._family is not None:
            self._group.add(self._family)

    @property
    def group(self):
        """set: Groups element belongs to."""
        return self._group

    @group.setter
    def group(self, g):
        if g is None:
            self._group = set()
        elif isinstance(g, (list, tuple, set)):
            self._group = set(g)
        else:
            _LOGGER.warning("'group': Input should be a set.")

    @property
    def name(self):
        """str: Element name, None if not given."""
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            self._name = None
        elif isinstance(name, basestring):
            self._name = name
        else:
            _LOGGER.warning("'name': Input should be a string.")

    @property
    def index(self):
        """int: Element index, ``-1`` if not given."""
        return self._index

    @index.setter
    def index(self, i):
        if i is None:
            self._index = -1
        elif isinstance(i, int):
            self._index = i
        elif isinstance(i, basestring):
            try:
                self._index = int(i)
            except ValueError:
                _LOGGER.error("'index': Invalid string to integer.")
        else:
            _LOGGER.warning("'index': Input should be an integer.")

    @property
    def family(self):
        """str: Element family, i.e. device type, None if not given."""
        return self._family

    @family.setter
    def family(self, t):
        if t is None:
            self._family = None
        elif isinstance(t, basestring):
            self._family = t
        else:
            _LOGGER.warning("'family': Input should be a string.")

    @property
    def length(self):
        """float: Element length, *m*, 0.0 if not given."""
        return self._length

    @length.setter
    def length(self, x):
        if x is None:
            self._length = 0.0
        elif isinstance(x, (int, float)):
            self._length = float(x)
        elif isinstance(x, basestring):
            try:
                self._length = float(x)
            except ValueError:
                _LOGGER.error("'length': Invalid string to float.")
        else:
            _LOGGER.warning("'length': Input should be a float number.")

    @property
    def sb(self):
        """float: Longitudinal position at the beginning point, *m*."""
        return self._sb

    @sb.setter
    def sb(self, x):
        if x is None:
            self._sb = float('inf')
        elif isinstance(x, (int, float)):
            self._sb = float(x)
        elif isinstance(x, basestring):
            try:
                self._sb = float(x)
            except ValueError:
                _LOGGER.error("'sb': Invalid string to float.")
        else:
            _LOGGER.warning("'sb': Input should be a float number.")

    @property
    def se(self):
        """float: Longitudinal position at the end point, *m*."""
        return self._se

    @se.setter
    def se(self, x):
        if x is None:
            self._se = float('inf')
        elif isinstance(x, (int, float)):
            self._se = float(x)
        elif isinstance(x, basestring):
            try:
                self._se = float(x)
            except ValueError:
                _LOGGER.error("'se': Invalid string to float.")
        else:
            _LOGGER.warning("'se': Input should be a float number.")

    @property
    def active(self):
        """Bool: Element is controllable or not, ``True`` by default."""
        return self._active

    @active.setter
    def active(self, b):
        new_flag = bool(b)
        if self._active != new_flag:
            self._active = new_flag
        else:
            _LOGGER.warning("Active status: {} is not changed.".format(new_flag))

    ##
    # def profile(self, vscale=1.0):
    #     """the profile for drawing the lattice.
    #
    #     The return is a tuple of (x, y, color) where (*x*, *y) are coordinates
    #     and *color* is one of the ['k', 'r', 'b'] depending its family.
    #
    #     It recognize the following *family*:
    #
    #     - 'QUAD', quadrupole, box height *vscale*, no negative
    #     - 'BEND', dipole. box height vscale both positive and negative.
    #     - 'SEXT', sextupole. box height 1.4*vscale
    #     - 'SOL', solenoid, box height 0.8*vscale
    #     - 'CAV', RF cavity,  box height 1.8*vscale
    #     - ['HCOR' | 'VCOR' | 'TRIMX' | 'TRIMY' | 'DCH' | 'DCV'], corrector, thin line
    #     - ['BPM' | 'BPMX' | 'BPMY' | 'PM'], beam position monitor, profile monitor, thin line
    #     - The rest unrecognized element, it returns a box with height
    #       0.2*vscale and color 'k'.
    #
    #     """
    #     b, e = self.sb, max(self.sb + self.length, self.se)
    #     h = vscale
    #     if self.family == 'CAV':
    #         return [b, b, e, e], [0, 1.8 * h, 1.8 * h, 0], 'k'
    #     elif self.family == 'SOL':
    #         return [b, b, e, e], [0, 0.8 * h, 0.8 * h, 0], 'k'
    #     elif self.family == 'QUAD':
    #         return [b, b, e, e], [0, h, h, 0], 'k'
    #     elif self.family == 'BEND':
    #         return [b, b, e, e, b, b, e, e], [0, h, h, -h, -h, h, h, 0], 'k'
    #     elif self.family == 'SEXT':
    #         return [b, b, e, e], [0, 1.4 * h, 1.4 * h, 0], 'k'
    #     elif self.family in ['HCOR', 'VCOR', 'TRIMX', 'TRIMY', 'DCH', 'DCV']:
    #         return [b, (b + e) / 2.0, (b + e) / 2.0, (b + e) / 2.0, e], \
    #                [0, 0, h, 0, 0], 'r'
    #     elif self.family in ['BPM', 'BPMX', 'BPMY', 'PM']:
    #         return [b, (b + e) / 2.0, (b + e) / 2.0, (b + e) / 2.0, e], \
    #                [0, 0, h, 0, 0], 'b'
    #     else:
    #         return [b, b, e, e], [0, 0.2 * h, 0.2 * h, 0], 'k'

    def __str__(self):
        return "{0:04d} | {1:<20s} {2:<8s} {3:^6.2f} [m] {4:^6.6f} [m]".format(
            int(self.index), self.name, self.family,
            float(self.sb), float(self.length)
        )

    def __repr__(self):
        return "%s [%s] @ sb=%f" % (self.name, self.family, self.sb)

    def __lt__(self, other):
        """use *index* if not None, otherwise use *sb*"""
        if self.index != other.index:
            return self.index < other.index
        elif self.sb != other.sb:
            return self.sb < other.sb
        else:
            _LOGGER.warning('{} and {} may be the same one'.format(self, other))

    def __eq__(self, other):
        """compares location, length and name"""
        return self.sb == other.sb and \
               self.length == other.length and \
               self.index == other.index and \
               self.name == other.name

    def __hash__(self,):
        return hash((self.name, self.index, self.length, self.sb))

    def _update_static_props(self, props):
        """Non-CA"""
        for k, v in props.items():
            if not hasattr(self, k) or getattr(self, k) != v:
                setattr(self, k, v)
            else:
                _LOGGER.debug("{0} already has {1} of {2}.".format(
                    self.name, k, getattr(self, k)))

    def update_properties(self, props, **kws):
        raise NotImplementedError("Not implemented.")


class CaField(object):
    """Channel Access support for element field.

    Usually, ``CaField`` instance has at most three types of PV names:
    *readback*, *readset* and *setpoint*, each PV should linked with valid
    PV connections.

    There are two approaches to retrieve the PV values, one is through
    ``value`` attribute, another one is by explicitly calling ``get()``;

    The same rule applies to set values, i.e. by setting ``value`` attribute
    and by calling ``put()`` method.

    Parameters
    ----------
    name : str
        Name of CA field, usually represents the physics attribute linked with CA.
    wait : bool
        If True, wait until put operation completed, default is True.
    timeout: float
        Time out in second for put operation, default is 10 seconds.
    ename : str
        Name of element which the field attaches to.

    Keyword Arguments
    -----------------
    readback : str, list(str)
        Readback PV name(s), if a single string is defined, append operation
        will be issued, if list or tuple of strings is defined, *readback*
        attribute will be overwritten with the new list, the same rule applies
        to *readset* and *setpoint*, as well as *readback_pv*, *readset_pv* and
        *setpoint_pv*.
    readset : str, list(str)
        Readset PV name(s).
    setpoint : str, list(str)
        Setpoint PV name(s).

    ### IMPLEMENTED IN HIGH-LEVEL LATTICE RIGHT NOW
    ### THIS WAY KEEP MULTIPLE SETTINGS FOR DIFFERENT LATTICES.
    ###
    If *trace* is True, every readback/setpoint will be recorded for later
    reset/revert whenever the get/put functions are called. Extra history
    point can be recorded by calling *mark*.
    ###
    """

    def __init__(self, name='', **kws):
        self.name = name
        self.ename = kws.get('ename', None)
        self.timeout = kws.get('timeout', None)
        self.wait = kws.get('wait', None)
        self._rdbk_pv_name = []
        self._rset_pv_name = []
        self._cset_pv_name = []
        self.readback = kws.get('readback', None)
        self.readset = kws.get('readset', None)
        self.setpoint = kws.get('setpoint', None)
        self._rdbk_pv = []
        self._rset_pv = []
        self._cset_pv = []
        self.init_pvs()
        pv_policy = kws.get('pv_policy', PV_POLICIES['DEFAULT'])
        self._default_read_policy = pv_policy['read']
        self._default_write_policy = pv_policy['write']
        self.read_policy = self._default_read_policy
        self.write_policy = self._default_write_policy
        self.ftype = kws.get('ftype', 'ENG')

        #################################################################
        # self.golden = []  # some setpoint can saved as golden value
        # self.pvh = []  # step size
        # self.pvlim = []  # lower/upper limit
        #
        # # buffer the initial value and last setting/reading
        # self.rb = []  # bufferred readback value
        # self.sp = []  # bufferred setpoint value
        # self._sp1 = []  # the last bufferred sp value when sp dimension changes.
        # self.field = ''
        # self.desc = kws.get('desc', None)
        # self.order = ASCENDING
        # self.opflags = 0
        # self.trace = kws.get('trace', False)
        # self.trace_limit = 200
        # self.sprb_epsilon = 0

    @property
    def name(self):
        """str: Field name, empty string if not given."""
        return self._name

    @name.setter
    def name(self, s):
        if s is None:
            self._name = ''
        elif isinstance(s, basestring):
            self._name = s
        else:
            _LOGGER.warning("Field name should be a valid string.")

    @property
    def ename(self):
        """str: Name of element the field attaches to."""
        return self._ename

    @ename.setter
    def ename(self, e):
        if e is None:
            self._ename = ''
        elif isinstance(e, basestring):
            self._ename = e
        else:
            _LOGGER.warning("Element name should be a valid string")

    @property
    def wait(self):
        """boolean: Wait (True) for not (False) when issuing set command,
        default: True."""
        return self._wait

    @wait.setter
    def wait(self, b):
        if b is None:
            self._wait = True
        else:
            self._wait = bool(b)

    @property
    def timeout(self):
        """float: Time out in second for put operation, default: 10 [sec]."""
        return self._timeout

    @timeout.setter
    def timeout(self, x):
        if x is None:
            self._timeout = 10
        else:
            self._timeout = float(x)

    @property
    def readback(self):
        """list[str]: Readback PV name, usually ends with *_RD*."""
        return self._rdbk_pv_name

    @readback.setter
    def readback(self, s):
        """if s is string, append will be issued, or override will be issued, the
        same policy for setpoint and readset."""
        if isinstance(s, basestring):
            if s not in self._rdbk_pv_name:
                self._rdbk_pv_name.append(s)
            else:
                _LOGGER.debug("Readback PV aleady exists.")
        elif isinstance(s, (list, tuple)):
            self._rdbk_pv_name = list(s)
        elif s is None:
            _LOGGER.debug("Readback PV not update.")
        else:
            _LOGGER.warning("Readback PV name should a valid string or list of string.")

    @property
    def readset(self):
        """list[str]: Readset PV name, usually ends with *_RSET*."""
        return self._rset_pv_name

    @readset.setter
    def readset(self, s):
        if isinstance(s, basestring):
            if s not in self._rset_pv_name:
                self._rset_pv_name.append(s)
            else:
                _LOGGER.debug("Readset PV aleady exists.")
        elif isinstance(s, (list, tuple)):
            self._rset_pv_name = list(s)
        elif s is None:
            _LOGGER.debug("Readset PV not update.")
        else:
            _LOGGER.warning("Readset PV name should a valid string or list of string.")

    @property
    def setpoint(self):
        """list[str]: Setpoint PV name, usually ends with *_CSET*."""
        return self._cset_pv_name

    @setpoint.setter
    def setpoint(self, s):
        if isinstance(s, basestring):
            if s not in self._cset_pv_name:
                self._cset_pv_name.append(s)
            else:
                _LOGGER.debug("Setpoint PV aleady exists.")
        elif isinstance(s, (list, tuple)):
            self._cset_pv_name = list(s)
        elif s is None:
            _LOGGER.debug("Setpoint PV not update.")
        else:
            _LOGGER.warning("Setpoint PV name should a valid string or list of string.")

    @property
    def readback_pv(self):
        """PV: Readback PV object."""
        return self._rdbk_pv

    @readback_pv.setter
    def readback_pv(self, pvobj):
        if isinstance(pvobj, PV):
            if pvobj not in self._rdbk_pv:
                self._rdbk_pv.append(pvobj)
            else:
                _LOGGER.debug("Readback PV object already exists.")
        elif isinstance(pvobj, (list, tuple)):
            self._rdbk_pv = list(pvobj)
        else:
            _LOGGER.warning("Input PV should be (list of) PV object.")

    @property
    def readset_pv(self):
        """PV: Readset PV object."""
        return self._rset_pv

    @readset_pv.setter
    def readset_pv(self, pvobj):
        if isinstance(pvobj, PV):
            if pvobj not in self._rset_pv:
                self._rset_pv.append(pvobj)
            else:
                _LOGGER.debug("Readset PV object already exists.")
        elif isinstance(pvobj, (list, tuple)):
            self._rset_pv = list(pvobj)
        else:
            _LOGGER.warning("Input PV should be (list of) PV object.")

    @property
    def setpoint_pv(self):
        """PV: Setpoint PV object."""
        return self._cset_pv

    @setpoint_pv.setter
    def setpoint_pv(self, pvobj):
        if isinstance(pvobj, PV):
            if pvobj not in self._cset_pv:
                self._cset_pv.append(pvobj)
            else:
                _LOGGER.debug("Setpoint PV object already exists.")
        elif isinstance(pvobj, (list, tuple)):
            self._cset_pv = list(pvobj)
        else:
            _LOGGER.warning("Input PV should be PV object.")

    def __eq__(self, other):
        return self.readback == other.readback and \
               self.setpoint == other.setpoint and \
               self.readset == other.readset and \
               self.name == other.name

    @property
    def write_policy(self):
        """Defined write policy, i.e. how to set value to field.

        The defined policy is a function, with *setpoint_pv* attribute and new
        value as arguments.
        """
        return self._write_policy

    @write_policy.setter
    def write_policy(self, f):
        if f is None:
            self._write_policy = self._default_write_policy
        else:
            self._write_policy = f

    @property
    def read_policy(self):
        """Defined read policy, i.e. how to read value from field.

        The defined policy is a function, with *readback_pv* attribute as argument,
        return a value.
        """
        return self._read_policy

    @read_policy.setter
    def read_policy(self, f):
        if f is None:
            self._read_policy = self._default_read_policy
        else:
            self._read_policy = f

    def reset_policy(self, policy=None):
        """Reset policy, by policy name."""
        if policy is None:
            self._reset_read_policy()
            self._reset_write_policy()
        elif policy == 'read':
            self._reset_read_policy()
        elif policy == 'write':
            self._reset_write_policy()
        else:
            _LOGGER.error("Invalid policy name, do not reset.")

    def _reset_read_policy(self):
        self._read_policy = self._default_read_policy

    def _reset_write_policy(self):
        self._write_policy = self._default_write_policy

    @property
    def value(self):
        """Get value of PV, returned from CA request."""
        return self.read_policy(self.readback_pv)

    @value.setter
    def value(self, v):
        self.write_policy(self.setpoint_pv, v, timeout=self.timeout,
                          wait=self.wait)

    def init_pvs(self, **kws):
        """PV initialization."""
        rdbk_pv_name, rset_pv_name, cset_pv_name = self._rdbk_pv_name, \
                                                   self._rset_pv_name, \
                                                   self._cset_pv_name
        self._init_rdbk_pv(rdbk_pv_name, **kws)
        self._init_rset_pv(rset_pv_name, **kws)
        self._init_cset_pv(cset_pv_name, **kws)

    def _init_rdbk_pv(self, pvs, **kws):
        if pvs:
            self.readback_pv = [PV(i) for i in pvs]

    def _init_rset_pv(self, pvs, **kws):
        if pvs:
            self.readset_pv = [PV(i) for i in pvs]

    def _init_cset_pv(self, pvs, **kws):
        if pvs:
            self.setpoint_pv = [PV(i) for i in pvs]

    def update(self, **kws):
        """Update PV with defined handle."""
        for k in ('readback', 'readset', 'setpoint'):
            v = kws.get(k)
            if v is not None:
                setattr(self, k, v)
                setattr(self, "{}_pv".format(k), PV(v))

    def pvs(self):
        """Return dict of valid pv type and names."""
        pv_types = ('readback', 'readset', 'setpoint')
        pv_names = (self.readback, self.readset, self.setpoint)
        pv_dict = dict(zip(pv_types, pv_names))
        return {k: v for k, v in pv_dict.items() if v is not None}

    def get(self, handle, **kws):
        """Get value of PV with specified *handle*.

        Parameters
        ----------
        handle : str
            PV handle, 'readback', 'readset' or 'setpoint'.

        Returns
        -------
        r : list
            List of readings for specified handle.

        Examples
        --------
        Get CA field instance from element:

        >>> from phantasy import MachinePortal
        >>> mp = MachinePortal(machine='<mach_name>')
        >>> lat = mp.work_lattice_conf
        >>> elem = lat[0]
        >>> print(elem.fields)
        >>> fld = elem.get_field('<field_name>')

        Get readings from PVs with 'readback' handle

        >>> print(fld.get('readback'))

        Get readings from PVs with 'setpoint' handle

        >>> print(fld.get('setpoint'))

        Get readings from PVs with 'readset' handle

        >>> print(fld.get('readset'))
        """
        if handle == 'readback':
            pv = self._rdbk_pv
        elif handle == 'readset':
            pv = self._rset_pv
        elif handle == 'setpoint':
            pv = self._cset_pv
        if pv is not None:
            return [ipv.get(**kws) for ipv in pv]
        else:
            return None

    def set(self, value, handle, **kws):
        """Set value(s) of PV(s) with specified *handle*.

        Parameters
        ----------
        value : list or list(val)
            New value(s) to be set.
        handle : str
            PV handle, 'readback', 'readset' or 'setpoint'.

        Examples
        --------
        Get CA field instance, see `get()`, set one field of an element
        which has two 'setpoint' PVs, e.g. quad:

        >>> fld.set([val1, val2], 'setpoint')
        >>> # Check with get:
        >>> fld.get('setpoint')
        >>> # should return [val1, val2]

        Note
        ----
        ``get()`` and ``set()`` are a pair of methods that can read/write PV(s)
        bypass field defined read/write policies.
        """
        if handle == 'readback':
            pv = self._rdbk_pv
        elif handle == 'readset':
            pv = self._rset_pv
        elif handle == 'setpoint':
            pv = self._cset_pv
        if not isinstance(value, (list, tuple)):
            value = value,
        if pv is not None:
            for (k, v) in zip(pv, value):
                k.put(v, **kws)
        else:
            pass

    def is_physics_field(self):
        """Test if *field* is physics field.
        """
        return self.ftype == 'PHY'

    def is_engineering_field(self):
        """Test if *field* is engineering field.
        """
        return self.ftype == 'ENG'

    def __repr__(self):
        return "[{}] Field '{}' of '{}'".format(self.ftype, self.name, self.ename)

        ################################################################################

        # def _insert_in_order(self, lst, v):
        #     """
        #     insert `v` to an ordered list `lst`
        #     """
        #     if len(lst) == 0 or self.order == UNSPECIFIED:
        #         if isinstance(v, (tuple, list)):
        #             lst.extend(v)
        #         else:
        #             lst.append(v)
        #         return 0
        #
        #     if self.order == ASCENDING:
        #         for i, x in enumerate(lst):
        #             if x < v:
        #                 continue
        #             lst.insert(i, v)
        #             return i
        #     elif self.order == DESCENDING:
        #         for i, x in enumerate(lst):
        #             if x > v:
        #                 continue
        #             lst.insert(i, v)
        #             return i
        #
        #     lst.append(v)
        #     return len(lst) - 1
        #
        # def _all_within_range(self, v, lowhigh):
        #     """if lowhigh is not valid, returns true"""
        #     # did not check for string type
        #     if isinstance(v, basestring):
        #         return True
        #     if lowhigh is None:
        #         return True
        #
        #     low, high = lowhigh
        #     if isinstance(v, (float, int)):
        #         if low is None:
        #             return v <= high
        #         elif high is None:
        #             return v >= low
        #         elif high <= low:
        #             return True
        #         elif v > high or v < low:
        #             return False
        #         else:
        #             return True
        #     elif isinstance(v, (list, tuple)):
        #         for vi in v:
        #             if not self._all_within_range(vi, lowhigh):
        #                 return False
        #         return True
        #     else:
        #         raise RuntimeError("unknow data type '{0}:{1}'".format(v, type(v)))
        #
        # def setReadbackPv(self, pv, idx=None):
        #     """
        #     set/replace the PV for readback.
        #
        #     :param str pv: PV name
        #     :param int idx: index in the PV list
        #
        #     `idx` is needed if such readback has a list
        #     of PVs.  if idx is None, replace the original one. if idx is an index
        #     integer and pv is not a list, then replace the one with this index.
        #     """
        #     if idx is None:
        #         if isinstance(pv, basestring):
        #             self.pvrb = [pv]
        #         elif isinstance(pv, (tuple, list)):
        #             self.pvrb = [p for p in pv]
        #         while len(self.golden) < len(self.pvrb):
        #             self.golden.append(None)
        #     elif not isinstance(pv, (tuple, list)):
        #         while idx >= len(self.pvrb):
        #             self.pvrb.append(None)
        #         while idx >= len(self.golden):
        #             self.golden.append(None)
        #         self.pvrb[idx] = pv
        #     else:
        #         raise RuntimeError("invalid readback pv '%s' for position '%s'" %
        #                            (str(pv), str(idx)))
        #
        # def setSetpointPv(self, pv, idx=None, **kwargs):
        #     """
        #     set the PV for setpoint at position idx.
        #
        #     :param str pv: PV name
        #     :param int idx: index in the PV list.
        #
        #     if idx is None, replace the original one. if idx is an index integer
        #     and pv is not a list, then replace the one with this index.
        #
        #     seealso :func:`setStepSize`, :func:`setBoundary`
        #     """
        #     # lim = kwargs.get("boundary", None)
        #     # h = kwargs.get("step_size", None)
        #     if idx is None:
        #         if isinstance(pv, basestring):
        #             self.pvsp = [pv]
        #         elif isinstance(pv, (tuple, list)):
        #             self.pvsp = [p for p in pv]
        #         # lim_h = [self._get_sp_lim_h(pvi) for pvi in self.pvsp]
        #         # None means not checked yet. (None, None) checked but no limit
        #         self.pvlim = [None] * len(self.pvsp)
        #         self.pvh = [None] * len(self.pvsp)
        #         self.golden = [None] * len(self.pvsp)
        #     elif not isinstance(pv, (tuple, list)):
        #         while idx >= len(self.pvsp):
        #             self.pvsp.append(None)
        #             self.pvh.append(None)
        #             self.pvlim.append(None)
        #             self.golden.append(None)
        #         self.pvsp[idx] = pv
        #         self.pvlim[idx] = None
        #         self.pvh[idx] = None
        #         self.golden[idx] = None
        #     else:
        #         raise RuntimeError("invalid setpoint pv '%s' for position '%s'" %
        #                            (str(pv), str(idx)))
        #
        #     # roll the buffer.
        #     self._sp1 = self.sp
        #     self.sp = []


class CaElement(AbstractElement):
    """Element with Channel Access support.

    This class could be used to create an element with data from Channel Finder Service
    or input keyword parameters.

    Parameters
    ----------
    enable : True or False
        Element is enabled or not, ``True`` is controllable, default is True.

    Keyword Arguments
    -----------------
    name : str
        Element name.
    family : str
        Element type.
    index : int
        Element index, default sort key, otherwise, ``sb`` is used as sort key.
    length : float
        Effective element length.
    sb : float
        Longitudinal position at the beginning point, unit: *m*.
    se : float
        Longitudinal position at the end point, unit: *m*.
    virtual : bool
        pass
    tags : dict
        Tags for each PV as key name and set of strings as tag names.
    fields : dict
        pass
    enable : True or False
        Element is enabled or not, ``True`` is controllable, default is True.
    pv_data : list or dict
        PV record data to build an element, should be of a list of:
        ``string of PV name, dict of properties, list of tags``, or
        with dict of keys of: ``pv_name``, ``pv_props`` and ``pv_tags``.

    Note
    ----
    If *pv_data* is defined, element will be initialized with data from
    *pv_data*, if *pv_data* is CFS formatted, ``simplify_data`` should be used
    first to convert data structure.

    See Also
    --------
    :func:`~phantasy.library.misc.miscutils.simplify_data`
        Convert CFS formatted data into simple tuple.
    :class:`phantasy.library.pv.datasource.DataSource`
        PV data source.
    """

    def __init__(self, **kws):
        self.__dict__['_fields'] = dict()
        self.virtual = kws.get('virtual', None)
        self.tags = kws.get('tags', None)
        super(CaElement, self).__init__(**kws)

        self.last_settings = {}
        self.design_settings = {}

        pv_data = kws.get('pv_data', None)
        if pv_data is not None:
            if isinstance(pv_data, list):
                self.process_pv(*pv_data)
            elif isinstance(pv_data, dict):
                self.process_pv(**pv_data)


        ###
        # self._pvarchive = []
        # self.trace = kws.get('trace', False)
        # self.alias = []
        ###

    @property
    def last_settings(self):
        """dict: Last setting(s) for all dynamic field(s)."""
        return self._last_settings

    @last_settings.setter
    def last_settings(self, x):
        if x is None:
            self._last_settings = {}
        else:
            self._last_settings = x

    @property
    def design_settings(self):
        """dict: Physics design setting(s) for all dynamic field(s)."""
        return self._design_settings

    @design_settings.setter
    def design_settings(self, x):
        if x is None:
            self._design_settings = {}
        else:
            self._design_settings = x

    @property
    def tags(self):
        """dict: Tags that element PVs have been assigned."""
        return self._tags

    @tags.setter
    def tags(self, t):
        if t is None:
            self._tags = dict()
        elif isinstance(t, dict):
            self._tags = t
        else:
            _LOGGER.warning("'tags' should be a valid dict.")

    @property
    def virtual(self):
        """bool: Virtual element or not."""
        return self._virtual

    @virtual.setter
    def virtual(self, b):
        if b is None:
            self._virtual = False
        else:
            self._virtual = bool(b)

    @property
    def fields(self):
        """list: Valid Channel Access field names.

        Warnings
        --------
        *fields* can only accept dict, with CA field name as key and ``CaField`` as value.
        """
        return list(self._fields.keys())

    @fields.setter
    def fields(self, f):
        if f is None:
            self._fields = dict()
        elif isinstance(f, dict):
            self._fields = f
        else:
            _LOGGER.warning("'fields' should be a valid dict.")

    def get_phy_fields(self):
        """Return list of all physics fields.

        Note
        ----
        If returned list is empty, but `get_eng_fields` is not, then physics
        fields should be the same as engineering fields, but only appeared as
        ENG field type.
        """
        return [f for f in self.fields
                if self.get_field(f).is_physics_field()]

    def get_eng_fields(self):
        """Return list of all engineering fields.
        """
        return [f for f in self.fields
                if self.get_field(f).is_engineering_field()]

    def _update_ca_props(self, props, **kws):
        """CA"""
        def build_pv_policy_phy(u_policy, pv_policy):
            # pv_policy is a dict
            fn_p, fn_n = u_policy['p'], u_policy['n']
            f_read, f_write = pv_policy['read'], pv_policy['write']

            @unicorn_read(fn_p)
            def f_read_phy(x):
                return f_read(x)

            @unicorn_write(fn_n)
            def f_write_phy(x, v, **kws):
                f_write(x, v, **kws)
            return {'read': f_read_phy, 'write': f_write_phy}

        handle_name = props.get('handle', None)
        field_name = props.get('field_eng', None) # engineering field name
        # if field_phy is undefined, use the same as field_eng
        field_name_phy = props.get('field_phy', None)
        pv_policy_str = props.get('pv_policy', 'DEFAULT')
        pv_policy = PV_POLICIES.get(pv_policy_str)
        # pv_policy passed as string, which is defined in channels datafile,
        # while pv_policy passed to CaField is a dict: {'read': rp, 'write': wp}
        u_policy = kws.get('u_policy')
        if u_policy is not None:
            pv_policy_phy = build_pv_policy_phy(u_policy, pv_policy)
            # Set u_policy as element attributes
            self._unicorn_e2p = u_policy['p']
            self._unicorn_p2e = u_policy['n']
        else:
            pv_policy_phy = PV_POLICIES.get(pv_policy_str)
            self._unicorn_e2p = lambda x:x
            self._unicorn_p2e = lambda x:x
        pv = kws.get('pv', None)
        #
        if field_name is not None:
            self.set_field(field_name, pv, handle_name, ftype='ENG',
                           pv_policy=pv_policy)
        if field_name_phy is not None:
            self.set_field(field_name_phy, pv, handle_name, ftype='PHY',
                           pv_policy=pv_policy_phy)

    def set_field(self, field, pv, handle=None, **kws):
        """Set element field with CA support.

        Parameters
        ----------
        field : str
            Field name.
        pv : str
            Valid PV name.
        handle : str
            PV channel type, valid options: ``readback``, ``readset``,
            ``setpoint``, default is ``readback``.

        Keyword Arguments
        -----------------
        pv_policy : dict
            Name of PV read/write policy, keys: 'read' and 'write', values:
            scaling law function object.
        ftype : str
            Field type, 'ENG' (default) or 'PHY'.
        """
        if handle is None:
            handle = 'readback'
        if field not in self._fields:
            new_field = CaField(name=field,
                                ename=self.name,
                                ftype=kws.get('ftype'),
                                pv_policy=kws.get('pv_policy'),
                                **{handle: pv})
            self._design_settings.update({field: None})
            self._last_settings.update({field: None})
            self._fields[field] = new_field
        else:
            self._fields[field].update(**{handle: pv})

        _LOGGER.debug("Process '{0}' PV: {1}.".format(handle, pv))


    def update_properties(self, props, **kws):
        """Update element properties.

        Parameters
        ----------
        props : dict
            Dictionary of properties, two categories:

            - static properties: without CA features:
              *name*, *family*, *index*, *se*, *sb* (optional), *length*
            - dynamic properties: with CA features:
              *handle*, *field*

        Keyword Arguments
        -----------------
        pv : str
            Valid PV name.
        """
        prop_st = {k: v for k, v in props.items() if k in VALID_STATIC_KEYS}
        prop_ca = {k: v for k, v in props.items() if k in VALID_CA_KEYS}
        self._update_static_props(prop_st)
        self._update_ca_props(prop_ca, **kws)

    def update_tags(self, tags, **kws):
        """Update element tags.

        Parameters
        ----------
        tags : list
            List of tags.

        Keyword Arguments
        -----------------
        pv : str
            Valid PV name.
        """
        pv_name = kws.get('pv', None)
        if pv_name is None:
            return None
        if pv_name in self._tags:
            self._tags[pv_name].update(tags)
        else:
            self._tags[pv_name] = set(tags)

    def process_pv(self, pv_name, pv_props, pv_tags=None, u_policy=None):
        """Process PV record to update element with properties and tags.

        Parameters
        ----------
        pv_name : str
            PV name.
        pv_props : dict
            PV properties, key-value pairs.
        pv_tags : list
            PV tag list.
        """
        if not isinstance(pv_name, basestring):
            raise TypeError("{} is not a valid type".format(type(pv_name)))

        # properties
        self.update_properties(pv_props, pv=pv_name, u_policy=u_policy)
        # tags
        self.update_tags(pv_tags, pv=pv_name)
        self.update_groups(pv_props, pv=pv_name)

    def update_groups(self, props, **kws):
        """Update new group with *family* name.

        Parameters
        ----------
        props : dict
            Element properties.

        See Also
        --------
        update_properties
        """
        new_groups = props.get('group', None)
        if new_groups is not None:
            if isinstance(new_groups, basestring):
                new_groups = new_groups,
            [self._group.add(g) for g in new_groups]
        if self._family is not None:
            self._group.add(self._family)

    def get_field(self, field):
        """Get element field of CA support.

        Parameters
        ----------
        field : str
            Field name.

        Note
        ----
        All valid field names could be retrieved by ``fields`` attribute.

        Returns
        -------
        ret :
            CaField or None.
        """
        if field in self._fields:
            return self._fields[field]
        else:
            print("INVALID field, could be one of ({}).".format(
                ', '.join(sorted(self.fields))))
            return None

    def __getattr__(self, key):
        if key in self._fields:
            return self._fields[key].value
        else:
            raise AttributeError(
                "element {} does not have field {}.".format(self.name, key)
            )

    def __setattr__(self, key, value):
        if key in self._fields:
            self._fields[key].value = value
            if self._fields[key].wait:
                _LOGGER.warning(
                    "Field '{f_name}' of '{e_name}' reached: {rd_val}.".format(
                        f_name=key, e_name=self.name, rd_val=getattr(self, key)
                    )
                )
            self._last_settings.update([(key, value)])
        else:
            super(CaElement, self).__setattr__(key, value)

    def __dir__(self):
        return dir(CaElement) + self._fields.keys() + self.__dict__.keys()

    def __repr__(self):
        if self.virtual:
            return "%s [%s] (virtual)" % (self.name, self.family)
        else:
            return super(CaElement, self).__repr__()

    def pv(self, field=None, handle=None, **kws):
        """Get PV names with defined *field* and *handle*, if none of them is defined,
        return all PV names.

        Parameters
        ----------
        field : str or list
            Channel access field name, all available fields will be used
            if not defined, ignore invalid field.
        handle : str
            Channel access protocol type, could be one of *readback*, *readset*
            and *setpoint*.

        Note
        ----
        1. All Valid field names could be retrieved by ``fields`` attribute.
        2. If more than one field is defined with *field*, i.e. *field* is a list
           of string, return PV names binding with these fields, may apply *handle*
           as a filter, e.g. if *handle* is not defined, return all PVs.

        Returns
        -------
        ret : list
            List of valid PVs as request.
        """
        pvs = list()
        if field is None and handle is None:
            for _, v in self._fields.items():
                pvs.extend(v.pvs().values())
        else:
            f_pv = list()
            if field is None:
                field = self.fields
            elif isinstance(field, basestring):
                field = field,

            for f in [k for k in field if k in self.fields]:
                f_pv.append(self._fields.get(f).pvs())

            for pv_i in f_pv:
                if handle is None:
                    pvs.extend([v for k, v in pv_i.items() if v is not None])
                elif handle in ['readback', 'setpoint', 'readset']:
                    pvs.extend([v for k, v in pv_i.items() if v is not None and k == handle])
                else:
                    print("Invalid handle, valid options: " +
                          "'readback', 'readset', 'setpoint'.")
                    break
        return flatten(pvs)

    #     def _pv_1(self, **kwargs):
    #         """Find the pv when len(kwargs)==1.
    #
    #         - tag:
    #         - tags: all tags are met
    #         - field: return pvrb + pvsp
    #         """
    #         if kwargs.get('tag', None):
    #             return self._pv_tags([kwargs['tag']])
    #         elif kwargs.get('tags', None):
    #             return self._pv_tags(kwargs['tags'])
    #         elif kwargs.get('field', None):
    #             att = kwargs['field']
    #             if att in self._field:
    #                 decr = self._field[att]
    #                 return decr.pvrb + decr.pvsp
    #             else:
    #                 return []
    #         elif kwargs.get('handle', None):
    #             pvl = []
    #             if kwargs["handle"] == "setpoint":
    #                 for _, act in self._field.items():
    #                     pvl.extend(act.pvsp)
    #             elif kwargs["handle"] == "readback":
    #                 for _, act in self._field.items():
    #                     pvl.extend(act.pvrb)
    #             return pvl
    #         return []
    #
    #     def _pv_tags(self, tags):
    #         """
    #         return pv list which has all the *tags*.
    #         """
    #         tagset = set(tags)
    #         return [pv for pv, ts in self._pvtags.items()
    #                 if tagset.issubset(ts) and ts]
    #
    #     def _pv_fields(self, fields):
    #         """
    #         return pv list which has all fields in the input
    #         """
    #         fieldset = set(fields)
    #         ret = []
    #         for k, v in self._field.items():
    #             # print k, v
    #             if k in fieldset:
    #                 ret.extend(v['eget'])
    #                 ret.extend(v['eput'])
    #         return ret
    #
    #     def pv(self, **kwargs):
    #         """Search for PV names with specified *tag*, *tags*, *field*, *handle* or a
    #         combinatinon of *field* and *handle*.
    #
    #         Returns
    #         -------
    #         ret : list
    #             List of PV names.
    #
    #         Examples
    #         --------
    #         >>> pv() # returns all pvs.
    #         >>> pv(tag='phyutil.sys.LS1')
    #         >>> pv(tag='aphla.X')
    #         >>> pv(tags=['aphla.EGET', 'aphla.Y'])
    #         >>> pv(field = "x")
    #         >>> pv(field="x", handle='readback')
    #
    #         See Also
    #         --------
    #         :class:`CaAction`
    #         """
    #         if len(kwargs) == 0:
    #             return self._pvtags.keys()
    #         elif len(kwargs) == 1:
    #             return self._pv_1(**kwargs)
    #         elif len(kwargs) == 2:
    #             handle = kwargs.get('handle', None)
    #             fd = kwargs.get('field', None)
    #             if fd not in self._field:
    #                 return []
    #             if handle == 'readback':
    #                 return self._field[kwargs['field']].pvrb
    #             elif handle == 'setpoint':
    #                 return self._field[kwargs['field']].pvsp
    #             else:
    #                 return []
    #         else:
    #             return []
    #
    #     def hasPv(self, pv, inalias=False):
    #         """Check if this element has pv.
    #
    #         inalias=True will also check its alias elements.
    #
    #         If the alias (child) has its aliases (grand children), they are not
    #         checked. (no infinite loop)
    #         """
    #         if pv in self._pvtags:
    #             return True
    #         if inalias is True:
    #             for e in self.alias:
    #                 # if e.hasPv(pv): return True
    #                 if pv in e._pvtags:
    #                     return True
    #         return False
    #
    #     def addAliasField(self, newfld, fld):
    #         self._field[newfld] = copy.deepcopy(self._field[fld])
    #
    #     def status(self):
    #         """String representation of value, golden setpoint, range for each
    #         field.
    #         """
    #         ret = self.name
    #         if not self._field.keys():
    #             return ret
    #
    #         maxlen = max([len(att) for att in self._field.keys()])
    #         head = '\n%%%ds: ' % (maxlen + 2)
    #         for att in self._field.keys():
    #             decr = self._field[att]
    #             if not decr:
    #                 continue
    #             val = decr.getReadback()
    #             val1 = decr.getGolden()
    #             val2 = decr.boundary()
    #             ret = ret + head % att + str(val) + " (%s) " % str(val1) + " [%s]" % str(val2)
    #         return ret
    #


    # #    def __setattr__(self, att, val):
    # #        # this could be called by AbstractElement.__init__ or Element.__init__
    # #        # Note: the quick way has wait=False
    # #        if hasattr(super(CaElement, self), att):
    # #            super(CaElement, self).__setattr__(att, val)
    # #        elif att in self._field:
    # #            decr = self._field[att]
    # #            if not decr:
    # #                raise AttributeError("field '%s' is not defined for '%s'" % (
    # #                    att, self.name))
    # #            if not decr.pvsp:
    # #                raise ValueError("field '%s' in '%s' is not writable" % (
    # #                    att, self.name))
    # #            decr.putSetpoint(val, wait=False)
    # #            # if _field_trig exists, trig it, do not wait
    # #            decr_trig = self._field.get(att + "_trig", None)
    # #            if decr_trig:
    # #                decr_trig.putSetpoint(1, wait=False)
    # #        elif att in self.__dict__.keys():
    # #            self.__dict__[att] = val
    # #        else:
    # #            # new attribute for superclass
    # #            super(CaElement, self).__setattr__(att, val)
    # #            # raise AttributeError("Error")
    # #        for e in self.alias:
    # #            e.__setattr__(att, val)
    #
    #     def _get_unitconv(self, field, handle):
    #         if field not in self._field:
    #             return {}
    #         if handle == "readback":
    #             return self._field[field].ucrb
    #         elif handle == "setpoint":
    #             return self._field[field].ucsp
    #         else:
    #             return {}
    #
    #     def convertible(self, field, src, dst, handle="readback"):
    #         """Check the unit conversion is possible or not.
    #
    #         Returns
    #         -------
    #         ret : True or False
    #             If no specified handle, returns False.
    #         """
    #         if field not in self._field:
    #             return False
    #
    #         if src is None and dst is None:
    #             return True
    #
    #         unitconv = self._get_unitconv(field, handle)
    #
    #         if (src, dst) in unitconv:
    #             return True
    #
    #         uc = unitconv.get((dst, src), None)
    #         if uc is not None and uc.invertible:
    #             return True
    #         return False
    #
    #     def addUnitConversion(self, field, uc, src, dst, handle=None):
    #         """Add unit conversion for field."""
    #         # src, dst is unit system name, e.g. None for raw, phy
    #         if handle is None or handle == "readback":
    #             self._field[field].ucrb[(src, dst)] = uc
    #             if src is None:
    #                 self._field[field].pvrbunit = uc.srcunit
    #             elif dst is None:
    #                 self._field[field].pvrbunit = uc.dstunit
    #         if handle is None or handle == "setpoint":
    #             self._field[field].ucsp[(src, dst)] = uc
    #             if src is None:
    #                 self._field[field].pvspunit = uc.srcunit
    #             elif dst is None:
    #                 self._field[field].pvspunit = uc.dstunit
    #
    #     def convertUnit(self, field, x, src, dst, handle="readback"):
    #         """Convert value x between units without setting hardware"""
    #         uc = self._get_unitconv(field, handle)
    #         return self._field[field]._unit_conv(x, src, dst, uc)
    #
    #     def get_unit_systems(self, field, handle="readback"):
    #         """Get a list of all unit systems for field.
    #
    #         None is the lower level unit, e.g. in EPICS channel. Use convertible
    #         to see if the conversion is possible between any two unit systems.
    #         """
    #         unitconv = self._get_unitconv(field, handle)
    #         if not unitconv:
    #             return [None]
    #
    #         src, dst = zip(*(unitconv.keys()))
    #
    #         ret = set(src).union(set(dst))
    #         return list(ret)
    #
    #     def getUnitSystems(self, field=None, handle="readback"):
    #         """Return a list of available unit systems for field.
    #
    #         If no field specified, return a dictionary for all fields and their
    #         unit systems.
    #
    #         None means the unit used in the lower level control system, e.g. EPICS.
    #         """
    #         if field is None:
    #             return dict([(f, self.get_unit_systems(f, handle)) for f \
    #                          in self._field.keys()])
    #         else:
    #             return self.get_unit_systems(field, handle)
    #
    #     def getUnit(self, field, unitsys='phy', handle="readback"):
    #         """Get the unit symbol of a unit system, e.g. unitsys='phy'
    #
    #         The unit name, e.g. "T/m" for integrated quadrupole strength, is
    #         helpful for plotting routines.
    #
    #         return '' if no such unit system. A tuple of all handles when *handle*
    #         is None
    #         """
    #         if field in self._field and unitsys is None:
    #             if handle == "readback":
    #                 return self._field[field].pvrbunit
    #             elif handle == "setpoint":
    #                 return self._field[field].pvspunit
    #             else:
    #                 return ""
    #
    #         unitconv = self._get_unitconv(field, handle)
    #         for k, v in unitconv.items():
    #             if k[0] == unitsys:
    #                 return v.srcunit
    #             elif k[1] == unitsys:
    #                 return v.dstunit
    #
    #         return ""
    #
    #     def setUnit(self, field, u, unitsys='phy', handle="readback"):
    #         """Set the unit symbol for a unit system.
    #         """
    #         if field not in self._field.keys():
    #             raise RuntimeError("element '%s' has no '%s' field" % \
    #                                self.name, field)
    #
    #         if unitsys is None:
    #             self._field[field].pvunit = u
    #
    #         for k, v in self._get_unitconv(field, handle).items():
    #             if k[0] == unitsys:
    #                 v.srcunit = u
    #             elif k[1] == unitsys:
    #                 v.dstunit = u
    #
    #     def getEpsilon(self, field):
    #         return self._field[field].sprb_epsilon
    #
    #     def setEpsilon(self, field, eps):
    #         self._field[field].sprb_epsilon = eps
    # def stepSize(self, field):
    #     """Return the stepsize of field (hardware unit)"""
    #     return self._field[field].stepSize()
    #
    # def updateBoundary(self, field=None, lowhi=None, r=None):
    #     """Update the boundary for field.
    #
    #     Parameters
    #     ----------
    #     field :
    #     lowhi : tuple
    #         Low(low) and high(hi) boundary. e.g. (0, 1)
    #     r : int
    #         Divide the range (hi-low) by r to get the stepsize.
    #
    #     Examples
    #     --------
    #     >>> updateBoundary('b1', (0, 2), 10)
    #
    #     The above example sets 'b1' range to (0, 2) and stepsize 0.2
    #
    #     If this field has been set once, its boundary has been updated at the
    #     first time putting a value to it. Since putting a value needs to know
    #     the boundary and check if the value is inside.
    #     """
    #     if field is None:
    #         fields = self._field.keys()
    #     else:
    #         fields = [field]
    #
    #     kw = {}
    #     if lowhi is not None:
    #         kw['low'] = lowhi[0]
    #         kw['high'] = lowhi[1]
    #
    #     if r is not None:
    #         kw['r'] = r
    #     for fld in fields:
    #         self._field[fld].setBoundary(**kw)
    #
    # def boundary(self, field=None):
    #     """Return the (low, high) range of *field* or all fields (raw unit)"""
    #     if field is not None:
    #         return self._field[field].boundary()
    #     else:
    #         return dict([(fld, act.boundary())
    #                      for fld, act in self._field.items()])
    #

    # def enableTrace(self, fieldname):
    #     if not self._field[fieldname].trace:
    #         self._field[fieldname].trace = True
    #         self._field[fieldname].sp = []
    #         self._field[fieldname].mark('setpoint')
    #
    # def disableTrace(self, fieldname):
    #     if self._field[fieldname].trace:
    #         self._field[fieldname].trace = False
    #         self._field[fieldname].sp = []
    #
    # def disableField(self, fieldname):
    #     self._field[fieldname].opflags |= _DISABLED
    #
    # def enableField(self, fieldname):
    #     self._field[fieldname].opflags &= ~_DISABLED
    #
    # def setFieldReadonly(self, fieldname):
    #     self._field[fieldname].opflags |= _READONLY
    #
    # def resetFieldReadonly(self, fieldname):
    #     self._field[fieldname].opflags &= ~_READONLY
    #
    # def revert(self, fieldname):
    #     """undo the field value to its previous one"""
    #     self._field[fieldname].revert()
    #     for e in self.alias:
    #         e._field[fieldname].revert()
    #
    # def mark(self, fieldname, handle='setpoint'):
    #     self._field[fieldname].mark(handle)
    #     for e in self.alias:
    #         e._field[fieldname].mark(handle)
    #
    # def reset(self, fieldname, data='golden'):
    #     """data='golden' or 'origin'. see CaAction::reset()"""
    #     self._field[fieldname].reset(data)
    #     for e in self.alias:
    #         e._field[fieldname].reset(data)
    #
    # def get(self, fields, handle='readback', unitsys='phy'):
    #     """Get the values for given fields. None if not exists.
    #
    #     Parameters
    #     ----------
    #     fields : str, list
    #         field.
    #     handle : str
    #         'readback', 'setpoint' or 'golden'.
    #     unitsys : the unit system
    #         None for lower level unit.
    #
    #     Examples
    #     --------
    #     >>> get('x')
    #     >>> get(['x', 'y'])
    #     >>> get(['x', 'unknown'])
    #     [ 0, None]
    #     """
    #     kw = {'handle': handle, 'unitsys': unitsys}
    #     if isinstance(fields, basestring):
    #         return self._get_field(fields, **kw)
    #     else:
    #         # a list of fields
    #         return [self._get_field(v, **kw) for v in fields]
    #
    # def _put_field(self, field, val, unitsys, **kwargs):
    #     """Set *val* to *field*. handle='golden' will set value as golden.
    #
    #     See Also
    #     --------
    #     :func:`pv(field=field)`
    #     """
    #     att = field
    #     if att not in self._field:
    #         raise RuntimeError("field '%s' is not defined for '%s'" % (
    #             att, self.name))
    #
    #     decr = self._field[att]
    #     if not decr:
    #         raise AttributeError("field '%s' is not defined for '%s'" % (
    #             att, self.name))
    #     if not decr.pvsp:
    #         raise ValueError("field '%s' in '%s' is not writable" % (
    #             att, self.name))
    #
    #     bc = kwargs.get('bc', 'exception')
    #     wait = kwargs.get("wait", True)
    #     timeout = kwargs.get("timeout", 5)
    #     decr.putSetpoint(val, unitsys, bc=bc, wait=wait, timeout=timeout)
    #
    # def put(self, field, val, **kwargs):
    #     """Set *val* to *field*.
    #
    #     Parameters
    #     ----------
    #     field : str
    #         Element field
    #     val : float, int
    #         The new value.
    #
    #     Keyword Arguments
    #     -----------------
    #     unitsys : str
    #         Unit system.
    #     bc : str
    #         Bounds checking: "exception" will raise a ValueError.
    #         "ignore" will abort the whole setting. "boundary" will use the
    #         boundary value it is crossing.
    #     wait :
    #         The same as in caput
    #     timeout :
    #
    #     See Also
    #     --------
    #     :func:`pv(field=field)`
    #     """
    #     unitsys = kwargs.get("unitsys", 'phy')
    #     bc = kwargs.get("bc", 'exception')
    #     wait = kwargs.get("wait", True)
    #     trig = kwargs.get("trig", None)
    #     timeout = kwargs.get("timeout", 5)
    #
    #     self._put_field(field, val, timeout=timeout, unitsys=unitsys, bc=bc, wait=wait)
    #     for e in self.alias:
    #         e._put_field(field, val, timeout=timeout, unitsys=unitsys, bc=bc, wait=wait)
    #
    #     trig_fld = field + "_trig"
    #     if trig_fld in self.fields() and trig is not None:
    #         self._put_field(field + "_trig", trig,
    #                         unitsys=None, timeout=timeout, wait=True)
    #
    # def settable(self, field):
    #     """check if the field can be changed. not disabled, nor readonly."""
    #     if field not in self._field:
    #         return False
    #     if self._field[field].opflags & _DISABLED:
    #         return False
    #     if self._field[field].opflags & _READONLY:
    #         return False
    #
    #     return self._field[field].settable()
    #
    # def readable(self, field):
    #     """check if the field readable (not disabled)."""
    #     if field not in self._field:
    #         return False
    #     if self._field[field].opflags & _DISABLED:
    #         return False
    #     return True


def merge(elems, field=None, **kwargs):
    """Merge the fields for all elements in a list return it as a single
    element.

    Parameters
    ----------
    elems : list
        a list of element object.
    field :

    Keyword Arguments
    -----------------

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
    :param field:
    :class:`CaElement`
    """

    # count 'field' owners and its rb,wb PVs.
    count, pvdict = {}, {}
    for e in elems:
        fds = e.fields()
        for f in fds:
            if f in count:
                count[f] += 1
            else:
                count[f] = 1
            pvrb = e.pv(field=f, handle='readback')
            pvsp = e.pv(field=f, handle='setpoint')
            if f not in pvdict: pvdict[f] = [[], []]
            # print f, pvrb, pvsp
            pvdict[f][0].extend(pvrb)
            pvdict[f][1].extend(pvsp)

    elem = CaElement(**kwargs)
    # print "merged:", elem
    # consider only the common fields
    if field is None:
        for k, v in count.items():
            if v < len(elems):
                _LOGGER.warning("field '%s' has %d < %d" % (k, v, len(elems)))
                pvdict.pop(k)
        # print pvdict.keys()
        for fld, pvs in pvdict.items():
            if len(pvs[0]) > 0:
                elem.set_get_action(pvs[0], fld, None, '')
            if len(pvs[1]) > 0:
                elem.set_put_action(pvs[1], fld, None, '')
        elem.sb = [e.sb for e in elems]
        elem.se = [e.se for e in elems]
        elem._name = [e.name for e in elems]
    elif field in pvdict:
        pvrb, pvsp = pvdict[field][0], pvdict[field][1]
        if len(pvrb) > 0:
            elem.set_get_action(pvrb, field, None, '')
        if len(pvsp) > 0:
            elem.set_put_action(pvsp, field, None, '')
        # count the element who has the field
        elemgrp = [e for e in elems if field in e.fields()]
        elem.sb = [e.sb for e in elemgrp]
        elem.se = [e.se for e in elemgrp]
        elem._name = [e.name for e in elemgrp]
        # print pvsp
    else:
        _LOGGER.warning("no pv merged for {0}".format([
            e.name for e in elems]))
    # if all raw units are the same, so are the merged element
    for fld in elem.fields():
        units = sorted([e.getUnit(fld, unitsys=None) for e in elems if fld in e.fields()])
        if units[0] == units[-1]:
            elem.setUnit(fld, units[0], unitsys=None)

    return elem


def main():
    pv_props = {
        'field': 'ANG', 'handle': 'setpoint',
        'length': 0.0, 'se': 0.1, 'family': 'HCOR',
        'index': 10,
    }

    elem = CaElement(**pv_props)
    print(elem.family)


if __name__ == '__main__':
    main()
