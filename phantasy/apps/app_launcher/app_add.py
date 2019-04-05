#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QToolButton

from phantasy.apps.utils import get_open_filename
from .ui.ui_add import Ui_Dialog


class AddLauncherDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(AddLauncherDialog, self).__init__(parent)

        # UI
        self.setupUi(self)
        self.setWindowTitle("Add New App Launcher")

        #
        self.launcher = None
        self.pixmap = QPixmap(":icons/icons/app3.png")

    @pyqtSlot()
    def on_click_ok(self):
        """Add app launcher.
        """
        name = self.name_lineEdit.text()
        desc = self.desc_textEdit.toPlainText().strip()
        cmd = self.cmd_lineEdit.text()

        launcher = Launcher(name, desc, cmd, pixmap=self.pixmap)
        self.launcher = launcher

        self.accept()

    @pyqtSlot()
    def on_select_icon(self):
        """Select icon for launcher.
        """
        filepath, ext = get_open_filename(self,
                caption="Select PNG File As App Icon",
                filter="PNG Files (*.png)")
        if filepath is None:
            return

        pixmap = QPixmap(filepath)
        self.icon_btn.setIcon(QIcon(pixmap.scaled(64, 64)))
        self.pixmap = pixmap


class Launcher(QObject):
    def __init__(self, name, desc, cmd, pixmap):
        super(self.__class__, self).__init__()

        btn = QToolButton()
        btn.setAutoRaise(True)
        btn.setText(name)
        btn.setIcon(QIcon(pixmap.scaled(128, 128)))
        btn.setIconSize(QSize(128, 128))

        self.button = btn
        self.name = name
        self.desc = desc
        self.cmd = cmd
