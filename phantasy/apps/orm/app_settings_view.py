#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize

from .ui.ui_settings_view import Ui_Dialog
from .utils import SettingsModel


class SettingsView(QDialog, Ui_Dialog):

    def __init__(self, data, parent=None,):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.data = data

        self.setupUi(self)
        self.setWindowTitle("Settings Overview")
        self.v = self.treeView

        model = SettingsModel(self.v, self.data)
        model.set_model()

        self.adjustSize()

    def sizeHint(self):
        return QSize(1600, 900)
