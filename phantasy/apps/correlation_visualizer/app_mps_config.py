#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from .ui.ui_mps_config import Ui_Dialog


class MpsConfigWidget(QDialog, Ui_Dialog):
    """Set up the PV name for MPS status.
    """
    def __init__(self, parent=None):
        super(MpsConfigWidget, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)

        #
        self.pvname = None
        self.mps_pv_name_cbb.editTextChanged['QString'].emit(
                self.mps_pv_name_cbb.currentText())

    @pyqtSlot('QString')
    def on_update_pvname(self, s):
        """Update MPS status PV name.
        """
        self.pvname = s

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    @pyqtSlot()
    def on_click_ok(self):
        self.close()
        self.setResult(QDialog.Accepted)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
