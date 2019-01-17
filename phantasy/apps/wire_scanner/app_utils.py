#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

import numpy as np
import time


class DeviceRunner(QObject):
    finished = pyqtSignal()
    update_progress = pyqtSignal(float, 'QString')
    results = pyqtSignal(dict)
    sync_data = pyqtSignal()
    """Run wire-scanner device by executing prefined function one by one.

    Parameters
    ----------
    func_list : list
        List of functions to execute.
    device : Device
        Device object.
    mode : str
        Run simulated mode if "simulation", or work with real device.
    """

    def __init__(self, func_list, device, mode="simulation"):
        super(DeviceRunner, self).__init__()
        self.count = 0
        self.simu = mode == 'simulation'
        self.run_flag = True

        # function to execute one by one
        self.device = device
        self.func = func_list
        self.func_length = len(self.func)

        # if emit sync_data after finished
        self._post_sync = np.any([f.__name__ == 'move' for f in func_list])

    def run(self):
        while self.run_flag and self.count < self.func_length:
            f = self.func[self.count]
            self.update_progress.emit(
                    float(self.count)/self.func_length * 100,
                    f.__name__)
            if self.simu:
                print(f.__name__)
                time.sleep(2)
            else:
                print("-" * 40)
                print("'{}' is running...".format(f.__name__))
                print("-" * 40 + "\n")
                f()
            self.count += 1
        self.send_results()
        self.finished.emit()
        if self._post_sync:
            self.sync_data.emit()

    def stop(self):
        self.run_flag = False
        # add routine to force stop device?

    def send_results(self):
        results = {'status': 'ok'}
        self.results.emit(results)


class DataAnalyzer(QObject):
    finished = pyqtSignal()
    resultsReady = pyqtSignal(dict)
    """Data analysis for PM data.

    Parameters
    ----------
    ws_data : PMData
        Object of PMData instance.
    """
    def __init__(self, ws_data):
        super(DataAnalyzer, self).__init__()
        self.ws_data = ws_data

    def run(self):
        try:
            ret = self.ws_data.analyze()
        except:
            print("Processing data ERROR...")
            self.resultsReady.emit({})
        else:
            self.resultsReady.emit(ret)
        finally:
            self.finished.emit()

