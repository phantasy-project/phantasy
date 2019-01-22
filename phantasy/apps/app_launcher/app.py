#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow

from subprocess import Popen

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow


MSG = {
  'cv': ('Correlation Visualizer',
         'Visualize the correlation between parameters.'),
  'qs': ('Quad Scan App',
         'Calculate transverse emittance based on quadrupole scan approach.'),
  'ws': ('Wire Scanner App',
         'Operating wire-scanner device and processing the acquired data.'),
  'va': ('Virtual Accelerator Launcher',
         'Launch FRIB virtual accelerators.'),
  'tv': ('Trajectory Viewer',
         'Visualize beam trajectory and apply correction.'),
  'un': ('Unicorn App',
         'Manage and visualize the scaling laws between engineering and phyiscs units.'),
}

MSG_TEMPLATE = "<b><span style='text-decoration: underline;'>{msg[0]}:</span></b><p>{msg[1]}</p>"
DEFAULT_MSG = '<p align="center"><span style="font-size:12pt;font-weight:600;">FRIB High-level Physics Controls Applications</span></p><p align="center">Click Button to Launch App</p>'


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

        # post init ui
        self.post_init_ui()

    def post_init_ui(self):
        self.textEdit.setHtml(DEFAULT_MSG)
        for btn,tt in zip(
                (self.cv_btn, self.qs_btn, self.ws_btn, self.va_btn, self.tv_btn, self.un_btn),
                ('cv', 'qs', 'ws', 'va', 'tv', 'un')):
            btn.setText(tt)
            btn.installEventFilter(self)

    def eventFilter(self, src, e):
        if e.type() == QEvent.HoverEnter:
            t = src.text()
            self.textEdit.setHtml(MSG_TEMPLATE.format(msg=MSG[t]))
            return True
        if e.type() == QEvent.HoverLeave:
            self.textEdit.setHtml(DEFAULT_MSG)
            return True
        return QMainWindow.eventFilter(self, src, e)

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

