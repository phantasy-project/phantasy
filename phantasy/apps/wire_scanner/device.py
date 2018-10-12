#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class built upon a collection of CaField(s) attached to PM element.
"""
import os
import logging

from phantasy import Configuration

from .utils import wait

_LOGGER = logging.getLogger(__name__)

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
        if os.path.isfile(dconf):
            self.dconf = Configuration(dconf)
        elif isinstance(dconf, Configuration):
            self.dconf = dconf
        else:
            _LOGGER.error("Cannot find device configuration.")

        # name
        self.name = name = elem.name

        # fork ids
        self._fork_ids = tuple()

        # device type, see .ini file
        self.dtype = dconf[name].get('type')

        # scan range
        self.scan_start_pos = dconf[name].getarray('start_pos_val')
        self.scan_stop_pos = dconf[name].getarray('stop_pos_val')

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
            setattr(self.elem, init_bit)
            # wait for signal
            wait(self.elem.get_field(escan_fld_name).readback_pv[0], 1)

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
            # block while motor is moving
            outlimit_fld_name = '{0}{1}'.format(outlimit_fld_prefix, fid)
            wait(self.elem.get_field(outlimit_fld_name).readback_pv[0], 1)
            assert getattr(self.elem, outlimit_fld_name) == outlimit_bit

    def reset_interlock(self, lock_off_bit=0, **kws):
        """Reset interlock signals.

        Parameters
        ----------
        lock_off_bit : int
            Int bit that interlock is off.

        Keyword Arguments
        -----------------
        field_prefix1 : str
            String of the field name for reset interlock, only (1) field.
        field_prefix2 : str
            String of the field name for interlock, excluding fork id.
        """
        if self.dtype != 'large': # only for large type PM.
            return

        self.init_motor_pos()

        fld_itlk_prefix = kws.get('field_prefix2', 'INTERLOCK')
        setattr(self.elem, kws.get('field_prefix1', 'RESET_ITLK'), 1)
        for fid in self.fork_ids:
            assert getattr(self.elem, '{0}{1}'.format(
                fld_itlk_prefix, fid)) == lock_off_bit

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
        """
        sbtn_fld_prefix = kws.get('field_prefix1', 'START_SCAN')
        sstatus_fld_prefix = kws.get('field_prefix2', 'SCAN_STATUS')
        for fid in self.fork_ids:
            sbtn_fld_name = '{0}{1}'.format(sbtn_fld_prefix, fid)
            setattr(self.elem, sbtn_fld_name, enable_bit)

            # wait until scan finished, ready for next scan
            sstatus_fld_name = '{0}{1}'.format(sstatus_fld_prefix, fid)
            wait(self.elem.get_field(sstatus_fld_name).readback_pv[0], "Ready")

