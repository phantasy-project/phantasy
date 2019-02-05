#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMainWindow

from functools import partial
import numpy as np

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.trajectory_viewer.utils import ElementListModel

from .ui.ui_app import Ui_MainWindow
from .utils import OrmWorker


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
        self._bpms_dict = kws.get('bpms', {})

        # cors dict
        self._cors_dict = kws.get('cors', {})

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

    @pyqtSlot()
    def on_refresh_models(self):
        # refresh 'bpm' and 'cor' model.
        for mode in ('bpm', 'cor'):
            v = getattr(self, '_{}s_dict'.format(mode))
            tv = getattr(self, '{}s_treeView'.format(mode))
            enames = list(v.keys())
            model = ElementListModel(tv, self.__mp, enames)
            model.set_model()

    @pyqtSlot(dict)
    def on_update_elements(self, mode, elems_dict):
        """Update monitor view with *elems_dict* for *mode*, 'bpm' or 'cor'.
        """
        print("[ORM]-{}: {}".format(mode, elems_dict))
        setattr(self, '_{}s_dict'.format(mode), elems_dict)

    @pyqtSlot()
    def on_measure_orm(self):
        """Measure ORM.
        """
        params = self.__prepare_inputs_for_orm_measurement()

        self.thread = QThread()
        self.orm_runner = OrmWorker(params)
        self.orm_runner.moveToThread(self.thread)
        self.orm_runner.started.connect(partial(self.orm_worker_started, self.measure_pb, self.run_btn))
        self.orm_runner.resultsReady.connect(partial(self.on_results_ready, 'measure'))
        self.orm_runner.update_progress.connect(partial(self.update_pb, self.measure_pb))
        self.orm_runner.finished.connect(partial(self.orm_worker_completed, self.measure_pb, self.run_btn))
        self.orm_runner.finished.connect(self.thread.quit)
        self.orm_runner.finished.connect(self.orm_runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.orm_runner.run)
        self.thread.start()

    @pyqtSlot(float, 'QString')
    def update_pb(self, pb, x, s):
        pb.setValue(x)
        pb.setFormat("%p%")
        self.log_textEdit.append(s)

    @pyqtSlot()
    def orm_worker_started(self, pb, sender_obj):
        print("ORM worker is about to start.")
        sender_obj.setEnabled(False)
        pb.setVisible(True)

    @pyqtSlot()
    def orm_worker_completed(self, pb, sender_obj):
        print("ORM worker is done.")
        sender_obj.setEnabled(True)
        pb.setVisible(False)

    @pyqtSlot(QVariant)
    def on_results_ready(self, mode, m):
        if mode == 'measure':
            self._orm = m
            print("ORM is ready")
        else:
            pass

    def __prepare_inputs_for_orm_measurement(self):
        source = OP_MODE_MAP[self.operation_mode_cbb.currentText()]
        x1 = float(self.alter_start_lineEdit.text())
        x2 = float(self.alter_stop_lineEdit.text())
        n = int(self.alter_steps_lineEdit.text())
        srange = np.linspace(x1, x2, n)

        cor_field = list(self._cors_dict.values())[0][0]

        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()
        wait = self.wait_time_dspinbox.value()

        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy

        print("source:", source)
        print("srange:", srange)
        print("cor_field:", cor_field)
        print("xoy:", xoy)
        print("wait:", wait)

        return (bpms, cors), (source, srange, cor_field, xoy, wait)

    @pyqtSlot()
    def on_apply_orm(self):
        """Apply ORM to correct orbit.
        """
        dfac = self.cor_damping_fac_dspinbox.value()
        niter = self.cor_niter_spinbox.value()
        t_wait = self.cor_wait_time_dspinbox.value()
        print(dfac, niter, t_wait)

        lat = self.__mp.work_lattice_conf
        lat.orm = self._orm
        #
        params = (lat,), (self._bpms, self._cors), (self._xoy, dfac, niter, t_wait)

        self.thread1 = QThread()
        self.orm_consumer = OrmWorker(params, mode='apply')
        self.orm_consumer.moveToThread(self.thread1)
        self.orm_consumer.started.connect(partial(self.orm_worker_started, self.cor_apply_pb, self.cor_apply_btn))
        self.orm_consumer.resultsReady.connect(partial(self.on_results_ready, 'apply'))
        self.orm_consumer.update_progress.connect(partial(self.update_pb, self.cor_apply_pb))
        self.orm_consumer.finished.connect(partial(self.orm_worker_completed, self.cor_apply_pb, self.cor_apply_btn))
        self.orm_consumer.finished.connect(self.thread1.quit)
        self.orm_consumer.finished.connect(self.orm_consumer.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.started.connect(self.orm_consumer.run)
        self.thread1.start()
