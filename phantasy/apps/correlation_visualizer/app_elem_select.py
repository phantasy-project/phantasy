#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize

from phantasy_ui.widgets.utils import LatticeDataModel

from phantasy.apps.correlation_visualizer.ui.ui_elem_select import Ui_Dialog
from phantasy.apps.correlation_visualizer.utils import PVElement
from phantasy.apps.correlation_visualizer.utils import PVElementReadonly
from phantasy.apps.correlation_visualizer.utils import milli_sleep1
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
        self.setWindowTitle("Select Element")

        # mode
        [o.setEnabled(mode=='alter') for o in
            (self.pv_set_lbl, self.pv_set_lineEdit, self.copy_set_to_read_btn)]

        #self.adjustSize()

        # events
        self.pv_mode_radiobtn.toggled.connect(self.pv_groupBox.setEnabled)
        self.elem_mode_radiobtn.toggled.connect(self.elem_treeView.setEnabled)

        # cmdbtn
        self.ok_btn.clicked.connect(self.on_click_ok)
        self.cancel_btn.clicked.connect(self.on_click_cancel)
        self.validate_btn.clicked.connect(self.on_validate)

        # copy_set_to_read_btn, if copy scan put pv string as get pv
        self.copy_set_to_read_btn.clicked.connect(self.on_copy_setpv)

        # PV mode: [set]/read PVs
        self.pv_set_lineEdit.returnPressed.connect(self.set_elem)
        self.pv_read_lineEdit.returnPressed.connect(self.set_elem)
        self.sel_elem = None  # selected element obj

        # validate flag
        self._already_validated = False

    @pyqtSlot()
    def on_click_ok(self):
        if not self._already_validated:
            valid_result = self.on_validate()
            if not valid_result:
                return
        self._already_validated = False
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    @pyqtSlot()
    def on_validate(self):
        """To validate the selected element CA connection.
        """
        if self.pv_mode_radiobtn.isChecked():
            #if self.sel_elem is None:
            self.set_elem()
            try:
                if self.sel_elem.connected:
                    QMessageBox.information(self, "",
                            "Device is connected",
                            QMessageBox.Ok)
                    return True
                else:
                    QMessageBox.warning(self, "",
                            "Device is not connected",
                            QMessageBox.Ok)
            except:
                QMessageBox.critical(self, "",
                        "Validating failed",
                        QMessageBox.Ok)
            return False
        else:
            # high-level element
            pass
        self._already_validated = True

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

        milli_sleep1(2000)
        delayed_check_pv_status(self, self.sel_elem, 100)

    @pyqtSlot()
    def on_copy_setpv(self):
        """Copy text from *alter_pv_set_lineEdit* to
        *alter_pv_read_lineEdit*, and replace 'CSET' to 'RD' if possible.
        """
        setpv = self.pv_set_lineEdit.text()
        readpv = re.sub(r'(.*)_CSET', r'\1_RD', setpv)
        self.pv_read_lineEdit.setText(readpv)

    @pyqtSlot(QVariant)
    def on_update_elem_tree(self, o):
        model = LatticeDataModel(self.elem_treeView, o)
        model.setHeaderData(0, Qt.Horizontal, "Device Type")
        #model.setHeaderData(0, Qt.Horizontal, "Device Type")
        #model.setHeaderData(1, Qt.Horizontal, "Field")
        self.elem_treeView.setModel(model)

    def sizeHint(self):
        return QSize(600, 400)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    w = ElementSelectDialog(None, 'monitor')
    w.show()

    app.exec_()
