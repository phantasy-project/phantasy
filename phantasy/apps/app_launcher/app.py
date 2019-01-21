#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot

from subprocess import Popen

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow


class AppLauncherWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(AppLauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("FRIB Physics Applications")
        #self.setWindowIcon()

        # set app properties
        self.setAppTitle("FRIB Physics Applications")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Launcher App</h4>
            <p>This app features the access portal for available
            physics apps for FRIB, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

    @pyqtSlot()
    def on_launch_cv(self):
        """Launch Correlation Visualizer App.
        """
        proc = Popen("correlation_visualizer", shell=True)

    @pyqtSlot()
    def on_launch_qs(self):
        """Launch Quad Scan App.
        """
        proc = Popen("quad_scan", shell=True)

    @pyqtSlot()
    def on_launch_ws(self):
        """Launch Wire Scanner App.
        """
        proc = Popen("wire_scanner", shell=True)

    @pyqtSlot()
    def on_launch_un(self):
        """Launch Unicorn App.
        """
        proc = Popen("unicorn_app", shell=True)

    @pyqtSlot()
    def on_launch_va(self):
        """Launch Virtual Accelerator App.
        """
        proc = Popen("va_launcher", shell=True)

    @pyqtSlot()
    def on_launch_tv(self):
        """Launch Trajectory Viewer App.
        """
        proc = Popen("trajectory_viewer", shell=True)

