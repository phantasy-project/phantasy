#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMainWindow

from functools import partial
import numpy as np

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.trajectory_viewer.utils import ElementListModel

from .ui.ui_app import Ui_MainWindow


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

        # test
        #self.__test()

    def __test(self):
        print(self._name_map)

    def post_init(self):
        # refresh element list model
        self.refresh_cors_btn.clicked.connect(
                partial(self.on_refresh_model, 'cor'))
        self.refresh_bpms_btn.clicked.connect(
                partial(self.on_refresh_model, 'bpm'))

        # set up models for BPMs and CORs
        self.refresh_cors_btn.clicked.emit()
        self.refresh_bpms_btn.clicked.emit()

    @pyqtSlot()
    def on_refresh_model(self, mode):
        # mode: 'bpm' or 'cor'
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
        #self.run_progressbar.setVisible(True)
        #self.emstop_btn.setVisible(True)
        #self.run_progressbar.setValue(0)

        params = self.__prepare_inputs_for_orm_runner()

        from PyQt5.QtCore import QThread
        from .utils import OrmRunner

        self.thread = QThread()

        self.orm_runner = OrmRunner(params)
        self.orm_runner.moveToThread(self.thread)
        self.orm_runner.resultsReady.connect(self.on_results_ready)
        #self.orm_runner.update_progress.connect(self.update_progress_bar)
        self.orm_runner.finished.connect(self.complete)
        self.orm_runner.finished.connect(self.thread.quit)
        self.orm_runner.finished.connect(self.orm_runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.orm_runner.run)
        self.thread.start()

    @pyqtSlot()
    def complete(self):
        #
        print("ORM runner is done.")

    @pyqtSlot(QVariant)
    def on_results_ready(self, m):
        # orm is ready
        np.savetxt("orm_test20190131.dat", m)
        print("ORM is saved")

    def __prepare_inputs_for_orm_runner(self):
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

        print("source:", source)
        print("srange:", srange)
        print("cor_field:", cor_field)
        print("xoy:", xoy)
        print("wait:", wait)

        return (bpms, cors), (source, srange, cor_field, xoy, wait)


