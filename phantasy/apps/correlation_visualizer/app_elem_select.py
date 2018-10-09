#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot

from phantasy.apps.correlation_visualizer.ui.ui_elem_select import Ui_Dialog
from phantasy.apps.correlation_visualizer.utils import PVElement
from phantasy.apps.correlation_visualizer.utils import PVElementReadonly
from phantasy.apps.correlation_visualizer.utils import delayed_check_pv_status


class ElementSelectDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None, mode='alter'):
        # mode: 'alter' or 'monitor'
        # monitor: only show readback PV
        super(ElementSelectDialog, self).__init__()
        self.parent = parent
        self.mode = mode

        # UI
        self.setupUi(self)
        self.setWindowTitle("Set Alter Element")

        # mode
        [o.setEnabled(mode=='alter') for o in
            (self.pv_set_lbl, self.pv_set_lineEdit, self.copy_set_to_read_btn)]

        self.adjustSize()

        # events
        self.pv_mode_radiobtn.toggled.connect(self.pv_groupBox.setEnabled)
        self.elem_mode_radiobtn.toggled.connect(self.latticeWidget.setEnabled)

        # cmdbtn
        self.ok_btn.clicked.connect(self.on_ok)
        self.cancel_btn.clicked.connect(self.on_cancel)
        self.validate_btn.clicked.connect(self.on_validate)

        # copy_set_to_read_btn, if copy scan put pv string as get pv
        self.copy_set_to_read_btn.clicked.connect(self.on_copy_setpv)

        # PV mode: [set]/read PVs
        self.pv_set_lineEdit.returnPressed.connect(self.set_elem)
        self.pv_read_lineEdit.returnPressed.connect(self.set_elem)
        self.sel_elem = None  # selected element obj

    @pyqtSlot()
    def on_ok(self):
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    @pyqtSlot()
    def on_validate(self):
        """To validate the selected element CA connection.
        """
        if self.pv_mode_radiobtn.isChecked():
            if self.sel_elem is None:
                self.set_elem()
            if self.sel_elem.connected:
                QMessageBox.information(self, "",
                        "Device is connected",
                        QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "",
                        "Device is not connected",
                        QMessageBox.Ok)
        else:
            # high-level element
            pass

    @pyqtSlot()
    def set_elem(self):
        """Build PVElement from [set]/read PVs
        """
        if self.mode == 'alter':
            putPV_str = self.pv_set_lineEdit.text()
            getPV_str = self.pv_read_lineEdit.text()
            if putPV_str == '' or getPV_str == '':
                return
            self.sel_elem = PVElement(putPV_str, getPV_str)
        elif self.mode == 'monitor':
            getPV_str = self.pv_read_lineEdit.text()
            if getPV_str == '':
                return
            self.sel_elem = PVElementReadonly(getPV_str)
        delayed_check_pv_status(self, self.sel_elem, 100)

    @pyqtSlot()
    def on_copy_setpv(self):
        """Copy text from *alter_pv_set_lineEdit* to
        *alter_pv_read_lineEdit*, and replace 'CSET' to 'RD' if possible.
        """
        setpv = self.pv_set_lineEdit.text()
        readpv = re.sub(r'(.*)_CSET', r'\1_RD', setpv)
        self.pv_read_lineEdit.setText(readpv)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    w = ElementSelectDialog(None, 'monitor')
    w.show()

    app.exec_()
