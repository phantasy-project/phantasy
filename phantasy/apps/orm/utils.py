# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QBrush, QColor

import getpass
import numpy as np
import time
from collections import OrderedDict
from threading import Thread
from functools import partial

try:
    from queue import Queue
except:
    from Queue import Queue

from phantasy import epoch2human
from phantasy import get_orm_for_one_corrector
from phantasy import get_orm
from phantasy import MachinePortal
from phantasy.apps.correlation_visualizer.data import JSONDataSheet

TS_FMT = "%Y-%m-%d %H:%M:%S"

CP = ['#EF2929', '#CC0000', '#A40000']
CN = ['#8AE234', '#73D216', '#4E9A06']


class OrmWorker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    stopped = pyqtSignal()

    # orm or True/None
    resultsReady = pyqtSignal(QVariant)

    # percentage, name of corrector
    update_progress = pyqtSignal(float, 'QString')

    def __init__(self, params, mode="measure"):
        # mode: 'measure' or 'apply'
        super(self.__class__, self).__init__()
        self._mode = mode
        if mode == 'measure':
            (bpms, cors), (source, srange, cor_field, xoy, wait, ndigits), \
            (daq_rate, daq_nshot, reset_wait, keep_all_data), srange_list = params
            self._source = source
            self._srange = srange
            self._srange_list = srange_list
            self._cor_field = cor_field
            self._bpms = bpms
            self._cors = cors
            self._xoy = xoy
            self._wait= wait
            self._reset_wait = reset_wait
            self._n_digits = ndigits
            self._n_cor = len(self._cors)
            self._m_bpm = len(self._bpms)
            self._daq_rate = daq_rate
            self._daq_nshot = daq_nshot
            self._keep_all_data = keep_all_data
        else:  # apply
            lat, settings, wait, n_digits = params
            self._lat = lat
            self._settings = settings
            self._wait = wait
            self._n_cor = len(settings)
            self._n_digits = n_digits

    def run(self):
        self._run_flag = True
        self.started.emit()
        q = Queue(0)
        self.message_receiver(q)
        if self._mode == 'measure':
            m = np.zeros([self._m_bpm * len(self._xoy), self._n_cor])
            if self._keep_all_data:
                mat_data = np.zeros(
                        [self._n_cor, len(self._srange),
                         self._m_bpm * len(self._xoy)])
            else:
                mat_data = None
            for i, cor in enumerate(self._cors):
                if not self._run_flag:
                    self.stopped.emit()
                    break
                r, d = get_orm_for_one_corrector(cor, self._bpms,
                        scan=self._srange_list[i][-1], cor_field=self._cor_field,
                        xoy=self._xoy, wait=self._wait, msg_queue=q,
                        idx=i, ncor=self._n_cor, ndigits=self._n_digits,
                        nshot=self._daq_nshot, rate=self._daq_rate,
                        reset_wait=self._reset_wait,
                        keep_all=self._keep_all_data)
                m[:, i] = r
                if self._keep_all_data:
                    mat_data[i] = d

            result = m, mat_data
        else:
            for ic, setting in enumerate(self._settings):
                if not self._run_flag:
                    self.stopped.emit()
                    break
                self._lat.apply_setting(setting,
                        wait=self._wait, idx=ic,
                        msg_queue=q, ncor=self._n_cor,
                        ndigits=self._n_digits)
            result = True

        q.join()
        self.resultsReady.emit(result)
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

    def stop(self):
        self._run_flag = False


def load_orm_sheet(filepath):
    """Load saved ORM configuration from *filepath*.
    """
    data_sheet = ORMDataSheet(filepath)
    machine, segment = data_sheet['machine'], data_sheet['segment']
    bpms_dict = data_sheet['monitors']
    cors_dict = data_sheet['correctors']

    orm_conf_sheet = data_sheet['measurement_config']
    t_wait = orm_conf_sheet.get('wait_seconds', 1.0)
    reset_wait = orm_conf_sheet.get('reset_wait_seconds', 1.0)
    ndigits = orm_conf_sheet.get('set_precision', 2)
    srange = orm_conf_sheet.get('alter_range', {'from': '-5', 'to': '5', 'total_steps': '5'})
    daq_nshot = orm_conf_sheet.get('daq_nshot', 1)
    daq_rate = orm_conf_sheet.get('daq_rate', 1)
    orm = np.asarray(orm_conf_sheet['orm'], dtype=np.float)
    cor_field = orm_conf_sheet.get('corrector_field', 'I')
    bpm_field = orm_conf_sheet.get('monitor_field', 'X&Y')

    mp = MachinePortal(machine, segment)
    name_elem_map = {i.name: i for i in mp.work_lattice_conf}
    #
    print("Loading {} of {}".format(segment, machine))
    #
    orm_conf = (orm, cor_field, bpm_field, \
               t_wait, reset_wait, ndigits, srange, \
               daq_nshot, daq_rate)
    #
    cor_conf_sheet = data_sheet['correction_config']
    cor_llmt = cor_conf_sheet.get('lower_limit', -5)
    cor_ulmt = cor_conf_sheet.get('upper_limit', 5)
    cor_dfac = cor_conf_sheet.get('damping_factor', 0.5)
    cor_niter = cor_conf_sheet.get('niter', 1)
    cor_wait = cor_conf_sheet.get('wait_seconds', 1.0)
    cor_prec = cor_conf_sheet.get('set_precision', 2)
    cor_daq_rate = cor_conf_sheet.get('daq_rate', 1)
    cor_daq_nshot = cor_conf_sheet.get('daq_nshot', 1)

    cor_conf = (cor_llmt, cor_ulmt, cor_dfac, cor_niter, cor_wait, \
                cor_prec, cor_daq_rate, cor_daq_nshot)

    file_type = data_sheet['info'].get('file_type', None)

    return mp, name_elem_map, bpms_dict, cors_dict, orm_conf, cor_conf, \
           file_type


class ORMDataSheet(JSONDataSheet):
    def __init__(self, path=None):
        super(self.__class__, self).__init__(path)

        if path is None:
            d = OrderedDict()
            d['info'] = {
                    'user': getpass.getuser(),
                    'created': epoch2human(time.time(), fmt=TS_FMT)
            }
            d['monitors'] = {}
            d['correctors'] = {}
            d['machine'] = ''
            d['segment'] = ''
            d['measurement_config'] = OrderedDict()
            d['correction_config'] = OrderedDict()
            self.update(d)


class SettingsDataSheet(JSONDataSheet):
    def __init__(self, path=None):
        super(self.__class__, self).__init__(path)

        if path is None:
            d = OrderedDict()
            d['user'] = getpass.getuser()
            d['created'] = epoch2human(time.time(), fmt=TS_FMT)
            d['settings'] = {}
            d['machine'] = ''
            d['segment'] = ''
            self.update(d)


def load_settings_sheet(filepath):
    """Load settings from *filepath*, which defines SettingsDataSheet.
    """
    ds = SettingsDataSheet(filepath)
    machine, segment = ds['machine'], ds['segment']
    settings_dict = ds['settings']
    mp = MachinePortal(machine, segment)
    name_elem_map = {i.name: i for i in mp.work_lattice_conf}
    settings = []
    for ename, econf in settings_dict.items():
        settings.append(
            (name_elem_map[ename],
             econf['field'],
             econf['setpoint'],
             econf['setpoint_limited']))

    return settings, mp


class SettingsModel(QStandardItemModel):

    item_changed = pyqtSignal(QVariant)
    view_size = pyqtSignal(int, int)

    def __init__(self, parent, data, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._data = data
        self.fmt = kws.get('fmt', '{0:>.2g}')

        #
        self._pvs = []

        # header
        self.header = self.h_idx, self.h_name, self.h_field, \
                self.h_oldset, self.h_read, self.h_newset1, self.h_newset2, \
                self.h_dset, self.h_ilimit = \
                "ID", "Name", "Field", "Setpoint", \
                "Readback", "Setpoint(Raw)", "Setpoint(New)", "Diff", "Limit?"
        self.ids = self.i_idx, self.i_name, self.i_field, \
                self.i_oldset, self.i_read, self.i_newset2, self.i_newset2, \
                self.i_dset, self.i_ilimit = \
                range(len(self.header))
        #
        self.set_data()
        #
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        #
        self.item_changed.connect(self.update_item)

    def set_model(self):
        # set model
        self._v.setModel(self)
        #
        self.set_cbs()
        self.__post_init_ui(self._v)
        #

    def set_data(self):
        for i, (c, f, v, v_limited) in enumerate(self._data):
            row = []
            set0 = c.current_setting(f)
            set1 = v
            set2 = v_limited
            is_hit_limit = 'YES' if v != v_limited else 'NO'
            item_idx = QStandardItem('{0:03d}'.format(i + 1))
            item_ename = QStandardItem(c.name)
            item_fname = QStandardItem(f)
            item_set0 = QStandardItem(self.fmt.format(set0))
            item_read = QStandardItem(self.fmt.format(getattr(c, f)))
            item_set1 = QStandardItem(self.fmt.format(set1))
            item_set2 = QStandardItem(self.fmt.format(set2))
            item_ilim = QStandardItem(str(is_hit_limit))
            item_dset = QStandardItem(self.fmt.format(set2 - set0))
            if is_hit_limit == 'YES':
                item_ilim.setForeground(QBrush(QColor('#CE5C00')))
            else:
                item_ilim.setForeground(QBrush(QColor('#888A85')))
            if set2 - set0 >= 0:
                hexc = CP[0]
            else:
                hexc = CN[0]
            item_dset.setForeground(QBrush(QColor(hexc)))

            for item in (item_idx, item_ename, item_fname, item_set0, \
                         item_read, item_set1, item_set2, item_dset, item_ilim):
                item.setEditable(False)
                row.append(item)
            self.appendRow(row)

    def update_item(self, p):
        self.setItem(*p)

    def set_cbs(self):
        def _cb(row, col, fld, **kws):
            item = QStandardItem(self.fmt.format(fld.value))
            self.item_changed.emit((row, col, item))

        for i, (c, f, _, _) in enumerate(self._data):
            row, col = i, self.i_read
            fld = c.get_field(f)
            pv = fld.readback_pv[0]
            pv.add_callback(partial(_cb, row, col, fld))
            self._pvs.append(pv)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        #tv.setSortingEnabled(True)
        tv.header().setStretchLastSection(False)
        w = 0
        for i in self.ids:
            tv.resizeColumnToContents(i)
            w += tv.columnWidth(i)
        h = 0
        for i in range(len(self._data)):
            h += tv.rowHeight(self.item(i, 0).index())
        #self.sort(self.i_idx, Qt.AscendingOrder)
        #tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_size.emit(w, h)


class ScanRangeModel(QStandardItemModel):

    item_changed = pyqtSignal(QVariant)
    view_size = pyqtSignal(int, int)

    def __init__(self, parent, data, sstart, sstop, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._data = data # list of (element, field)
        self._sstart = sstart
        self._sstop = sstop
        self.fmt = kws.get('fmt', '{0:>.8g}')

        #
        self._pvs = []

        # header
        self.header = self.h_idx, self.h_name, self.h_field, \
                self.h_cset, self.h_rd, \
                self.h_sstart, self.h_sstop = \
                "ID", "Name", "Field", \
                "Setpoint", "Readback", \
                "Scan Start", "Scan Stop"

        self.ids = self.i_idx, self.i_name, self.i_field, \
                self.i_cset, self.i_rd, \
                self.i_sstart, self.i_sstop = \
                range(len(self.header))
        #
        self.set_data()
        #
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        #
        self.item_changed.connect(self.update_item)

    def set_model(self):
        # set model
        self._v.setModel(self)
        #
        self.set_cbs()
        self.__post_init_ui(self._v)
        #

    def set_data(self):
        for i, (c, f) in enumerate(self._data):
            row = []
            cset = c.current_setting(f)

            item_idx = QStandardItem('{0:03d}'.format(i + 1))
            item_ename = QStandardItem(c.name)
            item_fname = QStandardItem(f)
            item_cset = QStandardItem(self.fmt.format(cset))
            item_rd = QStandardItem(self.fmt.format(getattr(c, f)))

            item_sstart = QStandardItem(self.fmt.format(self._sstart))
            item_sstop = QStandardItem(self.fmt.format(self._sstop))

            for item in (item_idx, item_ename, item_fname, \
                         item_cset, item_rd):
                item.setEditable(False)
                row.append(item)
            row.append(item_sstart)
            row.append(item_sstop)

            self.appendRow(row)

    def update_item(self, p):
        self.setItem(*p)

    def set_cbs(self):
        def _cb(row, col, fld, **kws):
            item = QStandardItem(self.fmt.format(fld.value))
            self.item_changed.emit((row, col, item))

        for i, (c, f) in enumerate(self._data):
            row, col = i, self.i_rd
            fld = c.get_field(f)
            pv = fld.readback_pv[0]
            pv.add_callback(partial(_cb, row, col, fld))
            self._pvs.append(pv)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        #tv.setSortingEnabled(True)
        #tv.header().setStretchLastSection(False)
        #w = 0
        for i in self.ids:
            tv.resizeColumnToContents(i)
        #    w += tv.columnWidth(i)
        #h = 0
        #for i in range(len(self._data)):
        #    h += tv.rowHeight(self.item(i, 0).index())
        #self.sort(self.i_idx, Qt.AscendingOrder)
        #tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.view_size.emit(w, h)

    def get_scan_range(self, n):
        #
        # list of (ename, scan_array)
        #
        s = []
        for i in range(self.rowCount()):
            item_ename = self.item(i, self.i_name)
            item_sstart = self.item(i, self.i_sstart)
            item_sstop = self.item(i, self.i_sstop)
            x1, x2 = float(item_sstart.text()), float(item_sstop.text())
            s.append((item_ename.text(), np.linspace(x1, x2, n)))
        return s


def get_orm_with_residuals(filepath):
    """Return ORM matrix with residuals from ORMDataSheet file.
    The shape of returned matrix (m): (n, m, 2), n: size of correctors,
    m: size of BPM * 2 (if 'X&Y' is checked), for i-th corrector:
    m[i] represents the responses for all BPMs plus residuals as the
    second column.
    """
    data = ORMDataSheet(filepath)
    srange = data.get('alter_range')
    x1 = float(srange['from'])
    x2 = float(srange['to'])
    n = int(srange['total_steps'])
    scan_arr = np.linspace(x1, x2, n)
    n = len(data['correctors'])
    if data['monitor_field'] == 'X&Y':
        m1 = 2
    else:
        m1 = 1
    m = len(data['monitors']) * m1
    mat_w_residual = np.zeros([n, m, 2])
    mat_data = np.asarray(data['orm_all'])
    for i in range(len(mat_data)):
        mat_w_residual[i] = [np.polyfit(scan_arr, mat_data[i][:, k], 1) for k in range(m)]

    return np.asarray(mat_w_residual)

