#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QProcess

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow


class VALauncherWindow(BaseAppForm, Ui_MainWindow):
    #
    vaStatusChanged = pyqtSignal('QString')

    def __init__(self, version):
        super(VALauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Virtual Accelerator Launcher")
#        self.setWindowIcon(QIcon(QPixmap(va_icon)))

        # set app properties
        self.setAppTitle("VA Launcher")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Virtual Accelerator Launcher</h4>
            <p>App for FRIB virtual accelerators management,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # status
        self.vaStatusChanged.connect(self.statusInfoChanged)

        # initialization
        self.on_machine_changed(self.mach_comboBox.currentText())
        self.on_engine_changed(self.engine_comboBox.currentText())

    @pyqtSlot()
    def on_run_va(self):
        """Run VA.
        """
        mach = self._mach
        run_cmd = self._run_cmd
        va = QProcess()
        self.va_process = va
        arguments = [run_cmd, '--mach', mach, '-v']
        va.start('/usr/local/bin/phytool', arguments)

        # start
        va.started.connect(self.on_va_started)
        va.errorOccurred.connect(self.on_error_occurred)

    def on_error_occurred(self, err):
        print("Error (code: {}) occurred...".format(err))

    @pyqtSlot()
    def on_va_started(self):
        """VA is started.
        """
        print("VA is started...")
        self.vaStatusChanged.emit(
            "<html><p style=″color:#4E9A06;″>VA is Running...</p></html>")

    @pyqtSlot()
    def on_stop_va(self):
        """Stop VA.
        """
        pid = self.va_process.processId()
        self.va_process.kill()
        print("VA ({}) is stopped...".format(pid))
        self.vaStatusChanged.emit(
            "<html><p style=″color:#EF2929;″>VA is Not Running...</p></html>")

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        """Machine is changed.
        """
        print(s)
        self._mach = s

    @pyqtSlot('QString')
    def on_engine_changed(self, s):
        self._engine = s
        self._run_cmd = '{}-vastart'.format(s.lower())
