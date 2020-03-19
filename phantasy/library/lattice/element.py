#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build elements with Channel Access support.
"""

import re
import logging

try:
    basestring
except NameError:
    basestring = str

from epics import PV, get_pv
from phantasy.library.misc import flatten
from phantasy.library.misc import convert_epoch
from phantasy.library.misc import QCallback
from phantasy.library.pv import PV_POLICIES
from phantasy.library.pv import unicorn_read
from phantasy.library.pv import unicorn_write
from phantasy.library.pv import ensure_put
from phantasy.library.settings import get_settings_from_element_list

import numpy as np

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


_LOGGER = logging.getLogger(__name__)

VALID_STATIC_KEYS = ('name', 'family', 'index', 'se', 'length', 'sb',
                     'phy_name', 'phy_type', 'machine')
VALID_CA_KEYS = ('field_eng', 'field_phy', 'handle', 'pv_policy')
# diagnostic device types
DIAG_DTYPES = ('FC', 'EMS', 'PM', 'BPM', 'BCM', 'ND', 'HMR', 'IC', 'VD')


class BaseElement(object):
    """Base class for all elements, contains most of the device properties,
    such as element name, length, location and family. It also keeps a list of
    groups which belongs to.

    ``BaseElement`` does not support Channel Access, ``CaElement`` does.

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
        Longitudinal position at the beginning of device, unit: *m*.
    se : float
        Longitudinal position at the end of device, unit: *m*.
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

    ename = name

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
        """float: Longitudinal position at the beginning of device, *m*."""
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
        """float: Longitudinal position at the end of device, *m*."""
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

    def is_diag(self):
        """Test if element is diagnostic device or not.
        """
        return self._family in DIAG_DTYPES


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

    Keyword Arguments
    -----------------
    wait : bool
        Wait or not (True/False) when issuing set command, which is attached
        to one of 'caput' keyword arguments, default: True.
    timeout : float
        Time out in second for put operation (see wait), default is 10 seconds.
    ensure_put : bool
        Apply ensure set operation or not, default is False, see the notes.
    tolerance : float
        Absolute discrepancy tolerance between current readback value
        and the set goal, default is 0.01.
    ename : str
        Name of element which the field attaches to.
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
    pv_policy : dict
        Name of PV read/write policy, keys: 'read' and 'write', values:
        scaling law function object.
    ftype : str
        Field type, 'ENG' (default) or 'PHY'.
    auto_monitor : bool
        If set True, initialize all channels auto subscribe, default is False.

    Note
    ----
    About `ensure_put` option: If this argument is set True, the set or put
    action to the field value will be ensured to reach the goal, since
    CA put wait action sometimes is not that working as the user expected. To
    make use of this feature, simply set `field.ensure_put = True`, then
    do `field.value = x`, the program will be blocking until `field.value`
    reaches `x`, here assumed `field` is the instance of `CaField` class.
    """

    def __init__(self, name='', **kws):
        self.name = name
        self.ename = kws.get('ename', None)
        self.timeout = kws.get('timeout', None)
        self.wait = kws.get('wait', None)
        self.tolerance = kws.get('tolerance', None)
        self.ensure_put = kws.get('ensure_put', None)
        self.init_auto_monitor = kws.get('auto_monitor', False)
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
        """boolean: Wait or not (True/False) when issuing set command, which
        is attached to one of 'caput' keyword arguments, default: True."""
        return self._wait

    @wait.setter
    def wait(self, b):
        if b is None:
            self._wait = True
        else:
            self._wait = bool(b)

    @property
    def ensure_put(self):
        """boolean: Apply ensure set operation or not, default is False."""
        return self._ensure_put

    @ensure_put.setter
    def ensure_put(self, b):
        if b is None:
            self._ensure_put = False
        else:
            self._ensure_put = bool(b)

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
    def tolerance(self):
        """float: Absolute discrepancy tolerance between current readback value
        and the set goal, default is 0.01."""
        return self._tolerance

    @tolerance.setter
    def tolerance(self, x):
        if x is None:
            self._tolerance = 0.01
        else:
            self._tolerance = float(x)

    @property
    def readback(self):
        """list[str]: Readback PV name, usually ends with *_RD*."""
        return self._rdbk_pv_name

    @readback.setter
    def readback(self, s):
        """If *s* is a string, append *s* to the current readback list,
        otherwise override the current readback PV name list, the
        same policy applies to *setpoint* and *readset*."""
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

        The defined policy is a function, with *readback_pv* attribute as the
        argument, return a value.
        """
        return self._read_policy

    @read_policy.setter
    def read_policy(self, f):
        if f is None:
            self._read_policy = self._default_read_policy
        else:
            self._read_policy = f

    def reset_policy(self, policy=None):
        """Reset policy, by policy name ('read' or 'write'), if not defined,
        reset both."""
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
        """Get the current readback value from readback PVs, intepret with
        read policy as the final field value as a return."""
        if not self.connected():
            return None
        return self.read_policy(self.readback_pv)

    @value.setter
    def value(self, v):
        """Set the current field value as *v*, by applying write policy to
        attached setpoint PVs."""
        if not self.write_access:
            _LOGGER.warning("{} [{}] is read only.".format(self.ename, self.name))
            return
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
        self._rdbk_pv = []
        for i in pvs:
            self._rdbk_pv.append(get_pv(i, auto_monitor=self.init_auto_monitor))

    def _init_rset_pv(self, pvs, **kws):
        self._rset_pv = []
        for i in pvs:
            self._rset_pv.append(get_pv(i, auto_monitor=self.init_auto_monitor))

    def _init_cset_pv(self, pvs, **kws):
        self._cset_pv = []
        for i in pvs:
            self._cset_pv.append(get_pv(i, auto_monitor=self.init_auto_monitor))

    def update(self, **kws):
        """Update PV with defined handle."""
        for k in ('readback', 'readset', 'setpoint'):
            v = kws.get(k)
            if v is not None:
                setattr(self, k, v)
                setattr(self, "{}_pv".format(k), get_pv(v, auto_monitor=self.init_auto_monitor))

    def pvs(self):
        """Return dict of valid pv type and names."""
        pv_types = ('readback', 'readset', 'setpoint')
        pv_names = (self.readback, self.readset, self.setpoint)
        pv_dict = dict(zip(pv_types, pv_names))
        return {k: v for k, v in pv_dict.items() if v is not None}

    def get(self, handle='readback', n_sample=1, timeout=10.0,
            with_timestamp=False, ts_format='raw', keep_raw=False,
            **kws):
        """Get value of PV with specified *handle*, if argument *n_sample* is
        larger than 1, statistical result with averaged value and standard
        deviation will be returned; the sample rate depends on the device
        scan rate. If *timeout* is defined, DAQ will be inactivated after
        *timeout* second. If PV is attached with a list pvs, the returned
        values are arrays, e.g. EQUAD usually has two power supply PVs to
        control one field.

        Warning
        -------
        For the case of devices that generate constant readings, if *n_sample*
        is larger than 1, set *timeout* parameter with a reasonable value is
        required, or this method will hang up your program.

        Parameters
        ----------
        handle : str
            PV handle, 'readback', 'readset' or 'setpoint'.
        n_sample : int
            Sample number, total DAQ count.
        timeout : float
            Timeout in second for the whole DAQ process, set `None` to wait
            forever.
        with_timestamp : bool
            If `True`, return timestamp, default value is `False`.
        ts_format : str
            Format for timestamp, valid options: `raw`, `epoch` and `human`.
        keep_raw : bool
            If `True`, return raw read data as well.

        Returns
        -------
        r : dict
            Valid keys: 'mean', 'std', 'timestamp', 'data', the values are
            the average of all shots, the standard deviation of all shots,
            the timestamp of the first shot, and all the aquired data array.

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

        Get readings with timestamp

        >>> fld.get('readback', with_timestamp=True)

        Define the style of timestamp

        >>> fld.get('readback', with_timestamp=True, ts_format='human')

        Get statistical readings, and keep all the raw data

        >>> fld.get('readback', n_sample=1, with_timestamp=True,
                    ts_format="epoch", keep_raw=True)

        """
        if handle == 'readback':
            pv = self._rdbk_pv
        elif handle == 'readset':
            pv = self._rset_pv
        elif handle == 'setpoint':
            pv = self._cset_pv
        self.set_auto_monitor(True, handle)
        if pv is not None:
            if with_timestamp:
                r = []
                for ipv in pv:
                    if keep_raw:
                        avg, std, ts, all_data = self.__get(ipv, n_sample, ts_format=ts_format, keep_raw=True, timeout=timeout)
                        r.append((avg, std, ts, all_data))
                    else:
                        avg, std, ts, _ = self.__get(ipv, n_sample, ts_format=ts_format, timeout=timeout)
                        r.append((avg, std, ts, []))
                self.set_auto_monitor(False, handle)
                return dict(zip(('mean', 'std', 'timestamp', 'data'), zip(*r)))
            else:
                r = []
                for ipv in pv:
                    if keep_raw:
                        avg, std, _, all_data = self.__get(ipv, n_sample, ts_format="epoch", keep_raw=True, timeout=timeout)
                        r.append((avg, std, '', all_data))
                    else:
                        avg, std, _, _ = self.__get(ipv, n_sample, ts_format="epoch", timeout=timeout)
                        r.append((avg, std, '', []))
                self.set_auto_monitor(False, handle)
                return dict(zip(('mean', 'std', 'timestamp', 'data'), zip(*r)))
        else:
            self.set_auto_monitor(False, handle)
            return None

    def set(self, value, handle='setpoint', **kws):
        """Set value(s) of PV(s) with specified *handle*, accept all *caput*
        keyword arguments.

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

    def __get(self, pvobj, n=1, keep_raw=False, ts_format='raw', timeout=None):
        dq, sq = Queue(n), Queue(1)
        cid = pvobj.add_callback(QCallback(dq, sq))
        try:
            if sq.get(timeout=timeout):
                all_data = np.array([dq.get() for _ in range(dq.qsize())])
                data, ts = all_data[:, 0], all_data[:, 1]
                if not keep_raw:
                    return data.mean(), data.std(), convert_epoch(ts[0], ts_format), []
                else:
                    return data.mean(), data.std(), convert_epoch(ts[0], ts_format), all_data
        except Empty:
            pvobj.remove_callback(cid)
            return pvobj.value, 0.0, convert_epoch(pvobj.timestamp, ts_format), []

    def connected(self, handle="readback"):
        """Check if the *handle* is connected.
        """
        if handle == 'readback':
            pvs = self.readback_pv
        elif handle == 'setpoint':
            pvs = self.setpoint_pv
        else:
            pvs = self.readset_pv
        return {i.connected for i in pvs} == {True}

    def get_pv_name(self, type='readback'):
        if type == 'readback':
            pv = self.readback[0]
        elif type == 'setpoint':
            pv = self.setpoint[0]
        return pv

    def current_setting(self):
        """Return current setpoint value.

        See Also
        --------
        value : get current readback value.
        """
        if not self.connected('setpoint'):
            _LOGGER.warning(
                "{} [{}] is not connected".format(self.ename, self.name))
            return None
        return self.read_policy(self.setpoint_pv)

    def set_auto_monitor(self, auto_monitor=True, handle='readback'):
        """Set auto_monitor bit True or False for the given PV type.
        """
        if handle == 'readback':
            pvs = self.readback_pv
        elif handle == 'setpoint':
            pvs = self.setpoint_pv
        else:
            pvs = self.readset_pv
        for i in pvs:
            i.auto_monitor = auto_monitor

    def get_auto_monitor(self, handle='readback'):
        """Get auto_monitor bit for the given PV type.
        """
        if handle == 'readback':
            pvs = self.readback_pv
        elif handle == 'setpoint':
            pvs = self.setpoint_pv
        else:
            pvs = self.readset_pv
        am_set = {pv.auto_monitor for pv in pvs}
        if len(am_set) == 1:
            return am_set.pop()
        else:
            raise RuntimeError(
                    "All {} PVs should have the same monitoring policy.".format(handle))

    @property
    def read_access(self):
        """bool: If field readable."""
        return {pv.read_access for pv in self.readback_pv} == {True}

    @property
    def write_access(self):
        """bool: If field writable."""
        return {pv.write_access for pv in self.setpoint_pv} == {True}

    @property
    def access(self):
        """tuple: (read_access, write_access), access permission of field.
        """
        # read
        read_access = {pv.read_access for pv in self.readback_pv}
        # write
        write_access = {pv.write_access for pv in self.setpoint_pv}
        return read_access == {True}, write_access == {True}


class CaElement(BaseElement):
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
    auto_monitor : bool
        If set True, initialize all channels auto subscribe, default is False.

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
        # unicorn laws, {'fname1': <fn>, 'fname2':...}
        # if 'fname' is physics unit, <fn> converts from physics to engineering
        # if 'fname' is engineering unit, <fn> converts from engineering to physics
        self.__unicorn = {}

        pv_data = kws.get('pv_data', None)
        am = kws.get('auto_monitor', False)
        if pv_data is not None:
            if isinstance(pv_data, list):
                self.process_pv(*pv_data, auto_monitor=am)
            elif isinstance(pv_data, dict):
                self.process_pv(**pv_data, auto_monitor=am)

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
        am = kws.get('auto_monitor', False)
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
            u_policy = {'n': lambda x:x, 'p': lambda x:x}

        pv = kws.get('pv', None)
        #
        if field_name is not None:
            self.__unicorn[field_name] = u_policy['p']
            self.set_field(field_name, pv, handle_name, ftype='ENG',
                           pv_policy=pv_policy, auto_monitor=am)
        if field_name_phy is not None:
            self.__unicorn[field_name_phy] = u_policy['n']
            self.set_field(field_name_phy, pv, handle_name, ftype='PHY',
                           pv_policy=pv_policy_phy, auto_monitor=am)

    def set_field(self, field, pv, handle=None, **kws):
        """Set element field with CA support, i.e. dynamic field.

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
        auto_monitor : bool
            If set True, initialize all channels auto subscribe, default is False.
        """
        if handle is None:
            handle = 'readback'
        if field not in self._fields:
            new_field = CaField(name=field,
                                ename=self.name,
                                ftype=kws.get('ftype'),
                                pv_policy=kws.get('pv_policy'),
                                auto_monitor=kws.get('auto_monitor'),
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
        auto_monitor : bool
            If set True, initialize all channels auto subscribe, default is False.
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

    def process_pv(self, pv_name, pv_props, pv_tags=None, u_policy=None, **kws):
        """Process PV record to update element with properties and tags.

        Parameters
        ----------
        pv_name : str
            PV name.
        pv_props : dict
            PV properties, key-value pairs.
        pv_tags : list
            PV tag list.

        Keyword Arguments
        -----------------
        auto_monitor : bool
            If set True, initialize all channels auto subscribe, default is False.
        """
        if not isinstance(pv_name, basestring):
            raise TypeError("{} is not a valid type".format(type(pv_name)))

        # properties
        self.update_properties(pv_props, pv=pv_name, u_policy=u_policy, **kws)
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
            print("{1} of {0} is not defined, valid ones are ({2}).".format(
                self.name, field, ', '.join(sorted(self.fields))))
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
            fld = self._fields[key]
            if fld.ensure_put:
                ensure_put(fld, value, fld.tolerance, fld.timeout)
            else:
                self._fields[key].value = value
            self._last_settings.update([(key, value)])
        else:
            super(CaElement, self).__setattr__(key, value)

    def __dir__(self):
        return dir(CaElement) + list(self._fields.keys()) + list(self.__dict__.keys())

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

    def convert(self, value, field):
        """Interpret the *value* of *field* of element, if *field* is physics
        field, returned one is in engineering unit; if *field* is engineering
        field, returned one is in physics unit.

        Parameters
        ----------
        value : float
            Value of field, no necessary be the current online reading.
        field : str
            Field name of element.

        Returns
        -------
        r : float
            Value Interpreted in another unit, from physics engineering or
            from engineering to physics, depends on the field type.

        Examples
        --------
        >>> mp = MachinePortal("FRIB", "MEBT")
        >>> quad = mp.get_elements(type='QUAD', name='*D1078*')[0]
        >>> # convert I = 100 A, to gradient 15.177 T/m
        >>> quad.convert(value=100, field='I')
        15.17734389601
        >>> quad.convert(value=15, field='GRAD')
        98.7534891752199
        """
        if field not in self.__unicorn:
            _LOGGER.warning("Invalid field name.")
            return
        return self.__unicorn[field](value)

    def current_setting(self, field):
        """Return the value of current setting (setpoint) for dynamic field
        defined by *field*, if setpoint PV is not available, return None.

        Parameters
        ----------
        field : str
            Name of valid dynamic field.

        Returns
        -------
        r :
            Field current setting or None.

        See Also
        --------
        get_settings : Get field setpoint value from given setpoint pv values.
        """
        if field not in self.fields:
            _LOGGER.error("Invalid field, should be one of {}.".format(self.fields))
            return None
        fld = self.get_field(field)
        return fld.current_setting()

    def get_settings(self, field, settings):
        """Get the *field* setpoint value from *settings*.

        Parameters
        ----------
        field : str
            Dynamic field name of element.
        settings : dict
            Key-value pairs of setpoint PV name and value.

        Returns
        -------
        r : float
            Setting value of defined dynamic field, or None.

        See Also
        --------
        current_setting : Get current field setting.
        """
        fld = self.get_field(field)
        sp_vals = [settings.get(sp) for sp in fld.setpoint]
        if None in sp_vals:
            _LOGGER.warning(
                "Failed to get setpoint PV reading(s) of '{} [{}]'.".format(self.name, field))
            print(
                "Failed to get setpoint PV reading(s) of '{} [{}]'.".format(self.name, field))
            return None
        return fld.read_policy([Number(float(x)) for x in sp_vals])

    def ensure_put(self, field, goal, tol=None, timeout=None):
        """Ensure set the *field* of element to *goal* within the
        discrepancy tolerance of *tol*, within the max *timeout* secs.
        If field is invalid, return None.

        Parameters
        ----------
        field : str
            Dynamic field name of element.
        goal : float
            The final value that the field of element would like to reach.
        tol : float
            Tolerance for discrepancy between current readback
            value and the set goal, default is 0.01.
        timeout : float
            Maximum wait time, default is 10.0 sec.

        Returns
        -------
        r : str
            Returns what `ensure_put` returns, or None.

        See Also
        --------
        :func:`~phantasy.library.pv.epics_tools.ensure_put`
        """
        fld = self.get_field(field)
        if fld is None:
            return None
        return ensure_put(fld, goal, tol, timeout)

    def get_current_settings(self, field_of_interest=None,
                                     only_physics=True):
        """Get current setpoint readings of interested dynamic fields.

        Parameters
        ----------
        field_of_interest : list
            Interested physics field names, if not defined, use all valid ones.
        only_physics : bool
            If `True`, only return physics settings otherwise return both
            physics and engineering field settings.

        Returns
        -------
        s : Settings
            Settings of interested physics fields.
        """
        field_list = self.get_phy_fields() if field_of_interest is None else field_of_interest
        return get_settings_from_element_list([self], data_source='control',
                            field_of_interest={self.name: field_list},
                            only_physics=only_physics)


class Number(float):
    def __init__(self, v):
        self.value = v
        self.auto_monitor = True

    def get(self):
        return self.value


def build_element(sp_pv, rd_pv, ename=None, fname=None, **kws):
    """Build CaElement from general setpoint and readback PV names, *sp_pv*
    and *rd_pv* could be the same. The created CaElement is of the element
    name defined by *ename*, and engineering field name defined by *fname*,
    the corresponding physics field is defined as *fname*_phy.

    If *ename* or *fname* is not defined, smart matching will be applied to find the
    element name from PV names based on naming convention.

    e.g.: PV is named as: SYSTEM_SUBSYS:DTYPE_DNUM:FIELD_HANDLE, then ename is
    "SYSTEM_SUBSYS:DTYPE_DNUM", engineering field name is "FIELD", physics
    field name is "FIELD_PHY".

    Parameters
    ----------
    sp_pv : str
        Setpoint PV name.
    rd_pv : str
        Readback PV name.
    ename : str
        Element name.
    fname : str
        Field name.

    Keyword Arguments
    -----------------
    field_phy : str
        Physics field name w.r.t. *fname*.
    index : int
        Element index, default is -1.
    length : float
        Element length, default is 0.0.
    sb : float
        Start s-position of element, default is -1.0, if not defined, will
        try to extract from the PV name.
    family : str
        Element family (type), default is 'PV'.

    Returns
    -------
    elem : CaElement
        CaElement object.
    """
    if ename is None or fname is None:
        ename_, fname_ = _parse_pv_name(sp_pv)
    ename = ename if ename is not None else ename_
    fname = fname if fname is not None else fname_
    fname_phy = "{}_PHY".format(fname)

    elem = CaElement(name=ename)
    pv_props = {
        'field_eng': fname,
        'field_phy': kws.get('field_phy', fname_phy),
        'handle': 'readback',
        'pv_policy': 'DEFAULT',
        'index': kws.get('index', -1),
        'length': kws.get('length', 0.0),
        'sb': kws.get('sb', _get_spos(sp_pv)),
        'family': kws.get('family', 'PV'),
    }
    pv_tags = []
    for pv, handle in zip((sp_pv, rd_pv), ('setpoint', 'readback')):
        pv_props['handle'] = handle
        elem.process_pv(pv, pv_props, pv_tags)
    return elem


def _get_spos(pvname):
    """Extract s-position from PV name.

    Note
    ----
    This is FRIB specific, D### to meter.

    Returns
    -------
    pos : float
        S-pos of PV device.
    """
    # pos
    try:
        r = re.match(r'.*D([0-9]{4}).*', pvname)
        assert r is not None
    except AssertionError:
        pos = -1
    else:
        pos = float(r.group(1)) / 10.0  # m
    return pos


def _parse_pv_name(pvname):
    """Extract element name, field name from pv name, based on the following
    naming convention: SYSTEM_SUBSYS:DEVICE_D####:FIELD_HANDLE,
    if HANDLE is not CSET nor RD, FIELD_HANDLE will be extracted as field name.

    Parameters
    ----------
    pvname : str
        PV name.

    Returns
    -------
    r : tuple
        A tuple of element name, field name.
    """
    pattern1 = r"(.*):(.*)_(CSET|RD)"
    pattern2 = r"(.*):(.*)"
    try:
        r = re.match(pattern1, pvname)
        assert r is not None
    except AssertionError:
        r = re.match(pattern2, pvname)
    finally:
        ename = r.group(1)
        fname = r.group(2)
    element_name = '{}:{}'.format(ename, fname)
    field_name = fname
    return element_name, field_name


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
