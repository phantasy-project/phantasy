import epics
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from numpy import ndarray


class SimDevice(QObject):
    data_changed = pyqtSignal(ndarray)
    finished = pyqtSignal()
    def __init__(self, data_pv, status_pv, trigger_pv):
        super(self.__class__, self).__init__()

        self._trigger_pv = trigger_pv
        self._status_pv = epics.PV(status_pv, auto_monitor=True)
        self._data_pv = epics.PV(data_pv, auto_monitor=True)
        self._scid = self._status_pv.add_callback(self.on_update_s)
        self._dcid = self._data_pv.add_callback(self.on_update)

    def on_update(self, value, **kws):
        self.data_changed.emit(value)

    def start(self):
        epics.caput(self._trigger_pv, 1)

    def reset_data_cb(self):
        self._data_pv.remove_callback(self._dcid)
        self._status_pv.remove_callback(self._scid)
        self.finished.emit()

    def on_update_s(self, value, **kws):
        print(kws.get('pvname'), "value is: ", value)
        if value == 12:
            self.reset_data_cb()

