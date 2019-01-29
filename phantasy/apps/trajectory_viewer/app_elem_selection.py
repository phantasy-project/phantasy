#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt

from functools import partial

from phantasy.apps.trajectory_viewer.ui.ui_app_elem_selection import Ui_Form
from phantasy.apps.trajectory_viewer.utils import LatticeDataModel


class ElementSelectionWidget(QWidget, Ui_Form):
    """Keyword Argyments
    --------------------
    ncol : int
        Number of columns for showing dtypes.
    dtypes : list or set
        List of device types (family).
    """

    # set of device types of elements (checked)
    dtypeChanged = pyqtSignal(set)

    # selected elements, list of CaElement
    elementsSelected = pyqtSignal(list)

    def __init__(self, parent, mp, **kws):
        super(ElementSelectionWidget, self).__init__()
        self.parent = parent
        # number of columns in device type checking
        self.__ncolumn = kws.get('ncol', 5)

        # UI
        self.setupUi(self)
        self.setWindowTitle("Select High-level Element(s)")

        #
        self.__mp = mp
        all_dtypes = mp.get_all_types()
        dtypes = kws.get('dtypes', None)
        if dtypes is None:
            self.__dtypes = set(all_types)
        else:
            self.__dtypes = set(i for i in dtypes if i in all_dtypes)

        # events
        self.dtypeChanged.connect(self.on_update_dtype)
        # set lattice data view
        self.set_lattice_view()

    @pyqtSlot(bool)
    def on_toggle_all_dtypes(self, f):
        [o.setChecked(f) for o in self.dtypes_groupBox.findChildren(QCheckBox)]

    @pyqtSlot(set)
    def on_update_dtype(self, l):
        layout = self.gridLayout
        all_dtypes = self.__mp.get_all_types()
        for i, n in enumerate(all_dtypes, 1):
            w = QCheckBox(n, self)
            row, col = int(i / self.__ncolumn), i % self.__ncolumn
            layout.addWidget(w, row, col)
            w.stateChanged.connect(partial(self.on_check_dtype, n))
            if n in l:
                w.setChecked(True)

    @pyqtSlot(int)
    def on_check_dtype(self, dtype, state):
        self.selected_nelem_lineEdit.setText('0')
        if state == Qt.Unchecked:
            self.__dtypes.remove(dtype)
        else:
            self.__dtypes.add(dtype)

        self.update_lattice_data(self.treeView,
                self.__mp, dtypes=self.__dtypes)

    def set_lattice_view(self):
        # set up lattice data view
        self.update_lattice_data(self.treeView, self.__mp, dtypes=self.__dtypes)
        self.dtypeChanged.emit(self.__dtypes)

    def update_lattice_data(self, tv, o, **kws):
        # kws: dtypes
        model = LatticeDataModel(tv, o, **kws)
        model.selectedItemsNumberChanged.connect(lambda i:self.selected_nelem_lineEdit.setText(str(i)))
        model.itemsSelected.connect(self.on_items_selected)
        model.set_model()
        self.listed_nelem_lineEdit.setText("{}".format(tv.model().rowCount()))

    @pyqtSlot(list)
    def on_items_selected(self, elems):
        self.elementsSelected.emit(elems)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    w = ElementSelectionWidget()
    w.show()

    app.exec_()
