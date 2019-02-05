# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant

import numpy as np
from threading import Thread

try:
    from queue import Queue
except:
    from Queue import Queue

from phantasy import get_orm


class OrmWorker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    # orm or True/None
    resultsReady = pyqtSignal(QVariant)

    # percentage, name of corrector
    update_progress = pyqtSignal(float, 'QString')

    def __init__(self, params, mode="measure"):
        # mode: 'measure' or 'apply'
        super(self.__class__, self).__init__()
        self._mode = mode
        if mode == 'measure':
            (bpms, cors), (source, srange, cor_field, xoy, wait) = params
            self._source = source
            self._cor_field = cor_field
            self._srange = srange
        else:
            (lat,), (bpms, cors), (xoy, dfac, niter, wait) = params
            self._lat = lat
            self._dfac = dfac
            self._niter = niter

        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy
        self._wait= wait

    def run(self):
        self.started.emit()
        q = Queue(0)
        self.message_receiver(q)
        if self._mode == 'measure':
            m = get_orm(self._cors, self._bpms,
                        source=self._source, scan=self._srange,
                        cor_field=self._cor_field, xoy=self._xoy,
                        wait=self._wait,
                        msg_queue=q)
        else:
            m = self._lat.correct_orbit(
                    self._cors, self._bpms,
                    xoy=self._xoy,
                    damping_factor=self._dfac,
                    iteration=self._niter, wait=self._wait,
                    msg_queue=q, mode="non-interactive")
        q.join()
        self.resultsReady.emit(m)
        self.finished.emit()

    def message_receiver(self, q):
        """Message receiver and processor from the message queue *q*.
        """
        def _receiver(q):
            while True:
                per, msg = q.get()
                self.update_progress.emit(per, msg)
                q.task_done()

        receiver = Thread(target=_receiver, args=(q,))
        receiver.setDaemon(True)
        receiver.start()
