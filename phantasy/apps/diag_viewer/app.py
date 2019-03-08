#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow
from .utils import DeviceLoader


class DiagViewerWindow(BaseAppForm, Ui_MainWindow):

    # update
    data_updated = pyqtSignal(QVariant, QVariant, QVariant)
    # init
    data_initialized = pyqtSignal(QVariant, QVariant, QVariant)

    def __init__(self, version):
        super(DiagViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Diagnostics Viewer")

        # set app properties
        self.setAppTitle("Diagnostics Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Diagnostics Viewer</h4>
            <p>This app is created to visualize the beam diagnostics
            readings of FRIB accelerator, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self._post_init()

    def _post_init(self,):
        #
        self._segs_chkbox = (self.lebt_chkbox, self.mebt_chkbox,
                             self.mebt2fs1a_chkbox, self.mebt2fs1b_chkbox)
        self._dtype = self.device_type_cbb.currentText()
        self.machine_cbb.currentTextChanged.emit(self.machine_cbb.currentText())

        #
        self.load_pb.setVisible(False)
        # names and elements of loaded devices
        self._names = None
        self._elems = None

        # DAQ
        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)
        #
        self.data_updated.connect(self.matplotlibbarWidget.update_curve)
        self.data_initialized.connect(self.matplotlibbarWidget.reset_data)
        self.__enable_widgets("WAIT")

        # DAQ freq
        self._daqfreq = 1.0
        self.freq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)

        # xdata opt
        self.id_as_x_rbtn.setChecked(False)
        self.pos_as_x_rbtn.setChecked(True)
        self._xdata_gauge = 'pos'

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    @pyqtSlot('QString')
    def on_device_type_changed(self, s):
        self._dtype = s

    @pyqtSlot()
    def on_load_devices(self):
        """Load devices based on selected type.
        """
        if self._mach == "FRIB":
            self._segs = [o.text() for o in self._segs_chkbox if o.isChecked()]
        else: # VA
            self._segs = ["LINAC"]
        if self._segs == []:
            QMessageBox.warning(self, "Device Loading Warning",
                    "Please select segments.", QMessageBox.Ok)
            return

        print("Load device of type: {}".format(self._dtype))
        self.load_pb.setVisible(True)
        self.load_status_lbl.setText("Loading...")
        self.thread = QThread()
        self.loader = DeviceLoader(self._mach, self._segs, self._dtype)
        self.loader.moveToThread(self.thread)
        self.loader.results_ready.connect(self.on_results_ready)
        self.loader.finished.connect(self.load_complete)
        self.loader.finished.connect(self.thread.quit)
        self.loader.finished.connect(self.loader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.loader.run)
        self.thread.start()
        self.load_btn.setEnabled(False)

    @pyqtSlot(bool)
    def load_complete(self, is_load_success):
        """Lattice loading completed.
        """
        self.load_pb.setVisible(False)
        if is_load_success:
            info = 'Loaded ({}) {}s from {}'.format(len(self._names),
                                                    self._dtype, self._mach)
        else:
            info = 'Failed to load {} from {}'.format(self._dtype, self._mach)
        self.load_status_lbl.setText(info)
        self.load_btn.setEnabled(True)

    @pyqtSlot(QVariant, QVariant)
    def on_results_ready(self, names, elems):
        """Results are ready.
        """
        if names is None:
            QMessageBox.warning(self, "Device Loading Warning",
                    "Failed to load devices.", QMessageBox.Ok)
            return
        self._names = names
        self._elems = elems
        self.field_cbb.clear()
        self.field_cbb.addItems(self._elems[0].fields)

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        # machine is changed
        [o.setEnabled(s=="FRIB") for o in self._segs_chkbox]
        self._mach = s

    @pyqtSlot()
    def on_daq_start(self):
        """Start DAQ.
        """
        if self._names is None:
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        self.daq_timer.start(1000.0 / self._daqfreq)
        self.__enable_widgets("START")

    @pyqtSlot()
    def on_daq_stop(self):
        """Stop DAQ.
        """
        self.daq_timer.stop()
        self.__enable_widgets("STOP")

    @pyqtSlot()
    def on_daq_update(self):
        s, h, herr = self.__refresh_data()
        self.data_updated.emit(s, h, herr)

    def __refresh_data(self):
        field = self.field_cbb.currentText()
        h = [getattr(e, field) for e in self._elems]
        if self._xdata_gauge == 'pos':
            s = [e.sb for e in self._elems]
        else: # ID as x
            s = list(range(len(h)))
        herr = [0] * len(h)
        return s, h, herr

    @pyqtSlot()
    def on_init_dataviz(self):
        # initial plot (reset figure btn)
        s, h, herr = self.__refresh_data()
        self.data_initialized.emit(s, h, herr)

    @pyqtSlot(bool)
    def on_apply_id_as_xdata(self, f):
        if f:
            print("Apply ID as xdata")
            self._xdata_gauge = 'id'

    @pyqtSlot(bool)
    def on_apply_pos_as_xdata(self, f):
        if f:
            print("Apply Pos as xdata")
            self._xdata_gauge = 'pos'

    def __enable_widgets(self, status):
        if status != "START":
            self.reset_figure_btn.setEnabled(True)
            self.start_btn.setEnabled(True)
            self.id_as_x_rbtn.setEnabled(True)
            self.pos_as_x_rbtn.setEnabled(True)
            self.stop_btn.setEnabled(False)
        else:
            self.reset_figure_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.id_as_x_rbtn.setEnabled(False)
            self.pos_as_x_rbtn.setEnabled(False)
            self.stop_btn.setEnabled(True)
