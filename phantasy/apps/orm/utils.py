# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant

import getpass
import numpy as np
import time
from collections import OrderedDict
from threading import Thread

try:
    from queue import Queue
except:
    from Queue import Queue

from phantasy import epoch2human
from phantasy import get_orm
from phantasy import MachinePortal
from phantasy.apps.correlation_visualizer.data import JSONDataSheet

TS_FMT = "%Y-%m-%d %H:%M:%S"


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
            self._srange = srange
        else:  # apply
            (lat,), (bpms, cors), (xoy, cor_field, dfac, niter, wait, l_limit, u_limit) = params
            self._lat = lat
            self._dfac = dfac
            self._niter = niter
            self._lower_limit = l_limit
            self._upper_limit = u_limit

        self._cor_field = cor_field
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
            s = self._lat.get_settings_from_orm(
                    self._cors, self._bpms,
                    cor_field=self._cor_field,
                    cor_min=self._lower_limit,
                    cor_max=self._upper_limit,
                    damping_factor=self._dfac)
            print_settings(s)
            con = input("Continue? [Y/N]")
            if con.upper() == 'Y':
                m = self._lat.apply_settings_from_orm(s,
                        iteration=self._niter, wait=self._wait,
                        cor_min=self._lower_limit,
                        cor_max=self._upper_limit,
                        msg_queue=q, mode='non-interactive')
#            m = self._lat.correct_orbit(
#                    self._cors, self._bpms,
#                    cor_field=self._cor_field,
#                    xoy=self._xoy,
#                    damping_factor=self._dfac,
#                    iteration=self._niter, wait=self._wait,
#                    cor_min=self._lower_limit, cor_max=self._upper_limit,
#                    msg_queue=q, mode="non-interactive")
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


def load_orm_sheet(filepath):
    """Load saved ORM configuration from *filepath*.
    """
    data_sheet = ORMDataSheet(filepath)
    machine, segment = data_sheet['machine'], data_sheet['segment']
    bpms_dict = data_sheet['monitors']
    cors_dict = data_sheet['correctors']
    cor_field = data_sheet.get('corrector_field', 'I')
    bpm_field = data_sheet.get('monitor_field', 'X&Y')
    mp = MachinePortal(machine, segment)
    name_elem_map = {i.name: i for i in mp.work_lattice_conf}
    orm = np.asarray(data_sheet['orm'], dtype=np.float)
    #
    print("Loading {} of {}".format(segment, machine))
    #
    return mp, name_elem_map, bpms_dict, cors_dict, orm, cor_field, bpm_field


class ORMDataSheet(JSONDataSheet):
    def __init__(self, path=None):
        super(self.__class__, self).__init__(path)

        if path is None:
            d = OrderedDict()
            d['user'] = getpass.getuser()
            d['created'] = epoch2human(time.time(), fmt=TS_FMT)
            d['monitors'] = {}
            d['correctors'] = {}
            d['machine'] = ''
            d['segment'] = ''
            d['orm'] = []
            self.update(d)


def print_settings(settings):
    # print settings
    for i, (c, f, v, v_limited) in enumerate(settings):
        print("[{cid}]: {name} [{f}] from {current:.6g} to {goal:.6g} (limited to {lg:.6g})".format(
            cid=i, name=c.name, f=f, current=getattr(c, f), goal=v, lg=v_limited))
