#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

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

        # default array
        self.array = None

        # initial array if scan task has ready alter array set up
        # usually happens for loaded scan task case
        self.init_array(self.parent.scan_task)

    def init_array(self, scan_task):
        if not scan_task.array_mode:
            return
        array = scan_task.get_alter_array()
        self.array = array
        self.data_textEdit.setPlainText(str(array.tolist()))

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
        if self.array is None:
            QMessageBox.warning(self, "Alter Array Set",
                                "No Array is Set",
                                QMessageBox.Ok)
            return

        if self.array.size != 0:
            self.close()
            self.setResult(QDialog.Accepted)
        else:
            QMessageBox.warning(self, "Alter Array Set",
                                "Empty Array is not valid",
                                QMessageBox.Ok)
            return

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    @pyqtSlot()
    def on_text_changed(self):
        """Text (array) is changed.
        """
        o = self.sender()
        array = self.plain_text_to_array(o.toPlainText())
        if array is not None:
            self.array = array

    @staticmethod
    def plain_text_to_array(text):
        """Convert plain text to array.
        """
        try:
            a = np.asarray(eval(text))
        except:
            a = None
        return a

    @pyqtSlot()
    def on_sort_array(self):
        """Sort array and refresh the data_textEdit.
        """
        obj = self.sender()
        if obj == self.sort_asc_tbtn:
            # sort ascending
            array = sorted(self.array)
        elif obj == self.sort_desc_tbtn:
            # sort descending
            array = sorted(self.array, reverse=True)
        self.data_textEdit.setPlainText(str(array))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    dlg = ArraySetDialog()
    dlg.show()

    app.exec_()
