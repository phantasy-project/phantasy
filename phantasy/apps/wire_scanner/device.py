#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Class built upon a collection of CaField(s) attached to PM element.
"""
import os
import time
import numpy as np
import logging
from collections import OrderedDict

from phantasy import Configuration
from phantasy import epoch2human
from phantasy.apps.correlation_visualizer.data import JSONDataSheet

from .utils import wait
from .utils import find_dconf
from .utils import get_value_with_timestamp

_LOGGER = logging.getLogger(__name__)

TS_FMT = "%Y-%m-%d %H:%M:%S"

try:
    basestring
except NameError:
    basestring = str

FORK_BIT_MAPPING = {
    'large': (
        1,
        2,
    ),
    'small': (1, ),
    'flapper': (
        1,
        2,
    ),
}

FACTOR_A2UA = 1.0 # before 2018.08, 1.0e6


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
        configuration file (.ini file). If not given, will read from
        the following locations, `~/.phantasy/ws.ini`,
        `/etc/phantasy/ws.ini` or from the package directory, see the
        loaded full path: `Device.dconf.config_path`.

    See Also
    --------
    :class:`~phantasy.CaElement`
    :class:`~phantasy.MachinePortal`
    :class:`~phantasy.Configuration`
    """

    def __init__(self, elem, dconf=None):
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

        # fork ids
        self._fork_ids = tuple()

        # device type, see .ini file
        self.dtype = self.dconf.get(name, 'type')

        # coord
        self.coord = self.dconf.get(name, 'coord')

        # scan range
        self.scan_start_pos = self.dconf.getarray(name, 'start_pos_val')
        self.scan_stop_pos = self.dconf.getarray(name, 'stop_pos_val')

        # wire offsets
        self.wire_offset = self.dconf.getarray(name, 'wire_pos_offset')

        # bias voltages
        self.bias_voltage = self.dconf.getarray(name, 'bias_voltage')

        # other misc info
        self.misc_info = self.dconf.get(name, 'info')

        # initial data sheet
        self.data_sheet = None

    @property
    def wire_offset(self):
        """list[float]: Additional offsets to all wires.
        """
        return self._wire_offset

    @wire_offset.setter
    def wire_offset(self, arr):
        self._wire_offset = [float(i) for i in arr]

    @property
    def bias_voltage(self):
        """list[float]: Bias voltages.
        """
        return self._bias_voltage

    @bias_voltage.setter
    def bias_voltage(self, arr):
        self._bias_voltage = [float(i) for i in arr]

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
        # meanwhile, configure fork_ids tuple
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
                wait(fld.readback_pv[0], init_bit, 10)
            else:
                _LOGGER.info("Scan already enabled...")

            try:
                assert fld.value == init_bit
            except AssertionError:
                self.reset_interlock()
                self.enable_scan()

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
                wait(outlimit_fld.readback_pv[0], outlimit_bit, 10)
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
        if self.dtype != 'large':  # only for large type PM.
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
                    wait(fld_itlk_status.readback_pv[0], lock_off_bit, 10)
                try:
                    assert fld_itlk_status.value == lock_off_bit
                    loop_out = True
                except AssertionError:
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
            setattr(self.elem, '{0}{1}'.format(start_fld_prefix, fid), vstart)
            setattr(self.elem, '{0}{1}'.format(stop_fld_prefix, fid), vstop)

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

            time.sleep(2.0)

            # wait until scan finished, ready for next scan
            sstatus_fld_name = '{0}{1}'.format(sstatus_fld_prefix, fid)
            fld_sstatus = self.elem.get_field(sstatus_fld_name)
            if fld_sstatus.value != 'Ready':
                # wait ready signal for next scan
                wait(fld_sstatus.readback_pv[0], "Ready", 300)

            # enable scan
            print("  Move: Enable scan")
            self.enable_scan()
            # reset motors to outlimits
            print("  Move: init motor pos")
            self.init_motor_pos()
            # reset interlock
            print("  Move: reset interlock")
            self.reset_interlock()

    def sync_data(self, mode='live', filename=None):
        """Synchronize data to device, if *mode* is 'live', read data from
        EPICS controls network thru pre-established CA; otherwise, read
        from local file, if valid *filename* is provided.

        After synchronization, the measured data could be accessed from
        properties, property names depends on device type.

        Parameters
        ----------
        mode : str
            Synchronization mode, 'live' or 'file'.
        filename : str
            Path of data file if *mode* is not 'live'.
        """
        if mode == 'live':
            self._sync_data()
        else:
            self._sync_data_from_file(filename)

    def _sync_data(self):
        # retrieve data from PVs
        if self.dtype == 'large':
            self.__sync_data_large_dtype()
        elif self.dtype == 'flapper':
            self.__sync_data_flapper_dtype()
        elif self.dtype == 'small':
            self.__sync_data_small_dtype()

    def __sync_data_to_sheet(self, k1, k2, f1, f2):
        # make data sheet from live data
        # ki: dict key names of forki data
        # fi: field names wrt ki
        ## k2 and f2 could be []

        # data sheet
        data_sheet = JSONDataSheet()
        data_sheet['data'] = {}

        # fork1
        fork1_data = OrderedDict()
        for k, fname in zip(k1, f1):
            fork1_data[k] = get_value_with_timestamp(self.elem, fname)
        data_sheet['data'].update({'fork1': fork1_data})

        if k2 != []:
            # fork2
            fork2_data = OrderedDict()
            for k, fname in zip(k2, f2):
                fork2_data[k] = get_value_with_timestamp(self.elem, fname)
            data_sheet['data'].update({'fork2': fork2_data})

        return data_sheet

    def __sync_data_large_dtype(self):
        # retrieve data from PVs for large type, fork 6in and 12in.
        k1 = ['ppot_raw', 'ppot_val1', 'offset1', 'signal1'],
        f1 = ['FORK1_PPOT_RAW', 'FORK1_PPOT_VAL1', 'FORK1_OFFSET1',
              'FORK1_SIGNAL1']
        k2 = ['ppot_raw', 'ppot_val1', 'ppot_val2', 'offset1', 'offset2',
              'signal1', 'signal2'],
        f2 = ['FORK2_PPOT_RAW', 'FORK2_PPOT_VAL1', 'FORK2_PPOT_VAL2',
              'FORK2_OFFSET1', 'FORK2_OFFSET2', 'FORK2_SIGNAL1',
              'FORK2_SIGNAL2']
        self.data_sheet = self.__sync_data_to_sheet(k1, k2, f1, f2)

    def __sync_data_flapper_dtype(self):
        # retrieve data from PVs for flapper type
        k1 = ['ppot_raw', 'ppot_val1', 'offset1', 'signal1'],
        f1 = ['FORK1_PPOT_RAW', 'FORK1_PPOT_VAL1', 'FORK1_OFFSET1',
              'FORK1_SIGNAL1']
        k2 = ['ppot_raw', 'ppot_val1', 'offset1', 'signal1'],
        f2 = ['FORK2_PPOT_RAW', 'FORK2_PPOT_VAL1', 'FORK2_OFFSET1',
              'FORK2_SIGNAL1']
        self.data_sheet = self.__sync_data_to_sheet(k1, k2, f1, f2)

    def __sync_data_small_dtype(self):
        # retrieve data from PVs for flapper type
        k1 = ['ppot_raw',
              'ppot_val1', 'ppot_val2', 'ppot_val3',
              'offset1', 'offset2', 'offset3',
              'signal1', 'signal2', 'signal3'],
        f1 = ['FORK1_PPOT_RAW',
              'FORK1_PPOT_VAL1', 'FORK1_PPOT_VAL2', 'FORK1_PPOT_VAL3',
              'FORK1_OFFSET1', 'FORK1_OFFSET2', 'FORK1_OFFSET3',
              'FORK1_SIGNAL1', 'FORK1_SIGNAL2', 'FORK1_SIGNAL3']
        k2 = f2 = []
        self.data_sheet = self.__sync_data_to_sheet(k1, k2, f1, f2)

    def _sync_data_from_file(self, filename):
        # read data from file
        self.data_sheet = JSONDataSheet(filename)

    def detail_data_sheet(self, data):
        """Detail the input data sheet *data* (dict) with device information.
        """
        if 'device' not in data:
            data['device'] = {
                'type': self.dtype,
                'coordinate': self.coord,
                'scan_start_pos': self.scan_start_pos,
                'scan_stop_pos': self.scan_stop_pos,
                'extra_offset': self.wire_offset,
                'bias_voltage': self.bias_voltage,
                'element': self.name,
            }

    def save_data(self, filename=None):
        """Save data (before analysis) into file named *filename*.

        Parameters
        ----------
        filename : str
            If not defined, device_name + timestamp + .json will be used.
        """
        self.detail_data_sheet(self.data_sheet)
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        info_dict = OrderedDict()
        info_dict['created'] = ctime
        self.data_sheet.update({'info': info_dict})

        if filename is None:
            filename = '{0}_{1}.json'.format(self.name, ctime.strip())
        self.data_sheet.write(filename)


class PMData(object):
    """PM data class for analysis, constructed with `Device` instance.

    Parameters
    ----------
    device : Device
        Instance of `Device`.
    """

    def __init__(self, device):

        # signals after noise substraction
        self._sig1_subnoise = None
        self._sig2_subnoise = None
        self._sig3_subnoise = None

        # position windows seleced for analysis
        self._pos_window1 = None
        self._pos_window2 = None
        self._pos_window3 = None

        # analyzed results after analyze()
        self._results = {}
        self._results_for_ioc = {}

        if device.data_sheet is None:
            _LOGGER.warning("Device data is not ready, try after sync_data()")
            raise RuntimeError
        else:
            self.device = device
            dtype = self.device.dtype
            data = device.data_sheet['data']
            if dtype == 'large':
                # wire on fork1: u
                # wires on fork2: v, w(x or y)
                # device.data_sheet.write("/user/zhangt/test_phantasy/data.json")
                self.raw_pos1 = np.asarray(data['fork1']['ppot_raw']['value'])
                self.raw_pos2 = np.asarray(data['fork2']['ppot_raw']['value'])
                self.signal_u = np.asarray(data['fork1']['signal1']['value'])
                self.signal_v = np.asarray(data['fork2']['signal1']['value'])
                self.signal_w = np.asarray(data['fork2']['signal2']['value'])
                self.offset_u = np.asarray(data['fork1']['offset1']['value'])
                self.offset_v = np.asarray(data['fork2']['offset1']['value'])
                self.offset_w = np.asarray(data['fork2']['offset2']['value'])
            elif dtype == 'flapper':
                self.raw_pos1 = np.asarray(data['fork1']['ppot_raw']['value'])
                self.raw_pos2 = np.asarray(data['fork2']['ppot_raw']['value'])
                self.signal_u = np.asarray(data['fork1']['signal1']['value'])
                self.signal_v = np.asarray(data['fork2']['signal1']['value'])
                self.offset_u = np.asarray(data['fork1'].get('offset1', {'value': 0})['value'])
                self.offset_v = np.asarray(data['fork2'].get('offset1', {'value': 0})['value'])
            elif dtype == 'small':
                self.raw_pos1 = np.asarray(data['fork']['ppot_raw']['value'])
                self.raw_pos2 = self.raw_pos1
                self.signal_u = np.asarray(data['fork']['signal1']['value'])
                self.signal_v = np.asarray(data['fork']['signal2']['value'])
                self.signal_w = np.asarray(data['fork']['signal3']['value'])
                self.offset_u = np.asarray(data['fork']['offset1']['value'])
                self.offset_v = np.asarray(data['fork']['offset2']['value'])
                self.offset_w = np.asarray(data['fork']['offset3']['value'])

    def get_middle_pos(self, fac, pos, signal1, signal2, offset1, offset2, th_factor=0.2, ran=None):
        """Get middle position on fork2 for large type.

        Parameters
        ----------
        pos : array
            Position.
        signal1 : array
            Wire signal array.
        signal2 : array
            Wire signal array.
        offset1 : float
            Offset of wire1.
        offset2 : float
            Offset of wire2.
        fac : float
            Projection factor.
        th_factor : float
            Threshold factor of signals to keep.
        ran : float
            If set, range is (-ran, ran).
        """
        th1, th2 = th_factor * signal1.max(), th_factor * signal2.max()
        if ran is None:
            ran = 20 if self.device.dtype == 'small' else 40
        d = []
        for pos, s1, s2 in zip(pos, signal1, signal2):
            if (s1 > th1 and -ran < pos + offset1 < ran) or \
               (s2 > th2 and -ran < pos + offset2 < ran):
                d.append([pos, s1 + s2 * fac])
        c = self.__calc_center(d)
        return c

    def analyze_wire(self,
                     pos,
                     signal0,
                     dtype,
                     mid1,
                     mid2,
                     wid,
                     coord,
                     offset,
                     norder=0):
        """Wire data analysis, return tuple of (sum, center, rms) info.

        pos: ppot_raw
        signal0: wire signal
        dtype: PM type
        mid1:
        mid2:
        wid: wire id, 0,1,2
        coord = self.device.coord  # Luvx
        offset: wire pos offset read from PV
        norder: int, noise polyfit order
        """
        # copy of orignal signal array
        signal = signal0.copy()

        # string name of wire
        wid_name = coord[wid + 1]

        # extra offset defined in config file
        extra_offset = self.device.wire_offset[wid]
        eff_offset = offset - extra_offset

        pos_adjusted = self.adjust_position(pos, wid, offset)
        # pos window for bkgd noise estimation
        pos_window = self.__get_range(pos, mid1, mid2)
        bgcoefs, bgstdv = self.__get_background_noise(pos, signal, pos_window,
                                                      norder)

        # substract background noise
        bkgd_signal = np.polyval(bgcoefs, pos)
        signal -= bkgd_signal

        signal[signal < 3.0 * bgstdv] = 0
        signal[pos < pos_window[0]] = 0
        signal[pos > pos_window[1]] = 0


        # weighted center position

        #weighted_sum = np.sum(signal)
        #weighted_center_pos0 = c0 = np.sum(signal * pos) / np.sum(signal)
        #s, avg_pos, avg_pos2 = self.__trapz_avg(signal, pos)
        s, avg_pos, avg_pos2 = self.__avg(signal, pos)
        weighted_center_pos0 = c0 = avg_pos
        weighted_sum = s

        # weighted_rms
        #weighted_rms2 = np.sum(signal * (pos - c0) **2) / np.sum(signal)
        weighted_rms2 = avg_pos2
        if weighted_rms2 > 0:
            weighted_rms = (weighted_rms2)**0.5
        else:
            weighted_rms = np.nan

        # apply offset
        if dtype != 'small' and wid_name == 'x':
            c1 = -1 * (c0 + offset)
            c = -1 * (c0 + eff_offset)
        else:
            c1 = c0 + offset
            c = c0 + eff_offset

        # beamsize with percentage ratio
        dat1 = np.vstack((pos, signal)).T
        r90p = self.__calc__percent_beamsize(dat1, s, c0, 0.9)
        r99p = self.__calc__percent_beamsize(dat1, s, c0, 0.99)

        # return dict
        ret = {
            'sum': weighted_sum * FACTOR_A2UA,
            'rms': weighted_rms,
            'center0': c0,  # wire center pos
            'center1': c1,  # c0 + offset
            'center': c,  # c0 + effective offset
            'rms90p': r90p,  # rms with 90%
            'rms99p': r99p,  # rms with 99%
        }

        return ret, pos_adjusted, signal, pos_window

    def adjust_position(self, s, wid, offset):
        """Return adjusted position to beam frame.
        """
        # effective offset to position
        extra_offset = self.device.wire_offset[wid]
        eff_offset = offset - extra_offset

        dtype = self.device.dtype
        coord = self.device.coord
        wid_name = coord[wid + 1]

        if dtype == 'large':
            if wid_name == 'x':
                xy_coef = -1.0 / np.sqrt(2.0)
            elif wid_name == 'y':
                xy_coef = 1.0 / np.sqrt(2.0)
            else:
                xy_coef = 1.0
        elif dtype == 'flapper':
            if wid_name == 'x':
                xy_coef = -1.0
            elif wid_name == 'y':
                xy_coef = 1.0
        elif dtype == 'small':
            if wid_name in ("x", "y"):
                xy_coef = 1.0 / np.sqrt(2.0)
            else:
                xy_coef = 1.0

        return (s + eff_offset) * xy_coef

    def __get_range(self, pos, mid1, mid2):
        # get pos window for analysis.
        lower, upper = mid1, mid2
        min_pos, max_pos = pos.min(), pos.max()
        if mid1 < min_pos: lower = min_pos + 1
        if mid2 > max_pos: upper = max_pos + 1
        return lower, upper

    def __get_background_noise(self, pos, signal, pos_window, norder):
        # calculate background noise with the data beyond *pos_window*
        lower, upper = pos_window
        idx_left = (pos >= lower) & (pos < lower + 3)
        idx_right = (pos > upper - 3) & (pos <= upper)
        p1s, s1s = pos[idx_left], signal[idx_left]
        p2s, s2s = pos[idx_right], signal[idx_right]

        if norder == 0:  # const
            cb1, stdv1 = 999, 999
            cb2, stdv2 = 999, 999
            if idx_left.any():
                cb1, stdv1 = s1s.mean(), s1s.std()
            if idx_right.any():
                cb2, stdv2 = s2s.mean(), s2s.std()

            if np.abs(cb1 - cb2) < 5.0 * min(stdv1, stdv2):
                n1, n2 = len(idx_left), len(idx_right)
                cb = (cb1 * n1 + cb2 * n2) / (n1 + n2)
                stdv = (stdv1 * n1 + stdv2 * n2) / (n1 + n2)
            else:
                cb, stdv = min(cb1, cb2), min(stdv1, stdv2)
            coefs = [cb]
        else:
            p12s = np.hstack([p1s, p2s])
            s12s = np.hstack([s1s, s2s])
            coefs = np.polyfit(p12s, s12s, norder)
            stdv = np.polyval(coefs, p12s).std()

        return coefs, stdv

    def __calc_center(self, dat):
        # calculate central position.
        ndat = len(dat)
        s, c = 0., 0.
        for i in range(ndat - 1):
            pos1, sig1 = dat[i + 1][0], dat[i + 1][1]
            pos2, sig2 = dat[i][0], dat[i][1]

            sig = (sig1 + sig2) / 2.
            pos = (pos1 + pos2) / 2.
            dpos = np.fabs(pos2 - pos1)

            s += sig * dpos
            c += sig * pos * dpos
        return c / s

    def __calc__percent_beamsize(self, dat, sum0, cen, ratio):
        print(sum0, cen)
        # should be refactored
        ndat = len(dat)
        #cnt = 0
        #for _,v in enumerate(dat[:,1]):
        #    if v == 0.0:
        #        continue
        #    cnt += 1
        #print(cnt)

        dxmax1 = np.fabs(dat[0][0] - cen)
        dxmax2 = np.fabs(dat[ndat - 1][0] - cen)
        dxmax = max(dxmax1, dxmax2)

        rlast = 0.0
        dxlast = 0.0
        for i in range(1, int(dxmax / 0.1)):
            dx = float(i) * 0.1
            sumt = 0.0
            for idat in range(ndat - 1):
                if dat[idat][1] == 0: continue
                sig = 0.5 * (dat[idat][1] + dat[idat + 1][1]
                             ) * np.fabs(dat[idat][0] - dat[idat + 1][0])
                pos = 0.5 * (dat[idat + 1][0] + dat[idat][0])

                if cen - 1 * dx < pos < cen + 1 * dx:
                    sumt += sig
            r = sumt / sum0

            #print str(dx)+'\t'+str(r)
            if rlast < ratio and r > ratio:
                #print r
                c1 = (dx - dxlast) / (r - rlast)
                c0 = dx - c1 * r
                dxx = c1 * ratio + c0
                _LOGGER.debug(
                    str(100 * ratio) + '% : ' + str(dx) + '\t' + str(r) +
                    '\t' + str(rlast) + '\t' + str(dxx))
                break

            rlast = r
            dxlast = dx

        return dxx

    def __smooth_array(self, x):
        # smooth array *x* by average every two consecutive points
        return 0.5 * (x[:-1] + x[1:])

    def __get_xyuv_center(self,
                          c6in,
                          c12in1,
                          c12in2,
                          coord,
                          offset=[0.0, 0.0, 0.0]):  #+ Right-hand system
        u, v, x, y = np.nan, np.nan, np.nan, np.nan
        #print offset
        #o6in = offset[0]
        #o12in1 = offset[1]
        #o12in2 = offset[2]
        if coord == "Luvx":
            u = c6in
            v = c12in1
            x1 = (u - v) / np.sqrt(2)
            x2 = (c12in2) / np.sqrt(2)
            x = (x1 + x2) / 2.
            y = (u + v) / np.sqrt(2)
            _LOGGER.debug("x1: " + str(x1) + "\tx2:" + str(x2))
            """
            u=c6in-offset[0]
            v=c12in1-offset[1]
            x1 = (u-v)/np.sqrt(2)
            x2 = (-c12in2+offset[2])/np.sqrt(2)
            x=(x1+x2)/2.
            #x=(u-v)/np.sqrt(2)
            y=(u+v)/np.sqrt(2)
            if self.debug:
                print "x1: "+str(x1)+"\tx2:"+str(x2)
                f1.write("x1: "+str(x1)+"\tx2:"+str(x2)+"\n")
            """
        elif coord == "Luvy":
            u = c6in
            v = c12in1
            x = (u - v) / np.sqrt(2)
            y1 = (u + v) / np.sqrt(2)
            y2 = (c12in2) / np.sqrt(2)
            y = (y1 + y2) / 2.
            _LOGGER.debug("y1: " + str(y1) + "\ty2: " + str(y2))
            """
            u=c6in-offset[0]
            v=c12in1-offset[1]
            x=(u-v)/np.sqrt(2)
            y1 = (u+v)/np.sqrt(2)
            y2 = (c12in2-offset[2])/np.sqrt(2)
            y = (y1+y2)/2.
            if self.debug:
                print "y1: "+str(y1)+"\ty2: "+str(y2)
                f1.write("y1: "+str(y1)+"\ty2: "+str(y2)+"\n")
                #y=(u+v)/np.sqrt(2)
            """
        elif coord == 'Suxy':
            x = (c12in1) / np.sqrt(2)
            y = (c12in2) / np.sqrt(2)
            u = c6in
            v = u - np.sqrt(2) * x
            _LOGGER.debug(
                "x1: " + str(x) + "\tx2:" + str(-1 * y + np.sqrt(2) * u))
        elif coord == "Fxy":
            '''
            x=-1*(c6in-offset[0])
            y=c12in1-offset[1]
            '''
            x = (c6in)
            y = c12in1

        return x, y, u, v

    def __get_xyuv_size(self, r6in, r12in1, r12in2, coord):
        #print coord
        #print str(r6in)+'\t'+str(r12in1)+'\t'+str(r12in2)
        u, v, x, y = np.nan, np.nan, np.nan, np.nan
        if coord == "Luvx":
            u = r6in
            v = r12in1
            x = r12in2 / np.sqrt(2)
            y = np.sqrt(u * u + v * v - x * x)
        elif coord == "Luvy":
            u = r6in
            v = r12in1
            y = r12in2 / np.sqrt(2)
            x = np.sqrt(u * u + v * v - y * y)
        elif coord == 'Suxy':
            u = r6in
            x = r12in1 / np.sqrt(2)
            y = r12in2 / np.sqrt(2)
            v = np.sqrt(x * x + y * y - u * u)
        elif coord == "Fxy":
            x = r6in
            y = r12in1
            u = np.nan
            v = np.nan
        return x, y, u, v

    def __get_cxy(self, xrms, yrms, urms, vrms):
        if min(xrms, yrms, urms, vrms) < -900.:
            cxy = np.nan
        else:
            cxy = -(vrms**2 - urms**2) / (2.0 * xrms * yrms)
        return cxy

    def analyze(self, norder=1):
        """Analyze all the data of this ws device
        """
        dtype = self.device.dtype
        coord = self.device.coord
        extra_offset = self.device.wire_offset

        if dtype == "large":
            mid = self.get_middle_pos(1.0 / np.sqrt(2.0), self.raw_pos2,
                    self.signal_v, self.signal_w, self.offset_v, self.offset_w)
            # u wire
            ret1, _, sig1_subnoise, wpos1 = self.analyze_wire(self.raw_pos1, self.signal_u, dtype, -999,
                                     999, 0, coord, self.offset_u, norder)
            # v wire
            ret2, _, sig2_subnoise, wpos2 = self.analyze_wire(self.raw_pos2, self.signal_v, dtype, mid - 10,
                                     999, 1, coord, self.offset_v, norder)
            # w wire (x/y)
            ret3, _, sig3_subnoise, wpos3 = self.analyze_wire(self.raw_pos2, self.signal_w, dtype, -999,
                                     mid + 10, 2, coord, self.offset_w, norder)

        elif dtype == "flapper":
            # u(x) wire
            ret1, _, sig1_subnoise, wpos1 = self.analyze_wire(self.raw_pos1, self.signal_u, dtype, -999,
                                     999, 0, coord, self.offset_u, norder)
            # v(y) wire
            ret2, _, sig2_subnoise, wpos2 = self.analyze_wire(self.raw_pos2, self.signal_v, dtype, -999,
                                     999, 1, coord, self.offset_v, norder)
            ret3 = {"sum": np.nan, "rms": np.nan, "center0": np.nan, "center1": np.nan,
                    "center": np.nan, "rms90p": np.nan, "rms99p": np.nan}
            sig3_subnoise = []
            wpos3 = None

        elif dtype == "small":
            mid12 = self.get_middle_pos(1.0 / np.sqrt(2.0), self.raw_pos1,
                        self.signal_u, self.signal_v, self.offset_u, self.offset_v)
            mid23 = self.get_middle_pos(1.0, self.raw_pos1,
                        self.signal_v, self.signal_w, self.offset_v, self.offset_w)
            ret1, _, sig1_subnoise, wpos1 = self.analyze_wire(self.raw_pos1, self.signal_u, dtype, mid12,
                        999, 0, coord, self.offset_u, norder)
            ret2, _, sig2_subnoise, wpos2 = self.analyze_wire(self.raw_pos1, self.signal_v, dtype, mid23,
                        mid12, 1, coord, self.offset_v, norder)
            ret3, _, sig3_subnoise, wpos3 = self.analyze_wire(self.raw_pos1, self.signal_w, dtype, -999,
                        mid23, 2, coord, self.offset_w, norder)

        # corrected centers
        xc, yc, uc, vc = self.__get_xyuv_center(
                ret1['center'], ret2['center'],
                ret3['center'], coord, extra_offset)

        # corrected rms size
        try:
            xr,yr,ur,vr = self.__get_xyuv_size(ret1['rms'],ret2['rms'],ret3['rms'],coord)
        except:
            xr,yr,ur,vr = np.nan, np.nan, np.nan, np.nan
        try:
            x90p,y90p,u90p,v90p = self.__get_xyuv_size(ret1['rms90p'],ret2['rms90p'],ret3['rms90p'],coord)
        except:
            x90p,y90p,u90p,v90p = np.nan, np.nan, np.nan, np.nan
        try:
            x99p,y99p,u99p,v99p = self.__get_xyuv_size(ret1['rms99p'],ret2['rms99p'],ret3['rms99p'],coord)
        except:
            x99p,y99p,u99p,v99p = np.nan, np.nan, np.nan, np.nan

        try:
            cxy = self.__get_cxy(xr,yr,ur,vr)
        except:
            cxy = np.nan
        try:
            cxy90p = self.__get_cxy(x90p,y90p,u90p,v90p)
        except:
            cxy90p = np.nan
        try:
            cxy99p = self.__get_cxy(x99p,y99p,u99p,v99p)
        except:
            cxy99p = np.nan

        xyuv_c = {'xc': xc, 'yc': yc, 'uc': uc, 'vc': vc}
        xyuv_r = {'rms_x': xr, 'rms_y': yr, 'rms_u': ur, 'rms_v': vr,
                  'rms90_x': x90p, 'rms90_y': y90p, 'rms90_u': u90p, 'rms90_v': v90p,
                  'rms99_x': x99p, 'rms99_y': y99p, 'rms99_u': u99p, 'rms99_v': v99p}
        xy_cor = {'cxy': cxy, 'cxy90': cxy90p, 'cxy99': cxy99p}

        ret = {
            'sum1': ret1['sum'],
            'sum2': ret2['sum'],
            'sum3': ret3['sum'],
            'cen1': ret1['center'],
            'cen2': ret2['center'],
            'cen3': ret3['center'],
            'cen01': ret1['center0'],
            'cen02': ret2['center0'],
            'cen03': ret3['center0'],
            'rms1': ret1['rms'],
            'rms2': ret2['rms'],
            'rms3': ret3['rms'],
            'r90p1': ret1['rms90p'],
            'r90p2': ret2['rms90p'],
            'r90p3': ret3['rms90p'],
            'r99p1': ret1['rms99p'],
            'r99p2': ret2['rms99p'],
            'r99p3': ret3['rms99p'],
            'xrms': xyuv_r['rms_x'] ,
            'yrms': xyuv_r['rms_y'],
            'urms': xyuv_r['rms_u'],
            'vrms': xyuv_r['rms_v'],
            'x90p': xyuv_r['rms90_x'],
            'y90p': xyuv_r['rms90_y'],
            'u90p': xyuv_r['rms90_u'],
            'v90p': xyuv_r['rms90_v'],
            'x99p': xyuv_r['rms99_x'],
            'y99p': xyuv_r['rms99_y'],
            'u99p': xyuv_r['rms99_u'],
            'v99p': xyuv_r['rms99_v'],
            'xcen': xyuv_c['xc'],
            'ycen': xyuv_c['yc'],
            'ucen': xyuv_c['uc'],
            'vcen': xyuv_c['vc'],
            'cxy': xy_cor['cxy'],
            'cxy90p': xy_cor['cxy90'],
            'cxy99p': xy_cor['cxy99'],
        }
        self._sig1_subnoise = sig1_subnoise
        self._sig2_subnoise = sig2_subnoise
        self._sig3_subnoise = sig3_subnoise
        self._pos_window1 = wpos1
        self._pos_window2 = wpos2
        self._pos_window3 = wpos3
        self._results = ret
        self._results_for_ioc = {
                'xcen': ret['xcen'], 'ycen': ret['ycen'],
                'xrms': ret['xrms'], 'yrms': ret['yrms'],
                'cxy': ret['cxy']}
        return ret

    def sync_results_to_ioc(self):
        # sync analyzed results to IOC.
        for k, v in self._results_for_ioc.items():
            setattr(self.device.elem, k.upper(), v)

    def __avg(self, y, x):
        s = abs(np.trapz(y, x))
        x_avg = np.sum(x * y) / np.sum(y)
        x2_avg = np.sum((x - x_avg) ** 2 * y) / np.sum(y)
        return s, x_avg, x2_avg

    def __trapz_avg(self, y, x):
        # trapzoid average x and x^2 (-<x>) over y
        # <x> = sum(y*x)/sum(y)
        # <x^2> = sum(y*x^2)/sum(y)
        xy = np.asarray(sorted(np.vstack([x, y]).T.tolist()))

        x1, x2 = xy[:, 0][:-1], xy[:, 0][1:]
        y1, y2 = xy[:, 1][:-1], xy[:, 1][1:]
        dx = x2 - x1
        xs = np.sum((x1 + x2) / 2.0 * dx * (y1 + y2) / 2.0)
        s = np.sum((y1 + y2) / 2.0 * dx)

        x_avg = xs / s

        x2s = np.sum(((x1 + x2) / 2.0 - x_avg)**2 * dx * (y1 + y2) / 2.0)

        return s, x_avg, x2s / s
