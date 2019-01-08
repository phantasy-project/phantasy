#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

import time


class DeviceRunner(QObject):
    finished = pyqtSignal()
    update_progress = pyqtSignal(float, 'QString')
    results = pyqtSignal(dict)
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
                f()
            self.count += 1
        self.send_results()
        self.finished.emit()

    def stop(self):
        self.run_flag = False

    def send_results(self):
        results = {'status': 'ok'}
        self.results.emit(results)

