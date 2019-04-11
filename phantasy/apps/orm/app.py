#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QIntValidator

from functools import partial
from collections import OrderedDict
from collections import deque
import numpy as np
import time

from phantasy_ui import BaseAppForm
from phantasy.apps.trajectory_viewer.utils import ElementListModel
from phantasy.apps.utils import get_save_filename
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import uptime
from phantasy import limit_input

from .ui.ui_app import Ui_MainWindow
from .utils import OrmWorker
from .utils import ORMDataSheet
from .utils import SettingsDataSheet
from .utils import load_orm_sheet
from .utils import load_settings_sheet
from .app_settings_view import SettingsView

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
        self.__mp = kws.get('mp', None)

        # orm
        self._orm = None

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
        # cor settings
        self._cor_settings = None
        # hide cached setting view btn
        self.view_cached_settings_btn.setVisible(False)

        # refresh element list models
        self.refresh_models_btn.clicked.connect(self.on_refresh_models)
        # latinfo
        self.lattice_info_btn.clicked.connect(self.on_show_latinfo)
        self._lv = None

        # set up models for BPMs and CORs
        self.refresh_models_btn.clicked.emit()

        #
        self.measure_pb.setVisible(False)
        self.measure_pb.setValue(0)
        self.cor_apply_pb.setVisible(False)
        self.cor_apply_pb.setValue(0)
        #
        self.stop_measure_btn.setEnabled(False)
        self.stop_apply_btn.setEnabled(False)

        #
        for o in (self.alter_start_lineEdit, self.alter_stop_lineEdit,
                  self.lower_limit_lineEdit, self.upper_limit_lineEdit):
                o.setValidator(QDoubleValidator())
        for o in (self.alter_steps_lineEdit,):
            o.setValidator(QIntValidator())

        #
        self.alter_steps_lineEdit.returnPressed.connect(self.on_update_eta)
        self.wait_time_dspinbox.valueChanged.connect(self.on_update_eta)
        self.reset_wait_time_dspinbox.valueChanged.connect(self.on_update_eta)
        self.daq_rate_sbox.valueChanged.connect(self.on_update_eta)
        self.daq_nshot_sbox.valueChanged.connect(self.on_update_eta)
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
                partial(self.on_elem_field_changed, "bpm"))
        self.corrector_fields_cbb.currentTextChanged.connect(
                partial(self.on_elem_field_changed, "cor"))

        #
        self.on_update_eta()

        #
        self.init_settings_dq()

        # mach/lat info
        self.update_lattice_info()

    @pyqtSlot()
    def on_refresh_models(self):
        # refresh 'bpm' and 'cor' model.
        for mode in ('bpm', 'cor'):
            v = getattr(self, '_{}s_dict'.format(mode))
            tv = getattr(self, '{}s_treeView'.format(mode))
            enames = list(v.keys())
            model = ElementListModel(tv, self.__mp, enames)
            model.set_model()
            o = getattr(self, 'nelem_selected_{}s_lineEdit'.format(mode))
            model.nElementSelected.connect(lambda i:o.setText(str(i)))
            model.select_all_items() # select all by default

        try:
            self.bpms_treeView.model().nElementSelected.connect(
                    lambda i:self.nelem_selected_bpms_lineEdit.setText(str(i)))
            self.cors_treeView.model().nElementSelected.connect(
                    lambda i:self.nelem_selected_cors_lineEdit.setText(str(i)))
        except:
            pass

        #
        self.on_update_eta()

        #
        self.on_set_srange_model()

    @pyqtSlot(dict)
    def on_update_elements(self, mode, elems_dict):
        """Update monitor view with *elems_dict* for *mode*, 'bpm' or 'cor'.
        """
        print("[ORM]-{}: {}".format(mode, elems_dict))
        e_dict = sort_dict(elems_dict)
        setattr(self, '_{}s_dict'.format(mode), e_dict)

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
        self.orm_runner.started.connect(partial(self.orm_worker_started, self.measure_pb, self.stop_measure_btn, [self.run_btn]))
        self.orm_runner.started.connect(self.start_eta_timer)
        self.orm_runner.resultsReady.connect(partial(self.on_results_ready, 'measure'))
        self.orm_runner.update_progress.connect(partial(self.update_pb, self.measure_pb))
        self.orm_runner.finished.connect(self.stop_eta_timer)
        self.orm_runner.finished.connect(partial(self.orm_worker_completed, self.measure_pb, self.stop_measure_btn, [self.run_btn]))
        self.orm_runner.finished.connect(self.thread.quit)
        self.orm_runner.finished.connect(self.orm_runner.deleteLater)
        self.orm_runner.stopped.connect(partial(self.on_stop_orm_worker, "Stopped ORM Measurement..."))
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.orm_runner.run)
        self.thread.start()

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
            print("ORM is ready")
        else:
            pass

    def __prepare_inputs_for_orm_apply(self):
        # limit for correctors
        try:
            llimit = float(self.lower_limit_lineEdit.text())
            ulimit = float(self.upper_limit_lineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Warning",
                    "Invalid Input", QMessageBox.Ok)
            return None
        #
        dfac = self.cor_damping_fac_dspinbox.value()
        niter = self.cor_niter_spinbox.value()
        t_wait = self.cor_wait_time_dspinbox.value()
        # daq rate and nshot
        daq_rate = self.eva_daq_rate_sbox.value()
        daq_nshot = self.eva_daq_nshot_sbox.value()
        #
        cor_field = self.corrector_fields_cbb.currentText()
        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()
        #
        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy
        #
        if self.__mp is None:
            return None
        lat = self.__mp.work_lattice_conf
        lat.orm = self._orm
        #
        # print info debug only
        print("\nTo Apply Correctors Settings...")
        print("--- Name of lattice to correct: {}/{}".format(
            lat.name, self.__mp.last_machine_name))
        print("--- # of BPMs loaded: {}".format(len(bpms)))
        print("--- # of CORs loaded: {}".format(len(cors)))
        print("--- Field of CORs to write: {}".format(cor_field))
        print("--- Field of BPMs to read : {}".format(xoy))
        print("--- Damping factor: {}".format(dfac))
        print("--- # of iteration: {}".format(niter))
        print("--- Wait second after put: {}".format(t_wait))
        print("--- Corrector limit: [{}, {}]".format(llimit, ulimit))
        print("--- DAQ rate, nshot: {}, {}".format(daq_rate, daq_nshot))

        return (lat,), (bpms, cors), \
               (xoy, cor_field, dfac, niter, t_wait, llimit, ulimit), \
               (daq_rate, daq_nshot)

    def __prepare_inputs_for_orm_measurement(self):
        source = OP_MODE_MAP[self.operation_mode_cbb.currentText()]
        try:
            x1 = float(self.alter_start_lineEdit.text())
            x2 = float(self.alter_stop_lineEdit.text())
            n = int(self.alter_steps_lineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "Warning",
                    "Invalid Input", QMessageBox.Ok)
            return None
        srange = np.linspace(x1, x2, n)
        # srange element-wised
        srange_list = self.get_srange_list(n)

        #
        cor_field = self.corrector_fields_cbb.currentText()
        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()
        wait = self.wait_time_dspinbox.value()
        reset_wait = self.reset_wait_time_dspinbox.value()
        ndigits = self.n_digits_measure_spinBox.value()
        # daq rate and nshot
        daq_rate = self.daq_rate_sbox.value()
        daq_nshot = self.daq_nshot_sbox.value()
        # keep all orm data
        keep_all = self.keep_all_data_chkbox.isChecked()
        #
        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy
        self._keep_all = keep_all
        #
        print("\nTo Measure Response Matrix...")
        print("--- Mode:", source)
        print("--- Alter Range: ", srange)
        print("--- Field of CORs to write: ", cor_field)
        print("--- Field of BPMs to read: ", xoy)
        print("--- Wait second after alter: ", wait)
        print("--- Wait second after reset: ", reset_wait)
        print("--- # of Precison Digit: ", ndigits)
        print("--- DAQ rate, nshot: ", daq_rate, daq_nshot)
        print("--- Keep ORM data?: ", keep_all)
        #
        nc = len(cors)
        eta = n * nc * (wait + daq_nshot * 1.0 / daq_rate) + reset_wait * nc
        print("... ETA: {} [H:M:S]".format(eta))
        self.eta_lbl.setText(uptime(int(eta)))
        return (bpms, cors), \
               (source, srange, cor_field, xoy, wait, ndigits), \
               (daq_rate, daq_nshot, reset_wait, keep_all), srange_list

    @pyqtSlot()
    def on_update_eta(self):
        ns = int(self.alter_steps_lineEdit.text())
        nc = len(self._cors_dict)
        dt = self.wait_time_dspinbox.value()
        r_dt = self.reset_wait_time_dspinbox.value()
        nshot = self.daq_nshot_sbox.value()
        daq_rate = self.daq_rate_sbox.value()
        eta = ns * nc * (dt + nshot * 1.0 / daq_rate) + nc * r_dt
        print("NS, NC, DT, NS, DS: ", ns, nc, dt, nshot, 1.0/daq_rate)
        print("... ETA: {} [t]".format(eta))
        self.eta_lbl.setText(uptime(int(eta)))

    def __apply_with_settings(self, settings=None, **kws):
        # apply settings to correct central trajectory
        if settings is None:
            QMessageBox.warning(self, "Apply ORM",
                "Correctors settings are not ready, click 'Evaluate' and 'Apply' again.",
                QMessageBox.Ok)
            return

        lat = self.__mp.work_lattice_conf
        t_wait = self.cor_wait_time_dspinbox.value()
        ndigits = self.n_digits_apply_spinBox.value()
        params = lat, settings, t_wait, ndigits
        to_cache = kws.get('to_cache', True)
        btns = kws.get('btns', [self.cor_apply_btn, self.undo_apply_btn, self.redo_apply_btn])

        self.thread1 = QThread()
        self.orm_consumer = OrmWorker(params, mode='apply')
        self.orm_consumer.moveToThread(self.thread1)
        if to_cache:
            self.orm_consumer.started.connect(partial(self.on_update_settings_dq, 'start'))
        self.orm_consumer.started.connect(partial(self.orm_worker_started, self.cor_apply_pb, self.stop_apply_btn, btns))
        self.orm_consumer.resultsReady.connect(partial(self.on_results_ready, 'apply'))
        self.orm_consumer.update_progress.connect(partial(self.update_pb, self.cor_apply_pb))
        self.orm_consumer.finished.connect(partial(self.orm_worker_completed, self.cor_apply_pb, self.stop_apply_btn, btns))
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
            mp, name_map, bpms_dict, cors_dict, (orm, cor_field, bpm_field, \
                t_wait, reset_wait, n_digits, srange, daq_nshot, daq_rate),\
                (cor_llmt, cor_ulmt, cor_dfac, cor_niter, cor_wait, cor_prec, \
                 cor_daq_rate, cor_daq_nshot), ftype = load_orm_sheet(filepath)
        except:
            QMessageBox.warning(self, "Loading Response Matrix",
                    "Cannot load selected file!", QMessageBox.Ok)
            return

        self.__mp = mp
        self._name_map = name_map
        self._bpms_dict = bpms_dict
        self._cors_dict = cors_dict
        #
        self._orm = orm
        self.refresh_models_btn.clicked.emit()
        self.corrector_fields_cbb.setCurrentText(cor_field)
        self.monitor_fields_cbb.setCurrentText(bpm_field)
        self.wait_time_dspinbox.setValue(t_wait)
        self.reset_wait_time_dspinbox.setValue(reset_wait)
        self.n_digits_measure_spinBox.setValue(n_digits)
        self.daq_rate_sbox.setValue(daq_rate)
        self.daq_nshot_sbox.setValue(daq_nshot)
        srange_start, srange_stop, srange_steps = srange['from'], \
                srange['to'], srange['total_steps']
        self.alter_start_lineEdit.setText(srange_start)
        self.alter_stop_lineEdit.setText(srange_stop)
        self.alter_steps_lineEdit.setText(srange_steps)
        self.corrector_fields_cbb.currentTextChanged.emit(cor_field)
        self.monitor_fields_cbb.currentTextChanged.emit(bpm_field)
        #
        self.lower_limit_lineEdit.setText(str(cor_llmt))
        self.upper_limit_lineEdit.setText(str(cor_ulmt))
        self.cor_damping_fac_dspinbox.setValue(cor_dfac)
        self.cor_niter_spinbox.setValue(int(cor_niter))
        self.cor_wait_time_dspinbox.setValue(cor_wait)
        self.n_digits_apply_spinBox.setValue(int(cor_prec))
        self.eva_daq_nshot_sbox.setValue(int(cor_daq_nshot))
        self.eva_daq_rate_sbox.setValue(int(cor_daq_rate))

        #
        self.update_lattice_info()

        #
        self.init_settings_dq()

        #
        self.on_update_eta()

    @pyqtSlot()
    def on_save_orm(self):
        filepath, ext = get_save_filename(self,
                cdir='.',
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        machine, segment = self.__mp.last_machine_name, self.__mp.last_lattice_name
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
        orm_conf['wait_seconds'] = self.wait_time_dspinbox.value()
        orm_conf['reset_wait_seconds'] = self.reset_wait_time_dspinbox.value()
        orm_conf['set_precision'] = self.n_digits_measure_spinBox.value()
        orm_conf['alter_range'] = {
                 'from': self.alter_start_lineEdit.text(),
                 'to': self.alter_stop_lineEdit.text(),
                 'total_steps': self.alter_steps_lineEdit.text()}
        orm_conf['daq_nshot'] = self.daq_nshot_sbox.value()
        orm_conf['daq_rate'] = self.daq_rate_sbox.value()
        if self._keep_all:
            orm_conf['orm_all'] = self._orm_all_data.tolist()

        # correction config
        cor_conf = data_sheet['correction_config']
        cor_conf['lower_limit'] = float(self.lower_limit_lineEdit.text())
        cor_conf['upper_limit'] = float(self.upper_limit_lineEdit.text())
        cor_conf['damping_factor'] = self.cor_damping_fac_dspinbox.value()
        cor_conf['niter'] = self.cor_niter_spinbox.value()
        cor_conf['wait_seconds'] = self.cor_wait_time_dspinbox.value()
        cor_conf['set_precision'] = self.n_digits_apply_spinBox.value()
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
            QMessageBox.warning(self, "Change Field",
                    "Failed to change field.", QMessageBox.Ok)

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
        (lat,), (bpms, cors), \
        (xoy, cor_field, dfac, niter, wait, l_limit, u_limit), \
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
            #self.__update_settings_btnlist()
            #from PyQt5.QtWidgets import QToolButton
            #btn = QToolButton(self)
            #btn.setText("")
            #self.cached_settings_hbox.insertWidget(0, btn)

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
            v =  i.current_setting(cor_field)
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

        machine, segment = self.__mp.last_machine_name, self.__mp.last_lattice_name
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

        if self.__mp is None:
            self.__mp = mp

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
        n = self.n_digits_apply_spinBox.value()
        return '{{{0}:.{1}g}}'.format(0, n)

    @pyqtSlot(bool)
    def on_keep_all_orm_data(self, f):
        self._keep_all = f

    def update_lattice_info(self):
        if self.__mp is None:
            return
        mach_name = self.__mp.last_machine_name
        lat_name = self.__mp.last_lattice_name
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

        sstart = float(self.alter_start_lineEdit.text())
        sstop = float(self.alter_stop_lineEdit.text())

        from .utils import ScanRangeModel

        model = ScanRangeModel(self.cor_srange_tableView, data,
                               sstart, sstop)#, fmt=self.get_fmt())
        model.set_model()

    def get_srange_list(self, n=None):
        #
        # list of (cor, srange)
        #
        m = self.cor_srange_tableView.model()
        if n is None:
            n = int(self.alter_steps_lineEdit.text())
        srange_list = m.get_scan_range(n)
        self._srange_list = srange_list
        return srange_list



def sort_dict(d):
    return OrderedDict([(k, d[k]) for k in sorted(d, key=lambda i:(i[-4:], i))])
