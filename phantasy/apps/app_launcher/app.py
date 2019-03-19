#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDialog

from subprocess import Popen
from functools import partial

from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow
from .app_add import AddLauncherDialog
from .utils import data as app_data
from .utils import AppDataModel
from .app_log import LogWidget


MSG_TEMPLATE = "<b><span style='text-decoration: underline;'>{msg[0]}:</span></b><p>{msg[1]}</p>"
#DEFAULT_MSG = '<p align="center"><span style="font-weight:600;">FRIB High-level Physics Controls Applications</span></p><p align="center">Click Button to Launch App</p>'
DEFAULT_MSG = 'FRIB High-level Physics Controls Applications'


class AppLauncherWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version, **kws):
        super(AppLauncherWindow, self).__init__()

        # logfile
        self._logfile = kws.get('logfile', None)
        #print("logfile: ", self._logfile)
        self._logwidget = None

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

        # debug
        self._debug = False

        # view
        self.v = self.tableView

        # set apps
        self.set_apps()

        # post init ui
        self.post_init_ui()

        #
        self.adjustSize()

    def set_apps(self):
        """Set apps defined in app_launcher.ini
        """
        model = AppDataModel(self.v, app_data)
        model.set_model()

    def on_launch_app(self, index):
        # slot
        item = self.v.model().item(index.row(), 0)
        Popen(item.cmd, shell=True)

    def sizeHint(self):
        return QSize(1150, 700)

    def post_init_ui(self):
        #self.textEdit.setHtml(DEFAULT_MSG)
        self.title_lbl.setText(DEFAULT_MSG)

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
    def on_add_launcher(self):
        """[VOID] Add new button as app launcher.
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

    @pyqtSlot(bool)
    def on_enable_debug(self, f):
        """Enable debug mode or not.
        """
        self._debug = f
        print("Debug is enabled?", self._debug)

    @pyqtSlot()
    def on_show_log(self):
        """Show log message under debug mode.
        """
        print("Show log message.")
        if self._logwidget is None:
            self._logwidget = LogWidget(self._logfile)
        self._logwidget.show()
