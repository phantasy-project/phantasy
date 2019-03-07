#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow
from .utils import DeviceLoader


class DiagViewerWindow(BaseAppForm, Ui_MainWindow):

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
            self._segs = None
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
            info = 'Loaded {} from {}'.format(self._dtype, self._mach)
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
        print(len(names), len(elems))

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        # machine is changed
        [o.setEnabled(s=="FRIB") for o in self._segs_chkbox]
        self._mach = s
