#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant

from collections import OrderedDict
from phantasy.apps.correlation_visualizer.data import JSONDataSheet

from phantasy import epoch2human

# test only
from phantasy import MachinePortal
from phantasy.apps.wire_scanner.device import Device
from phantasy.apps.wire_scanner.device import PMData
#

TS_FMT = "%Y-%m-%d %H:%M:%S"


class ScanTask(object):
    """Class to abstract scan routine.
    """

    def __init__(self, name):
        # task name identifier
        self.name = name

        # start timestamp
        self._ts_start = None
        # stop timestamp
        self._ts_stop = None

        # element to scan
        self._alter_elem = None

        # element to monitor (main)
        self._monitor_elem = None

        # additional monitors
        self._extra_monitor_elem = []

        # scan start value
        self._alter_start = 0
        # scan stop value
        self._alter_stop = 1
        # number of scan point
        self._alter_number = 10
        # shot/iter
        self._shotnum = 5

        # wait in sec
        self._wait_sec = 1.0

        # daq rate
        self._daq_rate = 1.0

        # initialize out data
        self.init_out_data()
        # set alter array
        self.set_alter_array()

    @property
    def name(self):
        """str: Name of scan task.
        """
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    @property
    def ts_start(self):
        """float: Timestamp of when task starts, epoch sec.
        """
        return self._ts_start

    @ts_start.setter
    def ts_start(self, t):
        self._ts_start = t

    @property
    def ts_stop(self):
        """float: Timestamp of when task stops, epoch sec.
        """
        return self._ts_stop

    @ts_stop.setter
    def ts_stop(self, t):
        self._ts_stop = t

    @property
    def alter_element(self):
        """obj: Element object to alter.
        """
        return self._alter_elem

    @alter_element.setter
    def alter_element(self, o):
        self._alter_elem = o
        self.set_initial_setting()

    @property
    def monitor_element(self):
        """obj: Element object to monitor.
        """
        return self._monitor_elem

    @monitor_element.setter
    def monitor_element(self, o):
        self._monitor_elem = o

    def add_extra_monitor(self, elem):
        """Add one extra monitor.
        """
        if elem in self._extra_monitor_elem:
            return
        self._extra_monitor_elem.append(elem)

    def del_extra_monitor(self, i):
        """Delete one extra monitor according to index *i*.
        """
        self._extra_monitor_elem.pop(i)

    def add_extra_monitors(self, elems):
        """Add a list of elems as extra monitors.
        """
        for elem in elems:
            if elem not in self._extra_monitor_elem:
                self._extra_monitor_elem.append(elem)

    def get_extra_monitors(self):
        """Return all extra monitor elements.
        """
        return self._extra_monitor_elem

    @property
    def alter_start(self):
        """float: Begining value where scan starts.
        """
        return self._alter_start

    @alter_start.setter
    def alter_start(self, x):
        self._alter_start = x
        self.set_alter_array()

    @property
    def alter_stop(self):
        """float: Ending value where scan stops.
        """
        return self._alter_stop

    @alter_stop.setter
    def alter_stop(self, x):
        self._alter_stop = x
        self.set_alter_array()

    @property
    def alter_number(self):
        """int: Total number of points of scan routine,
        one point is one iteration.
        """
        return self._alter_number

    @alter_number.setter
    def alter_number(self, n):
        self._alter_number = n
        self.set_alter_array()

    @property
    def shotnum(self):
        """int: Total number of DAQ event within each iteration.
        """
        return self._shotnum

    @shotnum.setter
    def shotnum(self, n):
        self._shotnum = n

    @property
    def t_wait(self):
        """float: Additional wait time in second after each set point.
        """
        return self._wait_sec

    @t_wait.setter
    def t_wait(self, s):
        self._wait_sec = s

    @property
    def daq_rate(self):
        """float: DAQ rate in Hz of fetching monitor values.
        """
        return self._daq_rate

    @daq_rate.setter
    def daq_rate(self, x):
        self._daq_rate = x

    def get_alter_array(self):
        return self._alter_array

    def set_alter_array(self, array=None):
        """Set up the value array for alter elem scan.
        if *array* is defined, use passed *array*.
        """
        if array is not None:
            self._alter_array = np.array(array)
            # update new start, stop and number
            self._alter_start = array[0]
            self._alter_stop = array[-1]
            self._alter_number = self._alter_array.size
        else:
            v1, v2, n = self.alter_start, self.alter_stop, self.alter_number
            self._alter_array = np.linspace(v1, v2, n)

    def init_out_data(self):
        """Initialize array for scan output data.
        """
        ndim = 2 + len(self.get_extra_monitors())
        self._scan_out_per_iter = np.zeros((self.shotnum, ndim))
        self._scan_out_all = np.asarray([
                                            [np.ones(
                                                ndim) * np.nan] * self.shotnum
                                        ] * self.alter_number)

    @property
    def scan_out_data_per_iter(self):
        return self._scan_out_per_iter

    @property
    def scan_out_data(self):
        return self._scan_out_all

    def __repr__(self):
        return "Scan Task: {name}\nAlter array: {array}".format(
            name=self.name,
            array=str(self.get_alter_array()),
        )

    def is_valid(self):
        """Check scan task, if valid return True, otherwise return False.
        """
        try:
            if not self.alter_element.connected:
                return False
            if not self.monitor_element.connected:
                return False
            return True
        except:
            return False

    def set_initial_setting(self):
        """Set initial setting for alter element.
        Every time set alter element, set initial setting.
        """
        x0 = self.alter_element.setpoint_pv[0].get()
        self._val0 = x0

    def get_initial_setting(self):
        """Return the initial setting of alter element.
        """
        return self._val0

    def to_datasheet(self):
        """return JSONDataSheet object.
        """
        data_sheet = JSONDataSheet()
        # task
        task_dict = OrderedDict()
        task_dict['start'] = epoch2human(self.ts_start, fmt=TS_FMT)
        task_dict['stop'] = epoch2human(self.ts_stop, fmt=TS_FMT)
        task_dict['duration'] = self.ts_stop - self.ts_start
        task_dict['n_iteration'] = self.alter_number
        task_dict['n_shot'] = self.shotnum
        task_dict['n_dim'] = 2 + len(self.get_extra_monitors())
        task_dict['scan_range'] = self.get_alter_array().tolist()
        task_dict['t_wait'] = self.t_wait
        task_dict['daq_rate'] = self.daq_rate
        data_sheet.update({'task': task_dict})

        # devices
        dev_dict = OrderedDict()
        dev_dict['alter_element'] = {
            'name': self.alter_element.ename,
            'field': self.alter_element.name,
            'readback_pv': self.alter_element.get_pv_name('readback'),
            'setpoint_pv': self.alter_element.get_pv_name('setpoint'),
        }
        dev_dict['monitors'] = []
        for elem in [self.monitor_element] + self.get_extra_monitors():
            dev_dict['monitors'].append({
                'name': elem.ename,
                'field': elem.name,
                'readback_pv': elem.get_pv_name('readback'),
            })
        data_sheet.update({'devices': dev_dict})

        # data
        data_dict = OrderedDict()
        data_dict['created'] = epoch2human(time.time(), fmt=TS_FMT)
        data_dict['shape'] = self.scan_out_data.shape
        data_dict['array'] = self.scan_out_data.tolist()
        data_sheet.update({'data': data_dict})

        return data_sheet


class ScanWorker(QObject):
    """Perform scan routine.

    Parameters
    ----------
    scantask :
        `ScanTask` instance, describe scan.
    starting_index : int
        Starting index of scan routine.
    index_array : list
        List of indices of scan, if defined, overrides *starting_index*.
    """
    # the whole scan routine is done
    scanFinished = pyqtSignal()
    # scan routine is stopped by STOP btn
    scanStopped = pyqtSignal()
    # scan routine is paused by PAUSE btn
    scanPaused = pyqtSignal()
    scanPausedAtIndex = pyqtSignal(int)
    # one iteration is done, param: index and value, array
    scanOneIterFinished = pyqtSignal(int, float, QVariant)
    # scan is done, param: scan out data array
    scanAllDataReady = pyqtSignal(QVariant)

    def __init__(self, scantask, starting_index=0, index_array=None,
                 parent=None):
        super(ScanWorker, self).__init__(parent)
        self.task = scantask
        self.parent = parent
        self.run_flag = True
        self.pause_flag = False
        self.starting_index = starting_index
        self.index_array = index_array

    def run(self):
        # enames of wire-scanners that have been processed

        nshot = self.task.shotnum
        alter_array = self.task.get_alter_array()
        alter_elem = self.task.alter_element
        monitor_elem = self.task.monitor_element
        extra_monitors = self.task.get_extra_monitors()
        all_monitors = [alter_elem, monitor_elem] + extra_monitors
        out_data = self.task.scan_out_data
        tmp_data = self.task.scan_out_data_per_iter
        wait_sec = self.task.t_wait
        daq_rate = self.task.daq_rate
        daq_delt = 1.0 / daq_rate

        index_array = range(self.starting_index, alter_array.size)

        # override index_array if arbitary index array is defined
        # could be activated by RETAKE
        if self.index_array is not None:
            index_array = self.index_array

        for idx, x in enumerate(alter_array):

            self._processed_ws = []

            if idx not in index_array:
                continue

            if not self.run_flag:
                print("Break scan by STOP button")
                self.scanStopped.emit()
                break

            if self.pause_flag:
                # save current idx, resume at this idx
                print("Break scan by PAUSE button")
                self.scanPaused.emit()
                self.scanPausedAtIndex.emit(idx)
                break

            alter_elem.value = x
            time.sleep(wait_sec)
            # DAQ
            for i in range(nshot):
                #tmp_data[i, :] = [elem.value for elem in all_monitors]
                tmp_data[i, :] = self.get_readings(i, all_monitors)
                time.sleep(daq_delt)
            out_data[idx, :, :] = tmp_data
            self.scanOneIterFinished.emit(idx, x, out_data)

        if idx == alter_array.size - 1:
            self.scanAllDataReady.emit(out_data)
            self.scanFinished.emit()
        #
        self.run_flag = False

    def get_readings(self, i, all_elements):
        # all_elements: list of PVElement/Readonly, or CaField
        readings = []
        for elem in all_elements:
            ename = elem.ename
            if 'PM' in ename and 'BPM' not in ename:
                self.process_ws(ename)
            readings.append(elem.value)
        return readings

    def stop(self):
        """Stop scan worker
        """
        self.run_flag = False

    def pause(self):
        """Pause scan worker
        """
        self.pause_flag = True

    def is_running(self):
        """Return if scan task is running or not.
        """
        return self.run_flag

    def process_ws(self, ename, machine="FRIB", segment="LEBT"):
        if ename in self._processed_ws:
            return
        print("Processing", ename)

        if "MEBT" in ename: segment = "MEBT"

        mp = MachinePortal(machine, segment)

        # process wire-scanner
        elem = mp.get_elements(name=ename)[0]

        ws = Device(elem)
        # online
        print("Run device...")
        ws.run_all()

        print("Sync data...")
        ws.sync_data(mode='live')

        # offline
        # ws.sync_data(mode='file', filename=fn)

        print("Analyzing data...")
        ws_data = PMData(ws)
        ws_data.analyze()

        print("Sync results to device...")
        ws_data.sync_results_to_ioc()

        # put processed flag
        self._processed_ws.append(ename)


if __name__ == '__main__':
    task = ScanTask("SCAN #1")
    print(task)

    task.alter_start = 0
    task.alter_stop = 10
    task.alter_number = 10
    print(task.get_alter_array(), task.alter_step)

    task.alter_stop = -10
    print(task.get_alter_array())

    task.alter_number = 5
    print(task.get_alter_array())

    task.alter_start = 10
    print(task.get_alter_array())

    task.set_alter_array([1, 3, 4, 5])
    print(task.get_alter_array())
    print(task.alter_start, task.alter_stop, task.alter_number, task.alter_step)
