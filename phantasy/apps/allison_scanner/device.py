#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build device upon a collection of CaFields attached to EMS element.
"""

import logging
import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from numpy import ndarray

from phantasy import Configuration
from phantasy import ensure_put
from phantasy.apps.wire_scanner.utils import wait as _wait
from .utils import find_dconf

_LOGGER = logging.getLogger(__name__)


TS_FMT = "%Y-%m-%d %H:%M:%S"

try:
    basestring
except NameError:
    basestring = str

XY2ID = {'X': 1, 'Y': 2}


class Device(QObject):
    """Build allison-scanner devices from CaElement, which family is 'EMS',
    After instantiating, the operations like device control, data analysis
    control could be expected.

    Parameters
    ----------
    elem : CaElement
        CaElement object, which is one element of high-level lattice.
    xoy : str
        Define the measurement direction, 'X' or 'Y'.
    dconf : callable or str
        Configuration object for this device, or file path of the
        configuration file (.ini file). If not given, will read from
        the following locations, `~/.phantasy/ems.ini`,
        `/etc/phantasy/ems.ini` or from the package directory, see the
        loaded full path: `Device.dconf.config_path`.
    """

    data_changed = pyqtSignal(ndarray)
    finished = pyqtSignal()

    def __init__(self, elem, xoy='X', dconf=None):
        super(self.__class__, self).__init__()
        self.elem = elem

        if dconf is None:
            self.dconf = Configuration(find_dconf())
        elif isinstance(dconf, Configuration):
            self.dconf = dconf
        elif isinstance(dconf, basestring) and os.path.isfile(dconf):
            self.dconf = Configuration(dconf)
        else:
            _LOGGER.error("Cannot find device configuration.")

        # name
        self.name = name = elem.name
        # orientation
        self.xoy = xoy

        # length: [mm]
        self.length = float(self.dconf.get(name, 'length'))

        # length1,2: [mm]
        self.length1 = float(self.dconf.get(name, 'length1'))
        self.length2 = float(self.dconf.get(name, 'length2'))

        # gap: [mm]
        self.gap = float(self.dconf.get(name, 'gap'))

        # slit, width & thickness: [mm]
        self.slit_width = float(self.dconf.get(name, 'slit_width'))
        self.slit_thickness = float(self.dconf.get(name, 'slit_thickness'))

        # bias volt threshold
        self.bias_volt_threshold = float(self.dconf.get(name, 'bias_volt_threshold'))

        # info
        self.info = self.dconf.get(name, 'info')

    def update_xoy_conf(self, name):
        # xoy
        # default pos/volt alter ranges, [mm], [V], settling time: [sec]
        self.kxoy = kxoy = "{}.{}".format(name, self.xoy)
        self.pos_begin = float(self.dconf.get(kxoy, 'pos_begin'))
        self.pos_end = float(self.dconf.get(kxoy, 'pos_end'))
        self.pos_step = float(self.dconf.get(kxoy, 'pos_step'))
        self.pos_settling_time = float(self.dconf.get(kxoy, 'pos_settling_time'))
        self.volt_begin = float(self.dconf.get(kxoy, 'volt_begin'))
        self.volt_end = float(self.dconf.get(kxoy, 'volt_end'))
        self.volt_step = float(self.dconf.get(kxoy, 'volt_step'))
        self.volt_settling_time = float(self.dconf.get(kxoy, 'volt_settling_time'))

    @property
    def xoy(self):
        """str: Device is for 'X' measurement or 'Y'."""
        return self._xoy

    @xoy.setter
    def xoy(self, s):
        s = s.upper()
        if s not in ('X', 'Y'):
            s = 'X'
        self._xoy = s
        self._id = XY2ID[self._xoy]
        self.update_xoy_conf(self.name)

    @property
    def name(self):
        """str: Element/device name."""
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    @property
    def length(self):
        """float: E-dipole plat length, [mm]."""
        return self._length

    @length.setter
    def length(self, x):
        self._length = x
        self.dconf.set(self.name, 'length', str(x))

    @property
    def length1(self):
        """float: Length from slit-entrance to plate, [mm]."""
        return self._length1

    @length1.setter
    def length1(self, x):
        self._length1 = x
        self.dconf.set(self.name, 'length1', str(x))

    @property
    def length2(self):
        """float: Length from plate to slit-exit, [mm]."""
        return self._length2

    @length2.setter
    def length2(self, x):
        self._length2 = x
        self.dconf.set(self.name, 'length2', str(x))

    @property
    def gap(self):
        """float: Distance between plates, [mm]."""
        return self._gap

    @gap.setter
    def gap(self, x):
        self._gap = x
        self.dconf.set(self.name, 'gap', str(x))

    @property
    def slit_width(self):
        """float: Slit width, [mm]."""
        return self._slit_width

    @slit_width.setter
    def slit_width(self, x):
        self._slit_width = x
        self.dconf.set(self.name, 'slit_width', str(x))

    @property
    def slit_thickness(self):
        """float: Slit thickness, [mm]."""
        return self._slit_thickness

    @slit_thickness.setter
    def slit_thickness(self, x):
        self._slit_thickness = x
        self.dconf.set(self.name, 'slit_thickness', str(x))

    @property
    def pos_begin(self):
        """float: Start position of motor, [mm]."""
        return self._pos_begin

    @pos_begin.setter
    def pos_begin(self, x):
        self._pos_begin = x
        self.dconf.set(self.kxoy, 'pos_begin', str(x))

    @property
    def pos_end(self):
        """float: End position of motor, [mm]."""
        return self._pos_end

    @pos_end.setter
    def pos_end(self, x):
        self._pos_end = x
        self.dconf.set(self.kxoy, 'pos_end', str(x))

    @property
    def pos_step(self):
        """float: Step of motor moving, [mm]."""
        return self._pos_step

    @pos_step.setter
    def pos_step(self, x):
        self._pos_step = x
        self.dconf.set(self.kxoy, 'pos_step', str(x))

    @property
    def volt_begin(self):
        """float: Start voltage applied on plates, [V]."""
        return self._volt_begin

    @volt_begin.setter
    def volt_begin(self, x):
        self._volt_begin = x
        self.dconf.set(self.kxoy, 'volt_begin', str(x))

    @property
    def volt_end(self):
        """float: End voltage applied on plates, [V]."""
        return self._volt_end

    @volt_end.setter
    def volt_end(self, x):
        self._volt_end = x
        self.dconf.set(self.kxoy, 'volt_end', str(x))

    @property
    def volt_step(self):
        """float: Step of voltage altering, [V]."""
        return self._volt_step

    @volt_step.setter
    def volt_step(self, x):
        self._volt_step = x
        self.dconf.set(self.kxoy, 'volt_step', str(x))

    @property
    def pos_settling_time(self):
        """float: Settling time of position altering, [sec]."""
        return self._pos_settling_time

    @pos_settling_time.setter
    def pos_settling_time(self, x):
        self._pos_settling_time = x
        self.dconf.set(self.kxoy, 'pos_settling_time', str(x))

    @property
    def volt_settling_time(self):
        """float: Settling time of voltage altering, [sec]."""
        return self._volt_settling_time

    @volt_settling_time.setter
    def volt_settling_time(self, x):
        self._volt_settling_time = x
        self.dconf.set(self.kxoy, 'volt_settling_time', str(x))

    @property
    def bias_volt_threshold(self):
        """float: Threshold of bias voltage applied on FC, [V], the applied
        bias voltage should be less or equal than this value."""
        return self._bias_volt_threshold

    @bias_volt_threshold.setter
    def bias_volt_threshold(self, x):
        self._bias_volt_threshold = x
        self.dconf.set(self.name, 'bias_volt_threshold', str(x))

    def is_bias_volt_ready(self, mode):
        # test if bias voltage (setpoint, readback) for FC is OK.
        if mode == 'setpoint':
            return self.elem.current_setting(field="BIAS_VOLT") <= self.bias_volt_threshold
        else:  # readback
            return self.elem.BIAS_VOLT <= self.bias_volt_threshold

    def init_bias_voltage(self, timeout=10):
        _LOGGER.info("Initialize bias voltage for FC...")
        s1 = self.turn_on_bias_voltage(timeout)
        if s1:
            self.set_bias_voltage(timeout)

    def turn_on_bias_voltage(self, timeout=10):
        _LOGGER.info("Turn on bias voltage for FC...")
        ensure_put(self.elem, 'BIAS_VOLT_ON', 1, tol=1.0, timeout=timeout)
        if self.elem.BIAS_VOLT_ON == 1:
            _LOGGER.info("Bias voltage switch is ON.")
            return True
        else:
            _LOGGER.info("Bias voltage switch cannot be ON.")
            return False

    def set_bias_voltage(self, timeout=10):
        _LOGGER.info("Set bias voltage for FC...")
        volt = self.bias_volt_threshold
        ensure_put(self.elem, 'BIAS_VOLT', volt, tol=1.0, timeout=timeout)
        _LOGGER.info("Bias voltage now is {}.".format(self.elem.BIAS_VOLT))
        if self.is_bias_volt_ready('readback'):
            _LOGGER.info("Bias voltage is ready.")
            return True
        else:
            _LOGGER.info("Bias voltage is not ready.")
            return False

    def enable(self, timeout=10):
        """Make device ready for the movement."""
        _LOGGER.info("Enable device...")
        fname = "ENABLE_SCAN{}".format(self._id)
        r = ensure_put(self.elem, fname, 1, tol=1.0, timeout=timeout)
        if r == 'PutFinished':
            _LOGGER.info("Device is enabled.")
            return True
        else:
            _LOGGER.info("Device is not enabled.")
            return False

    def set_pos_begin(self):
        """Set live config with current config."""
        setattr(self.elem, 'START_POS{}'.format(self._id), self.pos_begin)

    def set_pos_end(self):
        setattr(self.elem, 'STOP_POS{}'.format(self._id), self.pos_end)

    def set_pos_step(self):
        setattr(self.elem, 'STEP_POS{}'.format(self._id), self.pos_step)

    def set_volt_begin(self):
        setattr(self.elem, 'START_VOLT{}'.format(self._id), self.volt_begin)

    def set_volt_end(self):
        setattr(self.elem, 'STOP_VOLT{}'.format(self._id), self.volt_end)

    def set_volt_step(self):
        setattr(self.elem, 'STEP_VOLT{}'.format(self._id), self.volt_step)

    def set_pos_settling_time(self):
        setattr(self.elem, 'WAIT_POS{}'.format(self._id), self.pos_settling_time)

    def set_volt_settling_time(self):
        setattr(self.elem, 'WAIT_VOLT{}'.format(self._id), self.volt_settling_time)

    def get_pos_begin(self):
        """Return live config from controls network."""
        return getattr(self.elem, 'START_POS{}'.format(self._id))

    def get_pos_end(self):
        return getattr(self.elem, 'STOP_POS{}'.format(self._id))

    def get_pos_step(self):
        return getattr(self.elem, 'STEP_POS{}'.format(self._id))

    def get_volt_begin(self):
        return getattr(self.elem, 'START_VOLT{}'.format(self._id))

    def get_volt_end(self):
        return getattr(self.elem, 'STOP_VOLT{}'.format(self._id))

    def get_volt_step(self):
        return getattr(self.elem, 'STEP_VOLT{}'.format(self._id))

    def get_pos_settling_time(self):
        return getattr(self.elem, 'WAIT_POS{}'.format(self._id))

    def get_volt_settling_time(self):
        return getattr(self.elem, 'WAIT_VOLT{}'.format(self._id))

    def sync_params(self):
        """Pull device config from controls network, update
        regarding attr, and dconf as well.
        """
        ks = ['{}_{}'.format(u, v) for u in ('pos', 'volt')
              for v in ('begin', 'end', 'step', 'settling_time')]
        for s in ks:
            v = getattr(self, 'get_{}'.format(s))()
            setattr(self, s, v)
            _LOGGER.info("Sync '{}' with '{}'.".format(s, v))

    def set_params(self):
        self.set_pos_begin()
        self.set_pos_end()
        self.set_pos_step()
        self.set_volt_begin()
        self.set_volt_end()
        self.set_volt_step()

    def abort(self):
        setattr(self.elem, 'ABORT_SCAN{}'.format(self._id), 1)

    def move(self, timeout=600, wait=True, validate=True):
        """Start scan."""
        if validate:  # check scan status or not
            s = self.check_status()
            if s != 0:
                raise RuntimeError("Device is busy, not be ready for moving.")

        self.init_data_cb()
        setattr(self.elem, 'START_SCAN{}'.format(self._id), 1)
        if wait:
            _wait(self.get_status_pv(), 0, timeout)
            self.reset_data_cb()
            print("Move is done.")

    def get_status_pv(self):
        ss_fld_name = 'SCAN_STATUS{}'.format(self._id)
        ss_fld = self.elem.get_field(ss_fld_name)
        ss_pv = ss_fld.readback_pv[0]
        return ss_pv

    def check_status(self):
        pv = self.get_status_pv()
        return pv.get()

    def run_all_in_one(self):
        self.enable()
        self.set_params()
        self.move()
        print("Run-All-in-One is done.")

    def init_data_cb(self):
        self._status_pv = self.elem.get_field('SCAN_STATUS{}'.format(self._id)).readback_pv[0]
        self._scid = self._status_pv.add_callback(self.on_status_updated)
        self._data_pv = self.elem.get_field('DATA{}'.format(self._id)).readback_pv[0]
        self._data_pv.auto_monitor=True
        self._dcid = self._data_pv.add_callback(self.on_data_updated)

    def reset_data_cb(self):
        self._data_pv.remove_callback(self._dcid)
        self._status_pv.remove_callback(self._scid)
        self.finished.emit()

    def on_status_updated(self, value, **kws):
        if value == 12:
            self.reset_data_cb()

    def on_data_updated(self, value, **kws):
        self.data_changed.emit(value)

    def __repr__(self):
        s = "Device configuration: [{}.{}]".format(self.name, self.xoy)
        s += "\n--- info: {}".format(self.info)
        s += "\n--- length: {}".format(self.length)
        s += "\n--- length-1: {}, length-2: {}".format(self.length1, self.length2)
        s += "\n--- gap: {}".format(self.gap)
        s += "\n--- slit width: {}".format(self.slit_width)
        s += "\n--- slit thickness: {}".format(self.slit_thickness)
        s += "\n--- bias voltage threshold: {}".format(self.bias_volt_threshold)
        s += "\n--- pos start: {}, end: {}, step: {}".format(self.pos_begin, self.pos_end, self.pos_step)
        s += "\n--- volt start: {}, end: {}, step: {}".format(self.volt_begin, self.volt_end, self.volt_step)
        s += "\n--- settling times, pos: {}, volt: {}".format(self.pos_settling_time, self.volt_settling_time)
        return s

    def save_dconf(self, filepath):
        with open(filepath, 'w') as f:
            self.dconf.write(f)

    def __eq__(self, other):
        xoy0, xoy0_other = self.xoy, other.xoy
        attr_all = ('bias_volt_threshold', 'gap',
                    'length', 'length1', 'length2',
                    'slit_width', 'slit_thickness',
                    'pos_begin', 'pos_end', 'pos_step',
                    'pos_settling_time',
                    'volt_begin', 'volt_end', 'volt_step',
                    'volt_settling_time')
        for xoy in ['X', 'Y']:
            self.xoy = xoy
            other.xoy = xoy
            for i in attr_all:
                if getattr(self, i) != getattr(other, i):
                    self.xoy = xoy0
                    other.xoy = xoy0_other
                    return False

        self.xoy = xoy0
        other.xoy = xoy0_other
        return True

    @property
    def geometric_factor(self):
        """float: Geometric factor based on device configuration.
        """
        l_total = self.length + self.length1 + self.length2
        return (self.length + 2 * self.length2) / l_total

    @property
    def prefactor1(self):
        return (self.length + 2 * self.length1) / (self.length + 2 * self.length2)

    @property
    def prefactor2(self):
        l_total = self.length + self.length1 + self.length2
        slit_thickness = self.slit_thickness
        return slit_thickness * 2 * (self.length2 - self.length1) / \
                l_total / (l_total + 2 * slit_thickness)

    @property
    def dxp0(self):
        # delta_x'
        return 2 * self.slit_width / (self.length + self.length1 + self.length2)
