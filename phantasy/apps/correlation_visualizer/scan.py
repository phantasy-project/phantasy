#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant


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
            self.alter_start = array[0]
            self.alter_stop = array[-1]
            self.alter_number = self._alter_array.size
        else:
            v1, v2, n = self.alter_start, self.alter_stop, self.alter_number
            self._alter_array = np.linspace(v1, v2, n)

    def init_out_data(self):
        """Initialize array for scan output data.
        """
        ndim = 2 + len(self.get_extra_monitors())
        self._scan_out_per_iter = np.zeros((self.shotnum, ndim))
        self._scan_out_all = np.asarray([
            [np.ones(ndim) * np.nan] * self.shotnum
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

    def get_initial_setting(self):
        try:
            x0 = self.alter_element.setpoint_pv[0].get()
        except:
            print("Cannot get initial setting.")
            x0 = None
        finally:
            self.val0 = x0
            return x0


class ScanWorker(QThread):
    """Perform scan routine.
    """
    # the whole scan routine is done
    scanAllFinished = pyqtSignal()
    # one iteration is done, param: index and value, array
    scanOneIterFinished = pyqtSignal(int, float, QVariant)
    # scan is done, param: scan out data array
    scanAllDataReady = pyqtSignal(QVariant)

    def __init__(self, scantask, parent=None):
        super(ScanWorker, self).__init__(parent)
        self.task = scantask
        self.parent = parent

    def run(self):
        nshot = self.task.shotnum
        alter_array = self.task.get_alter_array()
        alter_elem = self.task.alter_element
        monitor_elem = self.task.monitor_element
        out_data = self.task.scan_out_data
        tmp_data = self.task.scan_out_data_per_iter
        wait_sec = self.task.t_wait
        daq_rate = self.task.daq_rate
        daq_delt = 1.0/daq_rate

        for idx, x in enumerate(alter_array):
            print(idx,x)
            alter_elem.value = x
            print('waiting {} sec'.format(wait_sec))
            time.sleep(wait_sec)
            # DAQ
            for i in range(nshot):
                tmp_data[i, :] = alter_elem.value, monitor_elem.value
                time.sleep(daq_delt)
                print('\twaiting {} sec'.format(daq_delt))

            out_data[idx,:,:] = tmp_data
            self.scanOneIterFinished.emit(idx, x, out_data)

        self.scanAllDataReady.emit(out_data)
        self.scanAllFinished.emit()


if __name__ == '__main__':
    task = ScanTask("SCAN #1")
    print(task)

    task.alter_start = 0
    task.alter_stop = 10
    task.alter_number = 10
    print(task.get_alter_array())

    task.alter_stop = -10
    print(task.get_alter_array())

    task.alter_number = 5
    print(task.get_alter_array())

    task.alter_start = 10
    print(task.get_alter_array())

    task.set_alter_array([1,3,4,5])
    print(task.get_alter_array())
    print(task.alter_start, task.alter_stop, task.alter_number)
