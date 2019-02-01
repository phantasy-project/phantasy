# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant

import numpy as np

from phantasy import get_orm


class OrmRunner(QObject):
    finished = pyqtSignal()
    resultsReady = pyqtSignal(QVariant)  # np.ndarray
    """Worker for ORM measurement.

    Parameters
    ----------
    """
    def __init__(self, params):
        super(self.__class__, self).__init__()
        (bpms, cors), (source, srange, cor_field, xoy, wait) = params

        self._bpms = bpms
        self._cors = cors
        self._source = source
        self._srange = srange
        self._cor_field = cor_field
        self._xoy = xoy
        self._wait= wait

    def run(self):
        m = get_orm(self._cors, self._bpms,
                    source=self._source, scan=self._srange,
                    cor_field=self._cor_field, xoy=self._xoy,
                    wait=self._wait)
        self.resultsReady.emit(m)
        self.finished.emit()

