#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build device upon a collection of CaFields attached to EMS element.
"""

import logging
import os

from phantasy import ensure_put
from phantasy import epoch2human
from phantasy import Configuration

from .utils import find_dconf

_LOGGER = logging.getLogger(__name__)


TS_FMT = "%Y-%m-%d %H:%M:%S"

try:
    basestring
except NameError:
    basestring = str

XY2ID = {'X': 1, 'Y': 2}


class Device(object):
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

    def __init__(self, elem, xoy='X', dconf=None):
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

        # length: [m]
        self.length = float(self.dconf.get(name, 'length')) / 1000.0

        # length1,2: [m]
        self.length1 = float(self.dconf.get(name, 'length1')) / 1000.0
        self.length2 = float(self.dconf.get(name, 'length2')) / 1000.0

        # gap: [m]
        self.gap = float(self.dconf.get(name, 'gap')) / 1000.0

        # slit, width & thickness: [m]
        self.slit_width = float(self.dconf.get(name, 'slit_width')) / 1000.0
        self.slit_thickness = float(self.dconf.get(name, 'slit_thickness')) / 1000.0

        # bias volt threshold
        self.bias_volt_threshold = float(self.dconf.get(name, 'bias_volt_threshold'))

        # info
        self.info = self.dconf.get(name, 'info')

    def update_xoy_conf(self, name):
        # xoy
        # default pos/volt alter ranges, [mm], [V], settling time: [sec]
        kxoy = "{}.{}".format(name, self.xoy)
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
        """float: E-dipole plat length, [m]."""
        return self._length

    @length.setter
    def length(self, x):
        self._length = x

    @property
    def length1(self):
        """float: Length from slit-entrance to plate, [m]."""
        return self._length1

    @length1.setter
    def length1(self, x):
        self._length1 = x

    @property
    def length2(self):
        """float: Length from plate to slit-exit, [m]."""
        return self._length2

    @length2.setter
    def length2(self, x):
        self._length2 = x

    @property
    def gap(self):
        """float: Distance between plates, [m]."""
        return self._gap

    @gap.setter
    def gap(self, x):
        self._gap = x

    @property
    def slit_width(self):
        """float: Slit width, [m]."""
        return self._slit_width

    @slit_width.setter
    def slit_width(self, x):
        self._slit_width = x

    @property
    def slit_thickness(self):
        """float: Slit thickness, [m]."""
        return self._slit_thickness

    @slit_thickness.setter
    def slit_thickness(self, x):
        self._slit_thickness = x

    @property
    def pos_begin(self):
        """float: Start position of motor, [mm]."""
        return self._pos_begin

    @pos_begin.setter
    def pos_begin(self, x):
        self._pos_begin = x

    @property
    def pos_end(self):
        """float: End position of motor, [mm]."""
        return self._pos_end

    @pos_end.setter
    def pos_end(self, x):
        self._pos_end = x

    @property
    def pos_step(self):
        """float: Step of motor moving, [mm]."""
        return self._pos_step

    @pos_step.setter
    def pos_step(self, x):
        self._pos_step = x

    @property
    def volt_begin(self):
        """float: Start voltage applied on plates, [V]."""
        return self._volt_begin

    @volt_begin.setter
    def volt_begin(self, x):
        self._volt_begin = x

    @property
    def volt_end(self):
        """float: End voltage applied on plates, [V]."""
        return self._volt_end

    @volt_end.setter
    def volt_end(self, x):
        self._volt_end = x

    @property
    def volt_step(self):
        """float: Step of voltage altering, [V]."""
        return self._volt_step

    @volt_step.setter
    def volt_step(self, x):
        self._volt_step = x

    @property
    def pos_settling_time(self):
        """float: Settling time of position altering, [sec]."""
        return self._pos_settling_time

    @pos_settling_time.setter
    def pos_settling_time(self, x):
        self._pos_settling_time = x

    @property
    def volt_settling_time(self):
        """float: Settling time of voltage altering, [sec]."""
        return self._volt_settling_time

    @volt_settling_time.setter
    def volt_settling_time(self, x):
        self._volt_settling_time = x

    @property
    def bias_volt_threshold(self):
        """float: Threshold of bias voltage applied on FC, [V], the applied
        bias voltage should be less or equal than this value."""
        return self._bias_volt_threshold

    @bias_volt_threshold.setter
    def bias_volt_threshold(self, x):
        self._bias_volt_threshold = x

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
        if self.is_bias_volt_ready():
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

    def set_params(self):
        self.set_pos_begin()
        self.set_pos_end()
        self.set_pos_step()
        self.set_volt_begin()
        self.set_volt_end()
        self.set_volt_step()

    def move(self, timeout=600):
        """Start scan."""
        scan_status = getattr(self.elem, 'SCAN_STATUS{}'.format(self._id))
        if scan_status != 0:
            raise RuntimeError("Device is busy, not be ready for moving.")
        setattr(self.elem, 'START_SCAN{}'.format(self._id))
        self.init_data_cb()
        wait(scan_status, 0, timeout)
        self.reset_data_cb()
        print("Move is done.")

    def init_data_cb(self):
        self._data_pv = self.elem.get_field('DATA{}'.format(self._id)).readback_pv()
        self._cid = data_pv.add_callback(self.on_data_updated)

    def reset_data_cb(self):
        self._data_pv.remove_callback(self._cid)

    def on_data_updated(self, **kws):
        data = kws.get('value')
        print(data)
