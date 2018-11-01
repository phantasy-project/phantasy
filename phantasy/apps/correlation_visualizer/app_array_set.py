#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator

import numpy as np

from phantasy.apps.correlation_visualizer.ui.ui_array_set import Ui_Dialog
from phantasy.apps.utils import get_open_filename


class ArraySetDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ArraySetDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Set Alter Range by Array")

        # self.adjustSize()

        # btns
        self.ok_btn.clicked.connect(self.on_click_ok)
        self.cancel_btn.clicked.connect(self.on_click_cancel)
        self.generate_btn.clicked.connect(self.on_generate_array)
        self.import_btn.clicked.connect(self.on_import_array)

        # validators
        self.vfrom_lineEdit.setValidator(QDoubleValidator())
        self.vto_lineEdit.setValidator(QDoubleValidator())
        self.vstep_lineEdit.setValidator(QDoubleValidator())

    @pyqtSlot()
    def on_generate_array(self):
        """Generate array and show.
        """
        try:
            v_from = float(self.vfrom_lineEdit.text())
            v_to = float(self.vto_lineEdit.text())
            v_step = float(self.vstep_lineEdit.text())
        except ValueError:
            QMessageBox.warning(self, "", "Input values are invalid",
                    QMessageBox.Ok)
        else:
            self.array = np.arange(v_from, v_to + v_step, v_step)
            self.data_textEdit.setPlainText(str(self.array.tolist()))

    @pyqtSlot()
    def on_import_array(self):
        """Import array from external file.
        """
        filepath, ext = get_open_filename(self,
                filter="TXT Files (*.txt);;NPY Files (*.npy);;CSV Files (*.csv)")
        if filepath is None:
            return
        if ext.upper() == 'TXT':
            arr = np.loadtxt(filepath)
        elif ext.upper() == 'NPY':
            arr = np.load(filepath)
        elif ext.upper() == 'CSV':
            arr = np.loadtxt(filepath)
        else:
            return

        self.array = arr
        self.data_textEdit.setPlainText(str(arr.tolist()))

    @pyqtSlot()
    def on_click_ok(self):
        if self.array.size != 0:
            self.close()
            self.setResult(QDialog.Accepted)
        else:
            QMessageBox.warning(self, "", "Empty Array is not valid",
                    QMessageBox.Ok)
            return

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    dlg = ArraySetDialog()
    dlg.show()

    app.exec_()
