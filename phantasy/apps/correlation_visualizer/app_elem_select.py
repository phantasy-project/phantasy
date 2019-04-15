#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import deque

from PyQt5.QtCore import QSize
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from phantasy_ui.widgets.utils import LatticeDataModel

from phantasy.apps.correlation_visualizer.ui.ui_elem_select import Ui_Dialog
from phantasy.apps.correlation_visualizer.utils import PVElement
from phantasy.apps.correlation_visualizer.utils import PVElementReadonly
from phantasy.apps.correlation_visualizer.utils import delayed_check_pv_status
from phantasy.apps.correlation_visualizer.utils import milli_sleep1

# max number of elements for selection
NMAX = 100


class ElementSelectDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None, mode='alter', mp=None):
        # mode: 'alter' or 'monitor', 'extra'
        # 'alter' and 'monitor': single selection
        # 'extra': multiple selection
        # monitor: only show readback PV
        super(ElementSelectDialog, self).__init__()
        self.parent = parent
        self.mode = mode

        # UI
        self.setupUi(self)
        self.setWindowTitle("Select Element")

        # mode
        [o.setEnabled(mode == 'alter') for o in
         (self.pv_set_lbl, self.pv_set_lineEdit, self.copy_set_to_read_btn)]

        self.adjustSize()

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

        # validate flag
        self._already_validated = False

        # set element tree view if mp is defined
        if mp is not None:
            self.on_update_elem_tree(mp)

        # post ui init
        self.pv_mode_radiobtn.toggled.emit(True)
        self.elem_mode_radiobtn.toggled.emit(False)

        # element selection
        self.__init_element_selection(self.mode)

        # info label
        self.__init_info_label(self.mode)

    def __init_info_label(self, mode):
        if mode != 'extra':  # only show for 'extra' mode
            self.info_lbl.hide()

    def __init_element_selection(self, mode):
        # initialize element selection
        if mode != 'extra':
            n = 1
        else:
            n = NMAX
        self.__elements = deque([], n)
        self.sel_elem = deque([], n)  # selected CaField objs
        self.sel_elem_display = deque([], n)  # Element objs
        self.sel_field = deque([], n)  # seleted field names

    @pyqtSlot()
    def on_click_ok(self):
        if not self._already_validated:
            is_valid = self.on_validate()
            if not is_valid:
                return
        self._already_validated = False
        self.close()
        if not self.sel_field:
            self.setResult(QDialog.Rejected)
        else:
            self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    def _is_elements_all_connected(self, elem_list):
        # return True if all elements in *elem_list* are connected.
        if len(elem_list) == 0:
            return False
        for elem in elem_list:
            if not elem.connected:
                QMessageBox.warning(self, "",
                                    "{} cannot be reached.".format(elem.ename),
                                    QMessageBox.Ok)
                return False
        return True

    @pyqtSlot()
    def on_validate(self):
        """To validate the selected element CA connection.
        """
        if self.pv_mode_radiobtn.isChecked():
            # generic
            self.set_elem()
        else:
            # high-level element
            self.set_elem_high_level()
        try:
            if self._is_elements_all_connected(self.sel_elem):
                QMessageBox.information(self, "",
                                        "Devices are all connected.",
                                        QMessageBox.Ok)
                is_valid = True
                self._already_validated = True
            else:
                QMessageBox.warning(self, "",
                                    "Devices are not all connected.",
                                    QMessageBox.Ok)
                is_valid = False
        except:
            QMessageBox.critical(self, "",
                                 "Validating failed",
                                 QMessageBox.Ok)
            is_valid = False

        return is_valid

    def set_elem_high_level(self):
        """Build selected high-level element(s).
        """
        for ename, fname, elem in self.__elements:
            print(ename, fname, elem.name)
            self.sel_elem.append(elem.get_field(fname))
            self.sel_field.append(fname)
            self.sel_elem_display.append(elem)

    @pyqtSlot()
    def set_elem(self):
        """Build PVElement from [set]/read PVs
        """
        if self.mode == 'alter':
            put_pv_str = self.pv_set_lineEdit.text()
            get_pv_str = self.pv_read_lineEdit.text()
            if put_pv_str == '' or get_pv_str == '':
                return
            sel_elem = PVElement(put_pv_str, get_pv_str)
        else:  # 'monitor' and 'extra'
            get_pv_str = self.pv_read_lineEdit.text()
            if get_pv_str == '':
                return
            sel_elem = PVElementReadonly(get_pv_str)

        self.sel_elem.append(sel_elem)
        self.sel_elem_display.append(sel_elem)
        self.sel_field.append(None)

        milli_sleep1(2000)
        for pvelem in self.sel_elem:
            delayed_check_pv_status(self, pvelem, 100)

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

    @pyqtSlot('QString', 'QString', QVariant, 'QString')
    def on_element_selected(self, ename, fname, elem, op):
        new_sel = (ename, fname, elem)
        if op == 'add':
            if new_sel not in self.__elements:
                self.__elements.append(new_sel)
        else:  # del
            if new_sel in self.__elements:
                self.__elements.remove(new_sel)
        # debug
        print(self.__elements)
        #

    def sizeHint(self):
        return QSize(1000, 800)

    def on_select_element(self, index):
        # slot: dbclick to select
        v = self.elem_treeView
        m = v.model()
        row = index.row()
        item = m.item(row, m.i_name)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    w = ElementSelectDialog(None, 'monitor')
    w.show()

    app.exec_()
