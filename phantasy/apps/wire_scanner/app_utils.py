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
        ret1, ret2, ret3, \
        xyuv_c, xyuv_r, \
        xy_cor = self.ws_data.analyze()
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

        self.resultsReady.emit(ret)
        self.finished.emit()

