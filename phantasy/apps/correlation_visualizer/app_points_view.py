#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint


from phantasy.apps.correlation_visualizer.ui.ui_points_view import Ui_Form


class PointsViewWidget(QWidget, Ui_Form):
    """
    """
    # remove alter idx from selected index array
    removeAlterIndex = pyqtSignal(int)

    def __init__(self, parent, data):
        super(PointsViewWidget, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Points Selected by Lasso Tool")

        # set and show data
        self.set_data(data)

        self.removeAlterIndex[int].connect(self.parent.update_retake_indices_view)

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
                if j == 0: # idx
                    alter_idx = v # index of alter array
                    item = QTableWidgetItem('{0:d}'.format(v))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                elif j == 4: # avg_y + sy
                    item = QTableWidgetItem(u'{0:.4f}\N{PLUS-MINUS SIGN}{1:.1f}%'.format(v[0], v[1]/v[0]*100))
                    item.setForeground(QColor('red'))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item = QTableWidgetItem('{0:.4f}'.format(v))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
            # Add another col for delete btn
            del_btn= QPushButton("Delete")
            del_btn.setToolTip("Select/deselect current point")
            del_btn.setProperty("alter_idx", alter_idx)
            del_btn.clicked.connect(self.on_delete)
            self.tableWidget.setCellWidget(i, j+1, del_btn)
        self._postset_table()

    @pyqtSlot()
    def on_delete(self):
        """Delete point.
        """
        self.removeAlterIndex.emit(self.sender().property("alter_idx"))

    def _postset_table(self):
        """
        """
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()

    def _preset_table(self):
        """Set horizontal header labels, row/column size.
        """
        header = ['Index', 'X_Set', 'X_Read', 'Y_Read', 'New_Y_Read', '']
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setHorizontalHeaderLabels(header)

    def _reset_table(self):
        """Reset table without data.
        """
        self._preset_table()
        self._postset_table()
