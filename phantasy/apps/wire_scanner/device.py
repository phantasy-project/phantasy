#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class built upon a collection of CaField(s) attached to PM element.
"""
import os
import logging

from phantasy import Configuration

from .utils import wait

_LOGGER = logging.getLogger(__name__)

try:
    basestring
except NameError:
    basestring = str

FORK_BIT_MAPPING = {
    'large': (1, 2,),
    'small': (1,),
    'flapper': (1, 2,),
}

class Device(object):
    """Build wire-scanner devices from CaElement, which family is 'PM'.
    After instantiating, the operations like device control, DAQ control
    could be expected.

    Parameters
    ----------
    elem : CaElement
        CaElement object, which is one element of high-level lattice.
    dconf : callable or str
        Configuration object for this device, or file path of the
        configuration file (.ini file).

    See Also
    --------
    :class:`~phantasy.CaElement`
    :class:`~phantasy.MachinePortal`
    :class:`~phantasy.Configuration`
    """
    def __init__(self, elem, dconf):
        self.elem = elem

        if isinstance(dconf, Configuration):
            self.dconf = dconf
        elif isinstance(dconf, basestring) and os.path.isfile(dconf):
            self.dconf = Configuration(dconf)
        else:
            _LOGGER.error("Cannot find device configuration.")

        # name
        self.name = name = elem.name

        # fork ids
        self._fork_ids = tuple()

        # device type, see .ini file
        self.dtype = dconf.get(name, 'type')

        # scan range
        self.scan_start_pos = dconf.getarray(name, 'start_pos_val')
        self.scan_stop_pos = dconf.getarray(name, 'stop_pos_val')

    @property
    def scan_start_pos(self):
        """list[float]: Scan start positions of all forks.
        """
        return self._scan_start_pos

    @scan_start_pos.setter
    def scan_start_pos(self, arr):
        self._scan_start_pos = [float(i) for i in arr]

    @property
    def scan_stop_pos(self):
        """list[float]: Scan stop positions of all forks.
        """
        return self._scan_stop_pos

    @scan_stop_pos.setter
    def scan_stop_pos(self, arr):
        self._scan_stop_pos = [float(i) for i in arr]

    @property
    def dtype(self):
        """str: Device type, fork configurtion.
        """
        return self._dtype

    @dtype.setter
    def dtype(self, s):
        self._dtype = s
        #
        self._fork_ids = FORK_BIT_MAPPING[self._dtype]

    @property
    def fork_ids(self):
        """tuple: Fork ids.
        """
        return self._fork_ids

    @property
    def name(self):
        """str: Element/device name.
        """
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    def initialize(self):
        """Initilize device.

        1. initialize potentiometer
        2. enable scan, get motor ready to move
        3. initialize motor position, i.e. extract forks to outward limit
        4. reset interlock signals, only ONE folk is moving
        """
        self.init_potentiometer()
        self.enable_scan()
        self.init_motor_pos()
        self.reset_interlock()

    def run_after_init(self):
        """Operate device.

        5. set scan start/stop position
        6. apply bias voltage
        7. move
        """
        self.initialize()
        self.set_scan_range()
        self.set_bias_volt()
        self.move()

    def run_all(self):
        """do 1 to 7.
        """
        self.init_potentiometer()
        self.enable_scan()
        self.init_motor_pos()
        self.reset_interlock()
        self.set_scan_range()
        self.set_bias_volt()
        self.move()
        self.init_motor_pos()

    def init_potentiometer(self, init_bit=1, **kws):
        """Initialize potentiometer.

        Parameters
        ----------
        init_bit : int
            Init bit that should be put to potentiometer.

        Keyword Arguments
        -----------------
        field_prefix : str
            String of the field name, excluding fork id.
        """
        _LOGGER.info("Initialize potentiometer...")

        fld_prefix = kws.get('field_prefix', 'SYNC')
        for fid in self.fork_ids:
            setattr(self.elem, '{0}{1}'.format(fld_prefix, fid), init_bit)

    def enable_scan(self, init_bit=1, **kws):
        """Enable scan.

        Parameters
        ----------
        init_bit : int
            Int bit to enable scan.

        Keyword Arguments
        -----------------
        field_prefix : str
            String of the field name, excluding fork id.
        """
        _LOGGER.info("Enable scan...")

        fld_prefix = kws.get('field_prefix', 'ENABLE_SCAN')
        for fid in self.fork_ids:
            escan_fld_name = '{0}{1}'.format(fld_prefix, fid)
            fld = self.elem.get_field(escan_fld_name)
            if fld.value != init_bit:
                fld.value = init_bit
                # wait for signal
                wait(fld.readback_pv[0], init_bit)
                assert fld.value == init_bit
            else:
                _LOGGER.info("Scan already enabled...")

    def init_motor_pos(self, outlimit_bit=1, outlimit_val=110, **kws):
        """Move out all forks until outward limit, enable movement,
        and move motor to out limit.

        Parameters
        ----------
        outlimit_bit : int
            Int bit indicating outward limit.
        outlimit_val : float
            Distance from origin to outward limit.

        Keyword Arguments
        -----------------
        field_prefix1 : str
            String of the field name for motor position setpoint,
            excluding fork id.
        field_prefix2 : str
            String of the field name for position outward limit readback,
            excluding fork id.
        """
        _LOGGER.info("Initilize motor position...")

        mpos_fld_prefix = kws.get('field_prefix1', 'MOTOR_POS')
        outlimit_fld_prefix = kws.get('field_prefix2', 'OUT_LIMIT')
        for fid in self.fork_ids:
            setattr(self.elem, '{0}{1}'.format(mpos_fld_prefix, fid),
                    outlimit_val)
            outlimit_fld_name = '{0}{1}'.format(outlimit_fld_prefix, fid)
            outlimit_fld = self.elem.get_field(outlimit_fld_name)
            if outlimit_fld.value != outlimit_bit:
                # wait until outlimit reached
                wait(outlimit_fld.readback_pv[0], outlimit_bit)
            assert outlimit_fld.value == outlimit_bit

    def reset_interlock(self, lock_off_bit=0, **kws):
        """Reset interlock signals, when all the forks are at outward limit.

        Parameters
        ----------
        lock_off_bit : int
            Int bit that interlock is off, i.e. ready to work.

        Keyword Arguments
        -----------------
        field_prefix1 : str
            String of the field name for reset interlock, only (1) field.
        field_prefix2 : str
            String of the field name for interlock, excluding fork id.
        """
        if self.dtype != 'large': # only for large type PM.
            return

        _LOGGER.info("Reseting interlock...")

        self.init_motor_pos()

        fld_itlk_prefix = kws.get('field_prefix2', 'INTERLOCK')

        loop_out = False
        while not loop_out:
            setattr(self.elem, kws.get('field_prefix1', 'RESET_ITLK'), 1)
            for fid in self.fork_ids:
                fld_name = '{0}{1}'.format(fld_itlk_prefix, fid)
                fld_itlk_status = self.elem.get_field(fld_name)
                if fld_itlk_status.value != lock_off_bit:
                    wait(fld.readback_pv[0], lock_off_bit)
                try:
                    assert fld_itlk_status.value == lock_off_bit
                    loop_out = True
                except assertionError:
                    _LOGGER.warning("Try to reset interlock again..")

    def set_scan_range(self, start=None, stop=None, **kws):
        """Set up fork scan range, from *start* to *stop* pos, the position
        values will be read from ``dconf`` if not defined.

        Parameters
        ----------
        start : list[float]
            Start positions for all forks.
        stop : list[float]
            Stop positions for all forks.

        Keyword Arguments
        -----------------
        field_prefix1 : str
            String of the field name for start pos, excluding fork id.
        field_prefix2 : str
            String of the field name for stop pos, excluding fork id.
        """
        _LOGGER.info("Configure scan range...")

        start = self.scan_start_pos if start is None else start
        stop = self.scan_stop_pos if stop is None else stop

        start_fld_prefix = kws.get('field_prefix1', 'START_POS')
        stop_fld_prefix = kws.get('field_prefix2', 'STOP_POS')

        for fid, vstart, vstop in zip(self.fork_ids, start, stop):
            setattr(self.elem, '{0}{1}'.format(
                start_fld_prefix, fid), vstart)
            setattr(self.elem, '{0}{1}'.format(
                stop_fld_prefix, fid), vstop)

    def set_bias_volt(self):
        """Apply bias voltage.
        """
        _LOGGER.info("Set bias voltage...[void]")

    def move(self, enable_bit=1, **kws):
        """Move the forks.

        Parameters
        ----------
        enable_bit : int
            Int bit to start moving.

        Keyword Arguments
        -----------------
        field_prefix1 : str
            String of the field name for start btn, excluding fork id.
        field_prefix2 : str
            String of the field name for scan status, excluding fork id.

        Note
        ----
        When one folk is moving, the interlock of this moving folk is off (red),
        the other folk is disabled (while the interlock is on (green)).
        """
        sbtn_fld_prefix = kws.get('field_prefix1', 'START_SCAN')
        sstatus_fld_prefix = kws.get('field_prefix2', 'SCAN_STATUS')
        for fid in self.fork_ids:
            sbtn_fld_name = '{0}{1}'.format(sbtn_fld_prefix, fid)
            setattr(self.elem, sbtn_fld_name, enable_bit)

            # wait until scan finished, ready for next scan
            sstatus_fld_name = '{0}{1}'.format(sstatus_fld_prefix, fid)
            fld_sstatus = self.elem.get_field(sstatus_fld_name)
            if fld_sstatus.value != "Ready":
                # wait ready signal for next scan
                wait(fld_sstatus.readback_pv[0], "Ready")

            # enable scan
            self.enable_scan()
            # reset motors to outlimits
            self.init_motor_pos()
            # reset interlock
            self.reset_interlock()
