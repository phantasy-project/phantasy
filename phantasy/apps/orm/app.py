#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from collections import OrderedDict
from collections import deque
from functools import partial

import numpy as np
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from phantasy_ui import BaseAppForm

from phantasy import limit_input
from phantasy.apps.trajectory_viewer.utils import ElementListModel
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import get_save_filename
from phantasy.apps.utils import uptime
from .app_settings_view import SettingsView
from .ui.ui_app import Ui_MainWindow
from .utils import ORMDataSheet
from .utils import OrmWorker
from .utils import ScanRangeModel
from .utils import SettingsDataSheet
from .utils import load_orm_sheet
from .utils import load_settings_sheet

OP_MODE_MAP = {
    'Simulation': 'model',
    'Live': 'control',
}


class OrbitResponseMatrixWindow(BaseAppForm, Ui_MainWindow):
    """Orbit reponse matrix measurement, visualization and data management.

    Parameters
    ----------
    parent :
        Paranet QObject.
    version : str
        Version number string.

    Keyword Arguments
    -----------------
    cors : dict
        Dict of correctors, key: element name, value: list of fields.
    bpms : dict
        Dict of monitors, key: element name, value: list of fields.
    name_map : dict
        Dict of element name (key) and element object (value) mapping.
    mp :
        MachinePortal object.
    """

    def __init__(self, parent, version, **kws):
        super(OrbitResponseMatrixWindow, self).__init__()
        self.parent = parent

        # name map
        self._name_map = kws.get('name_map', {})

        # mp
        self._lat = None
        self._mp = kws.get('mp', None)

        # orm
        self._orm = np.array([])
        self._orm_all_data = np.array([])

        # bpms dict
        self._bpms_dict = sort_dict(kws.get('bpms', OrderedDict()))

        # cors dict
        self._cors_dict = sort_dict(kws.get('cors', OrderedDict()))

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Trajectory Response Matrix")

        # set app properties
        self.setAppTitle("Trajectory Response Matrix")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Beam Central Trajectory Response Matrix</h4>
            <p>This app is created to measure, manage and visualize
            the response matrices for central trajectory correction,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self.post_init()

    def post_init(self):
        #
        for o in (self.rel_range_lineEdit,
                  self.lower_limit_lineEdit, self.upper_limit_lineEdit):
            o.setValidator(QDoubleValidator())
        #
        # source, mode
        self.operation_mode_cbb.currentTextChanged.connect(self.on_source_changed)
        # keep all intermediate ORM data or not
        self.keep_all_data_chkbox.toggled.connect(self.on_keep_all_data)
        # wait/reset wait sec
        self.wait_time_dsbox.valueChanged.connect(
            partial(self.on_float_changed, '_wait_sec', True))
        self.reset_wait_time_dsbox.valueChanged.connect(
            partial(self.on_float_changed, '_reset_wait_sec', True))
        # alter steps, rel.range
        self.alter_steps_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_ssteps', True))
        self.rel_range_lineEdit.returnPressed.connect(
            partial(self.on_value_changed, '_rel_range'))
        self.rel_range_lineEdit.returnPressed.connect(
            self.on_update_srange)

        # mprec
        self.mprec_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_mprec', False))
        # daq rate
        self.daq_rate_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_daq_rate', True))
        # daq nshot
        self.daq_nshot_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_daq_nshot', True))
        # set lower/upper limits
        self.lower_limit_lineEdit.returnPressed.connect(
            partial(self.on_value_changed, '_lower_limit'))
        self.upper_limit_lineEdit.returnPressed.connect(
            partial(self.on_value_changed, '_upper_limit'))
        # cor damping factor
        self.cor_damping_fac_dsbox.valueChanged.connect(
            partial(self.on_float_changed, '_cor_dfac', False))
        # cor niter
        self.cor_niter_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_cor_niter', False))
        # cor wait sec
        self.cor_wait_time_dsbox.valueChanged.connect(
            partial(self.on_float_changed, '_cor_wait_sec', False))
        # cor prec
        self.cor_prec_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_cor_prec', False))
        # cor eva daq rate
        self.eva_daq_rate_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_eva_daq_rate', False))
        # cor eva daq nshot
        self.eva_daq_nshot_sbox.valueChanged.connect(
            partial(self.on_int_changed, '_eva_daq_nshot', False))

        # update eta
        self.update_eta_btn.clicked.connect(self.on_update_eta)
        # element selection for BPMs/CORs treeview
        self.select_all_bpms_btn.clicked.connect(
            partial(self.on_select_all_elems, "bpm"))
        self.inverse_bpm_selection_btn.clicked.connect(
            partial(self.on_inverse_current_elem_selection, "bpm"))
        self.select_all_cors_btn.clicked.connect(
            partial(self.on_select_all_elems, "cor"))
        self.inverse_cor_selection_btn.clicked.connect(
            partial(self.on_inverse_current_elem_selection, "cor"))
        # batch change element field
        self.monitor_fields_cbb.currentTextChanged.connect(
            self.on_update_monitor_field)
        self.monitor_fields_cbb.currentTextChanged.connect(
            partial(self.on_elem_field_changed, "bpm"))
        self.corrector_fields_cbb.currentTextChanged.connect(
            self.on_update_corrector_field)
        self.corrector_fields_cbb.currentTextChanged.connect(
            partial(self.on_elem_field_changed, "cor"))

        # refresh element list models
        self.refresh_models_btn.clicked.connect(self.on_refresh_models)
        self.refresh_models_btn.clicked.connect(self.on_update_eta)
        self.refresh_models_btn.clicked.connect(self.on_set_srange_model)
        self.refresh_models_btn.clicked.connect(self.init_elements)

        # init params
        self.init_params()

        # init lat
        self.init_lattice()

        # init elements
        self.init_elements()

        # init settings table
        self.init_settings_table()

        # init latinfo
        self.init_latinfo()

        # init widget status
        self.init_widgets()

        # WIP
        self.init_settings_dq()

        # mach/lat info
        self.update_lattice_info()

        # init bpm/cor models, set up models for BPMs and CORs
        self.refresh_models_btn.clicked.emit()
        # init _bpm_field, _cor_field, _xoy
        self.init_fields()

    @pyqtSlot()
    def on_refresh_models(self):
        # refresh 'bpm' and 'cor' model.
        for mode in ('bpm', 'cor'):
            v = getattr(self, '_{}s_dict'.format(mode))
            tv = getattr(self, '{}s_treeView'.format(mode))
            enames = list(v.keys())
            model = ElementListModel(tv, self._mp, enames)
            model.set_model()
            model.elementSelected.connect(partial(self.on_update_selection, mode))
            o = getattr(self, 'nelem_selected_{}s_lineEdit'.format(mode))
            model.nElementSelected.connect(lambda i: o.setText(str(i)))
            model.select_all_items()  # select all by default

        try:
            self.bpms_treeView.model().nElementSelected.connect(
                lambda i: self.nelem_selected_bpms_lineEdit.setText(str(i)))
            self.cors_treeView.model().nElementSelected.connect(
                lambda i: self.nelem_selected_cors_lineEdit.setText(str(i)))
        except:
            pass

    @pyqtSlot(dict)
    def on_update_elements(self, mode, elems_dict):
        """Update monitor view with *elems_dict* for *mode*, 'bpm' or 'cor'.
        """
        print("[ORM]-{}: {}".format(mode, elems_dict))
        e_dict = sort_dict(elems_dict)
        setattr(self, '_{}s_dict'.format(mode), e_dict)

    @pyqtSlot(dict)
    def update_name_map(self, name_map):
        self._name_map.update(name_map)

    @pyqtSlot()
    def on_measure_orm(self):
        """Measure ORM.
        """
        params = self.__prepare_inputs_for_orm_measurement()
        if params is None:
            return

        self.thread = QThread()
        self.orm_runner = OrmWorker(params)
        self.orm_runner.moveToThread(self.thread)
        self.orm_runner.started.connect(
            partial(self.orm_worker_started, self.measure_pb,
                    self.stop_measure_btn, [self.run_btn]))
        self.orm_runner.started.connect(self.start_eta_timer)
        self.orm_runner.resultsReady.connect(
            partial(self.on_results_ready, 'measure'))
        self.orm_runner.update_progress.connect(
            partial(self.update_pb, self.measure_pb))
        self.orm_runner.update_progress.connect(self.hl_row)
        self.orm_runner.finished.connect(self.stop_eta_timer)
        self.orm_runner.finished.connect(
            partial(self.orm_worker_completed, self.measure_pb,
                    self.stop_measure_btn, [self.run_btn]))
        self.orm_runner.finished.connect(self.thread.quit)
        self.orm_runner.finished.connect(self.orm_runner.deleteLater)
        self.orm_runner.stopped.connect(
            partial(self.on_stop_orm_worker, "Stopped ORM Measurement..."))
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.orm_runner.run)
        self.thread.start()

    @pyqtSlot(float, 'QString')
    def hl_row(self, x, msg):
        row_id = self._pb_msg_to_index(msg)
        self.cor_srange_tableView.selectRow(row_id)

    @pyqtSlot(float, 'QString')
    def update_pb(self, pb, x, s):
        pb.setValue(x)
        pb.setFormat("%p%")
        self.log_textEdit.append(s)

    @pyqtSlot()
    def orm_worker_started(self, pb, sbtn, sender_obj):
        print("ORM worker is about to start.")
        [i.setEnabled(False) for i in sender_obj]
        pb.setVisible(True)
        sbtn.setEnabled(True)

    @pyqtSlot()
    def orm_worker_completed(self, pb, sbtn, sender_obj):
        print("ORM worker is done.")
        [i.setEnabled(True) for i in sender_obj]
        pb.setVisible(False)
        pb.setValue(0)
        sbtn.setEnabled(False)

    @pyqtSlot(QVariant)
    def on_results_ready(self, mode, result):
        if mode == 'measure':
            self._orm = result[0]
            self._orm_all_data = result[1]
            self.set_orm()
            print("ORM is ready")
        else:
            pass

    def set_orm(self):
        if self._lat is None:
            return
        self._lat.orm = self._orm

    def __prepare_inputs_for_orm_apply(self):
        #
        if self._lat.orm is None:
            return None
        #
        # debug
        print("\nTo Apply Correctors Settings...")
        print("--- Name of lattice to correct: {}/{}".format(
            self._lat.name, self._mp.last_machine_name))
        print("--- # of BPMs loaded: {}".format(len(self._bpms)))
        print("--- # of CORs loaded: {}".format(len(self._cors)))
        print("--- Field of CORs to write: {}".format(self._cor_field))
        print("--- Field of BPMs to read : {}".format(self._xoy))
        print("--- Damping factor: {}".format(self._cor_dfac))
        print("--- # of iteration: {}".format(self._cor_niter))
        print("--- Wait second after put: {}".format(self._cor_wait_sec))
        print("--- Corrector limit: [{}, {}]".format(self._lower_limit, self._upper_limit))
        print("--- DAQ rate, nshot: {}, {}".format(self._eva_daq_rate, self._eva_daq_nshot))

        return (self._lat,), (self._bpms, self._cors), \
               (self._xoy, self._cor_field, self._cor_dfac, self._cor_niter,
                self._cor_wait_sec, self._lower_limit, self._upper_limit), \
               (self._eva_daq_rate, self._eva_daq_nshot)

    def __prepare_inputs_for_orm_measurement(self):
        #
        self._srange_list = self.get_srange_list()
        # debug
        print("\nTo Measure Response Matrix...")
        print("--- Mode:", self._source)
        print("--- Alter Range: ", self._srange_list)
        print("--- Field of CORs to write: ", self._cor_field)
        print("--- Field of BPMs to read: ", self._xoy)
        print("--- Wait second after alter: ", self._wait_sec)
        print("--- Wait second after reset: ", self._reset_wait_sec)
        print("--- # of Precison Digit: ", self._mprec)
        print("--- DAQ rate, nshot: ", self._daq_rate, self._daq_nshot)
        print("--- Keep ORM data?: ", self._keep_all)
        #
        return (self._bpms, self._cors), \
               (self._source, self._srange_list, self._cor_field, self._xoy,
                self._wait_sec, self._mprec), \
               (self._daq_rate, self._daq_nshot, self._reset_wait_sec,
                self._keep_all)

    @pyqtSlot()
    def on_update_eta(self):
        ns = self._ssteps
        nc = len(self._cors_dict)
        dt = self._wait_sec
        r_dt = self._reset_wait_sec
        nshot = self._daq_nshot
        daq_rate = self._daq_rate

        eta = ns * nc * (dt + nshot * 1.0 / daq_rate) + nc * r_dt
        self.eta_lbl.setText(uptime(int(eta)))

        print("ETA Info:")
        print("--- # of alter points: ", ns)
        print("--- # of correctors: ", nc)
        print("--- Wait sec / step: ", dt)
        print("--- Reset wait sec: ", r_dt)
        print("--- DAQ # of shot: ", nshot)
        print("--- DAQ rate: ", daq_rate)
        print("--- ETA {} [s], or {}".format(eta, uptime(int(eta))))

    def __apply_with_settings(self, settings=None, **kws):
        # apply settings to correct central trajectory
        if settings is None:
            QMessageBox.warning(self, "Apply ORM",
                                "Correctors settings are not ready, click 'Evaluate' and 'Apply' again.",
                                QMessageBox.Ok)
            return

        lat = self._mp.work_lattice_conf
        t_wait = self.cor_wait_time_dsbox.value()
        cprec = self.cor_prec_sbox.value()
        params = lat, settings, t_wait, cprec
        to_cache = kws.get('to_cache', True)
        btns = kws.get('btns', [self.cor_apply_btn, self.undo_apply_btn, self.redo_apply_btn])

        self.thread1 = QThread()
        self.orm_consumer = OrmWorker(params, mode='apply')
        self.orm_consumer.moveToThread(self.thread1)
        if to_cache:
            self.orm_consumer.started.connect(partial(self.on_update_settings_dq, 'start'))
        self.orm_consumer.started.connect(
            partial(self.orm_worker_started, self.cor_apply_pb, self.stop_apply_btn, btns))
        self.orm_consumer.resultsReady.connect(partial(self.on_results_ready, 'apply'))
        self.orm_consumer.update_progress.connect(partial(self.update_pb, self.cor_apply_pb))
        self.orm_consumer.finished.connect(
            partial(self.orm_worker_completed, self.cor_apply_pb, self.stop_apply_btn, btns))
        self.orm_consumer.finished.connect(self.thread1.quit)
        self.orm_consumer.finished.connect(self.orm_consumer.deleteLater)
        if to_cache:
            self.orm_consumer.finished.connect(partial(self.on_update_settings_dq, 'finish'))
        self.orm_consumer.stopped.connect(partial(self.on_stop_orm_worker, "Stopped Correction..."))
        if to_cache:
            self.orm_consumer.stopped.connect(partial(self.on_update_settings_dq, 'stop'))
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.started.connect(self.orm_consumer.run)
        self.thread1.start()
        return self.orm_consumer

    @pyqtSlot()
    def on_apply_orm(self):
        """Apply ORM to correct orbit.
        """
        self.__apply_with_settings(settings=self._cor_settings)

    @pyqtSlot()
    def on_open_orm(self):
        filepath, ext = get_open_filename(self,
                                          filter="JSON Files (*.json)")
        if filepath is None:
            return

        try:
            mp, name_map, bpms_dict, cors_dict, \
                (orm, cor_field, bpm_field, t_wait, reset_wait, mprec, srange, daq_nshot, daq_rate), \
                (cor_llmt, cor_ulmt, cor_dfac, cor_niter, cor_wait, cor_prec, cor_daq_rate, cor_daq_nshot), \
                ftype = load_orm_sheet(filepath)
        except:
            QMessageBox.warning(self, "Loading Response Matrix",
                                "Cannot load selected file!", QMessageBox.Ok)
            return

        self._mp = mp
        self._name_map = name_map
        self._bpms_dict = bpms_dict
        self._cors_dict = cors_dict
        #
        self._orm = orm
        self.refresh_models_btn.clicked.emit()
        self.corrector_fields_cbb.setCurrentText(cor_field)
        self.monitor_fields_cbb.setCurrentText(bpm_field)
        self.wait_time_dsbox.setValue(t_wait)
        self.reset_wait_time_dsbox.setValue(reset_wait)
        self.mprec_sbox.setValue(mprec)
        self.daq_rate_sbox.setValue(daq_rate)
        self.daq_nshot_sbox.setValue(daq_nshot)
        srange_steps = srange['total_steps']
        rel_range = srange.get('relative_range', 0.1)
        self.alter_steps_sbox.setValue(srange_steps)
        self.rel_range_lineEdit.setText(str(rel_range))
        self.corrector_fields_cbb.currentTextChanged.emit(cor_field)
        self.monitor_fields_cbb.currentTextChanged.emit(bpm_field)
        #
        self.lower_limit_lineEdit.setText(str(cor_llmt))
        self.upper_limit_lineEdit.setText(str(cor_ulmt))
        self.cor_damping_fac_dsbox.setValue(cor_dfac)
        self.cor_niter_sbox.setValue(int(cor_niter))
        self.cor_wait_time_dsbox.setValue(cor_wait)
        self.cor_prec_sbox.setValue(int(cor_prec))
        self.eva_daq_nshot_sbox.setValue(int(cor_daq_nshot))
        self.eva_daq_rate_sbox.setValue(int(cor_daq_rate))

        #
        self.init_elements()

        #
        self.update_lattice_info()

        #
        self.init_settings_dq()

        #
        self.on_update_eta()

        #
        self.init_lattice()

    @pyqtSlot()
    def on_save_orm(self):
        filepath, ext = get_save_filename(self,
                                          cdir='.',
                                          filter="JSON Files (*.json)")
        if filepath is None:
            return

        machine, segment = self._mp.last_machine_name, self._mp.last_lattice_name
        bpms_dict = sort_dict(self.bpms_treeView.model()._selected_elements)
        cors_dict = sort_dict(self.cors_treeView.model()._selected_elements)

        orm = self._orm.tolist()
        data_sheet = ORMDataSheet()
        data_sheet['monitors'] = bpms_dict
        data_sheet['correctors'] = cors_dict
        data_sheet['scan_range'] = [(c, a.tolist()) for (c, a) in self._srange_list]
        data_sheet['machine'] = machine
        data_sheet['segment'] = segment
        #
        info_conf = data_sheet['info']
        info_conf['app'] = self.getAppTitle()
        info_conf['version'] = self.getAppVersion()
        info_conf['file_type'] = 'matrix'

        #
        orm_conf = data_sheet['measurement_config']
        orm_conf['orm'] = orm
        orm_conf['corrector_field'] = self.corrector_fields_cbb.currentText()
        orm_conf['monitor_field'] = self.monitor_fields_cbb.currentText()
        orm_conf['wait_seconds'] = self._wait_sec
        orm_conf['reset_wait_seconds'] = self._reset_wait_sec
        orm_conf['set_precision'] = self._mprec
        orm_conf['alter_range'] = {
            'relative range': self._rel_range,
            'total_steps': self._ssteps
        }
        orm_conf['daq_nshot'] = self._daq_nshot
        orm_conf['daq_rate'] = self._daq_rate
        if self._keep_all:
            orm_conf['orm_all'] = self._orm_all_data.tolist()

        # correction config
        cor_conf = data_sheet['correction_config']
        cor_conf['lower_limit'] = float(self.lower_limit_lineEdit.text())
        cor_conf['upper_limit'] = float(self.upper_limit_lineEdit.text())
        cor_conf['damping_factor'] = self.cor_damping_fac_dsbox.value()
        cor_conf['niter'] = self.cor_niter_sbox.value()
        cor_conf['wait_seconds'] = self.cor_wait_time_dsbox.value()
        cor_conf['set_precision'] = self.cor_prec_sbox.value()
        cor_conf['daq_nshot'] = self.eva_daq_nshot_sbox.value()
        cor_conf['daq_rate'] = self.eva_daq_rate_sbox.value()

        data_sheet.write(filepath)

    @pyqtSlot()
    def on_select_all_elems(self, mode):
        """Select all BPMs/CORs in *mode*s_treeView.
        """
        try:
            print("Select All {}s".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                                "Selection error, Choose elements first.",
                                QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self, mode):
        """Inverse current BPM/COR selection in *mode*s_treeView.
        """
        try:
            print("Inverse {} selection".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                                "Selection error, Choose elements first.",
                                QMessageBox.Ok)

    @pyqtSlot()
    def on_stop_measure_orm(self):
        """Stop ORM measurement.
        """
        print("Stop ORM measurement...")
        self.orm_runner.stop()

    def on_stop_orm_worker(self, msg):
        QMessageBox.warning(self, "Orbit Response Matrix App",
                            msg, QMessageBox.Ok)

    @pyqtSlot()
    def on_stop_apply_orm(self):
        """Stop ORM applying.
        """
        print("Stop ORM applying...")
        self.orm_consumer.stop()

    @pyqtSlot('QString')
    def on_elem_field_changed(self, mode, s):
        """Element field is changed.
        """
        try:
            print("Change selected {} field to {}...".format(mode.upper(), s))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.change_field(s)
        except AttributeError:
            QMessageBox.warning(self, "Change {} Field".format(mode.upper()),
                                "No worries, probably {}s are not ready, try to load the matrix file.".format(
                                    mode.upper()),
                                QMessageBox.Ok)

    @pyqtSlot()
    def start_eta_timer(self):
        self._start_time = time.time()
        self.eta_timer = QTimer(self)
        self.eta_timer.timeout.connect(self.update_eta_timer)
        self.eta_timer_lbl.setText('00:00:00')
        self.eta_timer.start(1000)

    @pyqtSlot()
    def update_eta_timer(self):
        self.eta_timer_lbl.setText(uptime(time.time() - self._start_time))

    @pyqtSlot()
    def stop_eta_timer(self):
        self.eta_timer.stop()

    @pyqtSlot()
    def on_evaluate_settings_from_orm(self):
        """
        """
        params = self.__prepare_inputs_for_orm_apply()
        if params is None:
            return

        settings = self.get_settings_from_orm(params)
        self._sv = SettingsView(settings, fmt=self.get_fmt())
        self._sv.setWindowTitle("Overview of Correctors' Settings")
        r = self._sv.exec_()
        if r == QDialog.Accepted:
            print('OK')
            self._cor_settings = settings
            QMessageBox.information(self, "Evaluate Settings",
                                    "New settings for the correctors are ready to apply, "
                                    "click 'Apply' to proceed.",
                                    QMessageBox.Ok)
        else:
            print('Cancel')

    @staticmethod
    def get_settings_from_orm(params):
        """Get corrector settings from ORM based on *params*.
        """
        (lat,), (bpms, cors), (xoy, cor_field, dfac, niter, wait, l_limit, u_limit), \
            (daq_rate, daq_nshot) = params
        s = lat.get_settings_from_orm(cors, bpms,
                                      cor_field=cor_field, cor_min=l_limit, cor_max=u_limit,
                                      damping_factor=dfac, nshot=daq_nshot, rate=daq_rate)
        return s

    @pyqtSlot()
    def on_update_settings_dq(self, sg):
        if sg == 'finish' and self._append_settings_dq:
            print("Finished emit")
            self._settings_dq.append(self._cor_settings)
            self._settings_pt = len(self._settings_dq) - 1
            self.update_undo_redo_status()
            # Update buttons
            # self.__update_settings_btnlist()
            # from PyQt5.QtWidgets import QToolButton
            # btn = QToolButton(self)
            # btn.setText("")
            # self.cached_settings_hbox.insertWidget(0, btn)

        elif sg == 'stop':
            print("Stopped emit")
            self._append_settings_dq = False
        elif sg == 'start':
            print("Started emit")
            self._append_settings_dq = True

    def update_undo_redo_status(self):
        print("spt:", self._settings_pt)
        print("sl :", len(self._settings_dq))
        if self._settings_pt == 0:
            self.undo_apply_btn.setEnabled(False)
        else:
            self.undo_apply_btn.setEnabled(True)
        if self._settings_pt == len(self._settings_dq) - 1:
            self.redo_apply_btn.setEnabled(False)
        else:
            self.redo_apply_btn.setEnabled(True)

    @pyqtSlot()
    def on_undo_apply_orm(self):
        print("Undo Apply...")
        self._settings_pt -= 1
        s = self._settings_dq[self._settings_pt]
        o = self.__apply_with_settings(s, to_cache=False)
        o.finished.connect(self.update_undo_redo_status)

    @pyqtSlot()
    def on_redo_apply_orm(self):
        print("Redo Apply...")
        self._settings_pt += 1
        s = self._settings_dq[self._settings_pt]
        o = self.__apply_with_settings(s, to_cache=False)
        o.finished.connect(self.update_undo_redo_status)

    def init_settings_dq(self):
        # initialize settings_dq
        self._settings_dq = deque([], 3)
        self._settings_pt = None

        cors = [self._name_map[e] for e in self._cors_dict]
        cor_field = self.corrector_fields_cbb.currentText()
        settings = []
        for i in cors:
            v = i.current_setting(cor_field)
            settings.append((i, cor_field, v, v))

        self._settings_dq.append(settings)
        self._settings_pt = len(self._settings_dq) - 1
        #
        self.update_undo_redo_status()

    @pyqtSlot()
    def on_show_cached_settings(self):
        # show cached settings
        print("Show cached settings (TBI)...")
        for s in self._settings_dq:
            print(s)

    @pyqtSlot()
    def on_reset_cached_settings(self):
        self.init_settings_dq()

    @pyqtSlot()
    def on_save_settings(self):
        print("Save current settings to file.")
        cor_field = self.corrector_fields_cbb.currentText()
        cors = [self._name_map[e] for e in self._cors_dict]
        llimit = float(self.lower_limit_lineEdit.text())
        ulimit = float(self.upper_limit_lineEdit.text())
        settings = []
        for cor in cors:
            setting = cor.current_setting(cor_field)
            setting_limited = limit_input(setting, llimit, ulimit)
            settings.append((cor, cor_field, setting, setting_limited))
        #
        for i, (e, f, s, sl) in enumerate(settings):
            print("{0} {1} {2} {3:.3g} {4:.3g}".format(i, e.name, f, s, sl))
        #

        filepath, ext = get_save_filename(self,
                                          cdir='.',
                                          filter="JSON Files (*.json)")
        if filepath is None:
            return

        machine, segment = self._mp.last_machine_name, self._mp.last_lattice_name
        ds = SettingsDataSheet()
        ds['settings'] = {e.name: {'field': f, 'setpoint': s, 'setpoint_limited': sl}
                          for (e, f, s, sl) in settings}
        ds['machine'] = machine
        ds['segment'] = segment

        ds.write(filepath)

    @pyqtSlot()
    def on_load_settings(self):
        print("Load settings from file.")
        filepath, ext = get_open_filename(self,
                                          filter="JSON Files (*.json)")
        if filepath is None:
            return

        settings, mp = load_settings_sheet(filepath)

        if self._mp is None:
            self._mp = mp

        self._sv_loaded = SettingsView(settings, fmt=self.get_fmt())
        self._sv_loaded.setWindowTitle("Overview of Loaded Correctors' Settings")
        r = self._sv_loaded.exec_()
        if r == QDialog.Accepted:
            self._cor_settings = settings
            QMessageBox.information(self, "Evaluate Settings",
                                    "New settings for the correctors are ready to apply, "
                                    "click 'Apply' to proceed.",
                                    QMessageBox.Ok)
        else:
            print('Cancel')

    def get_fmt(self):
        n = self.cor_prec_sbox.value()
        return '{{{0}:.{1}g}}'.format(0, n)

    @pyqtSlot(bool)
    def on_keep_all_orm_data(self, f):
        self._keep_all = f

    def update_lattice_info(self):
        if self._mp is None:
            return
        mach_name = self._mp.last_machine_name
        lat_name = self._mp.last_lattice_name
        self.loaded_mach_lbl.setText(mach_name)
        self.loaded_lattice_lbl.setText(lat_name)

    @pyqtSlot()
    def on_show_latinfo(self):
        machine = self.loaded_mach_lbl.text()
        lattice = self.loaded_lattice_lbl.text()
        if machine == '' or lattice == '':
            return

        from phantasy.apps.lattice_viewer import LatticeViewerWindow
        from phantasy.apps.lattice_viewer import __version__
        from phantasy.apps.lattice_viewer import __title__

        if self._lv is None:
            self._lv = LatticeViewerWindow(__version__)
            self._lv.setWindowTitle("{} ({})".format(__title__, self.getAppTitle()))
        lw = self._lv.latticeWidget
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        lw.setEnabled(False)
        self._lv.show()

    def on_set_srange_model(self):
        # set up settings w/ scan range model view.
        data = [(self._name_map[ename], fname[0])
                for ename, fname in self._cors_dict.items()]

        model = ScanRangeModel(self.cor_srange_tableView, data,
                               self._rel_range, fmt=self.get_fmt())
        model.set_model()

    def get_srange_list(self, n=None):
        #
        # list of (cor, srange)
        #
        m = self.cor_srange_tableView.model()
        if n is None:
            n = self.alter_steps_sbox.value()
        srange_list = m.get_scan_range(n)
        self._srange_list = srange_list
        # debug
        for i, (cname, srange) in enumerate(srange_list):
            print("[{}] {}: {}".format(i, cname, srange))
        #
        return srange_list

    @staticmethod
    def _pb_msg_to_index(msg):
        #
        # return corrector index from pb msg.
        #
        return int(msg.split()[3].replace('[', '').replace(']', '')) - 1

    def init_params(self):
        """Initialize parameters for matrix measurement/apply.
        """
        # measurement
        # op mode
        self._source = OP_MODE_MAP[self.operation_mode_cbb.currentText()]
        # wait secs
        self._wait_sec = self.wait_time_dsbox.value()
        self._reset_wait_sec = self.reset_wait_time_dsbox.value()
        # global ssteps
        self._ssteps = self.alter_steps_sbox.value()
        # rel range
        self._rel_range = float(self.rel_range_lineEdit.text())
        # n-prec
        self._mprec = self.mprec_sbox.value()
        # daq rate, nshot
        self._daq_rate = self.daq_rate_sbox.value()
        self._daq_nshot = self.daq_nshot_sbox.value()
        # keep all
        self._keep_all = self.keep_all_data_chkbox.isChecked()

        # apply
        # lower/upper limits
        self._lower_limit = float(self.lower_limit_lineEdit.text())
        self._upper_limit = float(self.upper_limit_lineEdit.text())
        # cor damping factor
        self._cor_dfac = self.cor_damping_fac_dsbox.value()
        # cor nter
        self._cor_niter = self.cor_niter_sbox.value()
        # cor wait sec
        self._cor_wait_sec = self.cor_wait_time_dsbox.value()
        # cor prec
        self._cor_prec = self.cor_prec_sbox.value()
        # cor eva daq rate, nshot
        self._eva_daq_rate = self.eva_daq_rate_sbox.value()
        self._eva_daq_nshot = self.eva_daq_nshot_sbox.value()

    def init_fields(self):
        for o in (self.monitor_fields_cbb, self.corrector_fields_cbb,):
            o.currentTextChanged.emit(o.currentText())

    def init_settings_table(self):
        # WIP
        # initial table for settings
        # cor settings
        self._cor_settings = None
        # hide cached setting view btn
        self.view_cached_settings_btn.setVisible(False)

    def init_latinfo(self):
        # initial lattice info view
        self._lv = None
        self.lattice_info_btn.clicked.connect(self.on_show_latinfo)

    def init_widgets(self):
        # initial widget status
        self.measure_pb.setVisible(False)
        self.measure_pb.setValue(0)
        self.cor_apply_pb.setVisible(False)
        self.cor_apply_pb.setValue(0)
        #
        self.stop_measure_btn.setEnabled(False)
        self.stop_apply_btn.setEnabled(False)

    @pyqtSlot('QString')
    def on_source_changed(self, s):
        # operation mode changed, Simuation/Live
        self._source = OP_MODE_MAP[s]

    @pyqtSlot(bool)
    def on_keep_all_data(self, f):
        self._keep_all = f

    @pyqtSlot()
    def on_value_changed(self, var_str):
        # lineedit returnpressed
        # var_str: attr name
        v = _str2float(self.sender().text())
        if v is not None:
            setattr(self, var_str, v)
        else:
            QMessageBox.warning(self, "Warning",
                                "Input is not a valid number", QMessageBox.Ok)

        # debug
        print("rel_range ", self._rel_range)
        print("lower limit: ", self._lower_limit)
        print("upper limit: ", self._upper_limit)

    @pyqtSlot(float)
    def on_float_changed(self, var_str, update_eta, x):
        setattr(self, var_str, x)
        if update_eta:
            self.on_update_eta()

    @pyqtSlot(int)
    def on_int_changed(self, var_str, update_eta, i):
        setattr(self, var_str, i)
        if update_eta:
            self.on_update_eta()

    @pyqtSlot('QString')
    def on_update_monitor_field(self, s):
        if s == 'X&Y':
            xoy = 'xy'
        else:
            xoy = s.lower()
        self._xoy = xoy
        self._bpm_field = s

    @pyqtSlot('QString')
    def on_update_corrector_field(self, s):
        self._cor_field = s

    def init_elements(self):
        # initial bpms and cors list(elements).
        self._bpms = [self._name_map[e] for e in self._bpms_dict]
        self._cors = [self._name_map[e] for e in self._cors_dict]

    def init_lattice(self):
        if self._mp is not None:
            self._lat = self._mp.work_lattice_conf
        self.set_orm()

    @pyqtSlot()
    def on_update_srange(self, ):
        # update scan range list model with updated rel_range.
        print(self._rel_range)
        m = self.cor_srange_tableView.model()
        m.update_scan_range(self._rel_range)

    def on_update_selection(self, mode, d):
        # update the devices after selection changed
        setattr(self, "_{}s_dict".format(mode), d)
        self.init_elements()


def _str2float(s):
    try:
        x = float(s)
    except:
        r = None
    else:
        r = x
    finally:
        return r


def sort_dict(d):
    return OrderedDict([(k, d[k]) for k in sorted(d, key=lambda i: (i[-4:], i))])
