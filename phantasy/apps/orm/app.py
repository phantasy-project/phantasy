#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QIntValidator

from functools import partial
from collections import OrderedDict
import numpy as np
import time

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.trajectory_viewer.utils import ElementListModel
from phantasy.apps.utils import get_save_filename
from phantasy.apps.utils import get_open_filename
from phantasy.apps.utils import uptime

from .ui.ui_app import Ui_MainWindow
from .utils import OrmWorker
from .utils import ORMDataSheet
from .utils import load_orm_sheet


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
        self.setWindowTitle("Orbit Response Matrix")

        # set app properties
        self.setAppTitle("Orbit Response Matrix")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Orbit Response Matrix</h4>
            <p>This app is created to measure, manage and visualize
            the orbit response matrices for central trajectory correction,
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
        # refresh element list models
        self.refresh_models_btn.clicked.connect(self.on_refresh_models)

        # set up models for BPMs and CORs
        self.refresh_models_btn.clicked.emit()

        #
        self.measure_pb.setVisible(False)
        self.cor_apply_pb.setVisible(False)
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
        self.orm_runner.started.connect(partial(self.orm_worker_started, self.measure_pb, self.stop_measure_btn, self.run_btn))
        self.orm_runner.started.connect(self.start_eta_timer)
        self.orm_runner.resultsReady.connect(partial(self.on_results_ready, 'measure'))
        self.orm_runner.update_progress.connect(partial(self.update_pb, self.measure_pb))
        self.orm_runner.finished.connect(self.stop_eta_timer)
        self.orm_runner.finished.connect(partial(self.orm_worker_completed, self.measure_pb, self.stop_measure_btn, self.run_btn))
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
        sender_obj.setEnabled(False)
        pb.setVisible(True)
        sbtn.setEnabled(True)

    @pyqtSlot()
    def orm_worker_completed(self, pb, sbtn, sender_obj):
        print("ORM worker is done.")
        sender_obj.setEnabled(True)
        pb.setVisible(False)
        sbtn.setEnabled(False)

    @pyqtSlot(QVariant)
    def on_results_ready(self, mode, m):
        if mode == 'measure':
            self._orm = m
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
        lat = self.__mp.work_lattice_conf
        lat.orm = self._orm
        #
        # print info debug only
        print("-" * 30)
        print("Name of lattice to correct: {}".format(lat.name))
        print("# of BPMs loaded: {}".format(len(bpms)))
        print("# of CORs loaded: {}".format(len(cors)))
        print("Field of CORs to write: {}".format(cor_field))
        print("Field of BPMs to read : {}".format(xoy))
        print("Damping factor: {}".format(dfac))
        print("# of iteration: {}".format(niter))
        print("Wait second after put: {}".format(t_wait))
        print("Corrector limit: [{}, {}]".format(llimit, ulimit))
        print("-" * 30)

        return (lat,), (bpms, cors), (xoy, cor_field, dfac, niter, t_wait, llimit, ulimit)

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
        #
        cor_field = self.corrector_fields_cbb.currentText()
        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()
        wait = self.wait_time_dspinbox.value()
        #
        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy
        #
        print("source:", source)
        print("srange:", srange)
        print("cor_field:", cor_field)
        print("xoy:", xoy)
        print("wait:", wait)
        #
        eta = n * len(cors) * wait
        print("ETA: {} [H:M:S]".format(eta))
        self.eta_lbl.setText(uptime(int(eta)))
        return (bpms, cors), (source, srange, cor_field, xoy, wait)

    @pyqtSlot()
    def on_update_eta(self):
        ns = int(self.alter_steps_lineEdit.text())
        nc = len(self._cors_dict)
        dt = self.wait_time_dspinbox.value()
        eta = ns * nc * dt
        print("NS, NC, DT: ", ns, nc, dt)
        print("ETA: {} [t]".format(eta))
        self.eta_lbl.setText(uptime(int(eta)))

    @pyqtSlot()
    def on_apply_orm(self):
        """Apply ORM to correct orbit.
        """
        params = self.__prepare_inputs_for_orm_apply()
        if params is None:
            return

        self.thread1 = QThread()
        self.orm_consumer = OrmWorker(params, mode='apply')
        self.orm_consumer.moveToThread(self.thread1)
        self.orm_consumer.started.connect(partial(self.orm_worker_started, self.cor_apply_pb, self.stop_apply_btn, self.cor_apply_btn))
        self.orm_consumer.resultsReady.connect(partial(self.on_results_ready, 'apply'))
        self.orm_consumer.update_progress.connect(partial(self.update_pb, self.cor_apply_pb))
        self.orm_consumer.finished.connect(partial(self.orm_worker_completed, self.cor_apply_pb, self.stop_apply_btn, self.cor_apply_btn))
        self.orm_consumer.finished.connect(self.thread1.quit)
        self.orm_consumer.finished.connect(self.orm_consumer.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.started.connect(self.orm_consumer.run)
        self.thread1.start()

    @pyqtSlot()
    def on_open_orm(self):
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        mp, name_map, bpms_dict, cors_dict, orm, cor_field, bpm_field = \
                load_orm_sheet(filepath)
        self.__mp = mp
        self._name_map = name_map
        self._bpms_dict = bpms_dict
        self._cors_dict = cors_dict
        self._orm = orm
        self.refresh_models_btn.clicked.emit()
        self.corrector_fields_cbb.setCurrentText(cor_field)
        self.monitor_fields_cbb.setCurrentText(bpm_field)
        self.corrector_fields_cbb.currentTextChanged.emit(cor_field)
        self.monitor_fields_cbb.currentTextChanged.emit(bpm_field)

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
        data_sheet['machine'] = machine
        data_sheet['segment'] = segment
        data_sheet['orm'] = orm
        data_sheet['corrector_field'] = self.corrector_fields_cbb.currentText()
        data_sheet['monitor_field'] = self.monitor_fields_cbb.currentText()

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



def sort_dict(d):
    return OrderedDict([(k, d[k]) for k in sorted(d, key=lambda i:(i[-4:], i))])
