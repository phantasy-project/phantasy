import epics
from numpy import ndarray
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class SimDevice(QObject):
    data_changed = pyqtSignal(ndarray)
    def __init__(self, pvname):
        super(self.__class__, self).__init__()

        self._pv = epics.PV(pvname, auto_monitor=True)
        self._cid = self._pv.add_callback(self.on_update)

    def on_update(self, value, **kws):
        self.data_changed.emit(value)

    def start(self, start_pv):
        epics.caput(start_pv, 1)

    def reset_data_cb(self):
        self._pv.remove_callback(self._cid)

