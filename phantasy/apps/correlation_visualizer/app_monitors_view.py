#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint
from .icons import clean_icon as delete_icon


from phantasy.apps.correlation_visualizer.ui.ui_monitors_view import Ui_Form


class MonitorsViewWidget(QWidget, Ui_Form):
    """
    """
    # remove monitor element according to name
    removeElement = pyqtSignal('QString')

    def __init__(self, parent, data):
        super(MonitorsViewWidget, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Elements Selected as Extra Monitors")

        # set and show data
        self.set_data(data)

        self.removeElement['QString'].connect(
                self.parent.update_extra_monitors)

    def set_data(self, data):
        """Set data to present.
        """
        self.data = data
        self.show_data()

    def show_data(self):
        """Set data into tableWidget.
        """
        if self.data == []:
            self._reset_table()
            return
        self._preset_table()
        for i, row in enumerate(self.data):
            for j, v in enumerate(row):
                if j == 0:
                    name = v
                    item = QTableWidgetItem(v)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, item)
                elif j == 1: # elementWidget
                    elem_widget = v

                    elem_btn = QPushButton(name)
                    elem_btn.setAutoDefault(True)
                    elem_btn.clicked.connect(
                        lambda: self.on_show_elem_info(name, elem_widget))
                    elem_btn.setToolTip(
                        "Element to monitor, click to see element detail")
                    elem_btn.setCursor(Qt.PointingHandCursor)

                    self.tableWidget.setCellWidget(i, j, elem_btn)
            # Add another col for delete btn
            del_btn= QToolButton(self)
            del_btn.setIcon(QIcon(QPixmap(delete_icon)))
            del_btn.setToolTip("Delete current selection")
            del_btn.setProperty("ename", name)
            del_btn.clicked.connect(self.on_delete)
            self.tableWidget.setCellWidget(i, j+1, del_btn)
        self._postset_table()

    @pyqtSlot()
    def on_delete(self):
        """Delete point.
        """
        self.removeElement.emit(self.sender().property("ename"))

    def _postset_table(self):
        """
        """
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()

    def _preset_table(self):
        """Set horizontal header labels, row/column size.
        """
        header = ['Name', 'Element', '']
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setHorizontalHeaderLabels(header)

    def _reset_table(self):
        """Reset table without data.
        """
        self._preset_table()
        self._postset_table()

    @pyqtSlot()
    def on_update(self):
        """Update tableWidget.
        """
        print("update view")
        self.parent.on_show_extra_monitors()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def on_show_elem_info(self, name, elemWidget):
        elemWidget.setWindowTitle(name)
        elemWidget.show()