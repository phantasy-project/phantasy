#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal

from phantasy.recipes import get_devices_by_type


class DeviceLoader(QObject):
    # true: successful, false: failed to load lattice
    finished = pyqtSignal(bool)
    results_ready = pyqtSignal(QVariant, QVariant)

    def __init__(self, machine, segments, dtype, parent=None):
        super(DeviceLoader, self).__init__(parent)
        self._parent = parent
        self._mach = machine
        self._segs = segments
        self._dtype = dtype

    def run(self):
        try:
            names, elems = get_devices_by_type(self._dtype, machine=self._mach,
                                           segments=self._segs)
        except:
            self.results_ready.emit(None, None)
        else:
            self.results_ready.emit(names, elems)
        finally:
            self.finished.emit(True)
