#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

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
        model.view_size.connect(self.on_resize)
        model.set_model()
        self._pvs = model._pvs

    def on_resize(self, w, h):
        rect = self.geometry()
        w0, h0 = rect.width(), rect.height()
        if h0 < h:
            h = h0
        else:
            h += 150
        self.resize(w * 1.05, h * 1.05)

    def closeEvent(self, e):
        for pv in self._pvs:
            pv.clear_callbacks()
        QDialog.closeEvent(self, e)

    @pyqtSlot()
    def on_click_ok(self):
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            QDialog.keyPressEvent(self, e)
