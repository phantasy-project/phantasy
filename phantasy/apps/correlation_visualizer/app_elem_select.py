#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

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

    def __init__(self, parent=None, mode='alter', mp=None):
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

        # Element mode
        self.sel_field = None # seleted field name

        # validate flag
        self._already_validated = False

        # set element tree view if mp is defined
        if mp is not None:
            self.on_update_elem_tree(mp)

        # post ui init
        self.pv_mode_radiobtn.toggled.emit(True)
        self.elem_mode_radiobtn.toggled.emit(False)

        # Element mode, selected elements
        self.__element = OrderedDict()

    @pyqtSlot()
    def on_click_ok(self):
        if not self._already_validated:
            is_valid = self.on_validate()
            if not is_valid:
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
                    is_valid = True
                    self._already_validated = True
                else:
                    QMessageBox.warning(self, "",
                            "Device is not connected",
                            QMessageBox.Ok)
                    is_valid = False
            except:
                QMessageBox.critical(self, "",
                        "Validating failed",
                        QMessageBox.Ok)
                is_valid = False
        else:
            # high-level element
            self.set_elem_high_level()
            try:
                if self.sel_elem.connected:
                    QMessageBox.information(self, "",
                            "Device is connected",
                            QMessageBox.Ok)
                    is_valid = True
                    self._already_validated = True
                else:
                    QMessageBox.warning(self, "",
                            "Device is not connected",
                            QMessageBox.Ok)
                    is_valid = False
            except:
                QMessageBox.critical(self, "",
                        "Validating failed",
                        QMessageBox.Ok)
                is_valid = False

        return is_valid

    def set_elem_high_level(self):
        """Build Element from selected high-level element.
        """
        for k, v in self.__element.items():
            self.sel_elem = v.get_field(k[1])
            self.sel_field = self.sel_elem.name
            self.sel_elem_display = v

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

        self.sel_elem_display = self.sel_elem

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
        tv = self.elem_treeView
        model = LatticeDataModel(tv, o)
        model.set_model()
        tv.model().itemSelected.connect(self.on_element_selected)

    @pyqtSlot('QString', 'QString', QVariant)
    def on_element_selected(self, ename, fname, elem):
        ekey = (ename, fname)
        if ekey not in self.__element:
            self.__element.update([(ekey, elem)])
        else:
            self.__element.pop(ekey)

    def sizeHint(self):
        return QSize(600, 400)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    w = ElementSelectDialog(None, 'monitor')
    w.show()

    app.exec_()
