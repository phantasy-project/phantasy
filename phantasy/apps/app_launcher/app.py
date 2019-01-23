#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDialog

from subprocess import Popen
from functools import partial

from phantasy_ui.templates import BaseAppForm

from .ui.ui_app import Ui_MainWindow
from .app_add import AddLauncherDialog


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
DEFAULT_MSG = '<p align="center"><span style="font-weight:600;">FRIB High-level Physics Controls Applications</span></p><p align="center">Click Button to Launch App</p>'

APP_CMD = {
    'cv': 'correlation_visualizer',
    'qs': 'quad_scan',
    'ws': 'wire_scanner',
    'va': 'va_launcher',
    'tv': 'trajectory_viewer',
    'un': 'unicorn_app',
}


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

        self.cv_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['cv']))
        self.qs_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['qs']))
        self.ws_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['ws']))
        self.va_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['va']))
        self.tv_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['tv']))
        self.un_btn.clicked.connect(partial(self.on_launch_app, APP_CMD['un']))

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
    def on_launch_app(self, cmd):
        proc = Popen(cmd, shell=True)

    @pyqtSlot()
    def on_add_launcher(self):
        """Add new button as app launcher.
        """
        idx = self.horizontalLayout.count()
        self._dlg = AddLauncherDialog()
        r = self._dlg.exec_()
        if r == QDialog.Accepted and self._dlg.launcher is not None:
            launcher = self._dlg.launcher
            btn = launcher.button
            self.horizontalLayout.insertWidget(idx - 1, btn)

            btn.clicked.connect(partial(self.on_launch_app, launcher.cmd))
            btn.installEventFilter(self)
            MSG.update({launcher.name: (launcher.name, launcher.desc)})

        else:
            return
