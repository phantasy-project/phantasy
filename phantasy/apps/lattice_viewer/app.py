#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_app import Ui_MainWindow
from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import LatticeDataModelFull

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt


class LatticeViewerWindow(BaseAppForm, Ui_MainWindow):

    # selected element by double clicking
    elementSelected = pyqtSignal(QVariant)

    def __init__(self, version):
        super(LatticeViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Lattice Viewer")

        # set app properties
        self.setAppTitle("Lattice Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Lattice Viewer</h4>
            <p>This app is created to visualize the FRIB accelerator
            hierarchical structure, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self.post_init_ui()

    def post_init_ui(self):
        #
        self.__mp = None
        # events
        self.treeView.doubleClicked.connect(self.on_dbclicked_view)
        self.elementSelected.connect(self.probeWidget.on_select_element)

    @pyqtSlot(QVariant)
    def onLatticeChanged(self, o):
        """loaded lattice changed.
        """
        self.__mp = o
        model = LatticeDataModelFull(self.treeView, o)
        model.set_model()
        # update meta info
        self.on_update_metainfo(o)

    def on_update_metainfo(self, o):
        """Update meta info of loaded lattice.
        """
        n_elem = len(o.work_lattice_conf)
        dtypes = o.get_all_types()
        sts_elem = [(f, len(o.get_elements(type=f))) for f in dtypes]
        sts_info = ' '.join(['{}({})'.format(f, n) for f, n in sts_elem])
        self.elem_num_lineEdit.setText('{0:d}'.format(n_elem))
        self.elem_sts_lineEdit.setText(sts_info)
        self.elem_types_lineEdit.setText(';'.join(dtypes))

    @pyqtSlot(QModelIndex)
    def on_dbclicked_view(self, index):
        """On double clicking.
        """
        row, col = index.row(), index.column()
        model = self.treeView.model()
        # selected item
        #item = model.item(row, col)
        ename = model.item(row, 0).text()
        elem = self.__mp.get_elements(name=ename)[0]
        self.elementSelected.emit(elem)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = LatticeViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
